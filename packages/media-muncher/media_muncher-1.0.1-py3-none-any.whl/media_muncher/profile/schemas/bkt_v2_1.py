from importlib.metadata import version

from media_muncher.framerate import FrameRate
from media_muncher.h264_levels import H264LevelValidator
from media_muncher.messages import WarningMessage
from media_muncher.resolution import Resolution
from media_muncher.profile.schemas.base import BaseSchemaGenerator
from media_muncher.segment_size import SegmentSizer

PRESET_MAPPING = {
    "VERYFAST": 3,
    "FAST": 5,
    "MEDIUM": 7,
    "SLOW": 9,
    "SLOWER": 11,
    "VERYSLOW": 13,
    "PLACEBO": 15,
}

AAC_BITRATES = [64000, 80000, 96000, 128000, 160000, 192000, 224000, 256000, 320000]

DEFAULT_FRAMERATE = 25


class BktV2dot1ProfileSchemaGenerator(BaseSchemaGenerator):
    schema_name = "bkt-v2.1"

    def generate(self, renditions, packaging, name: str = ""):
        video_renditions = [r for r in renditions if r["type"] == "video"]
        audio_renditions = [r for r in renditions if r["type"] == "audio"]
        video_ladder = {}
        audio_ladder = {}

        default_audio_sample_rate = 48000
        perf_level = PRESET_MAPPING.get(self.config["preset"].upper(), 7)

        # Default framerate (in case of audio-only or if cannot be determined)
        common_framerate = FrameRate(DEFAULT_FRAMERATE)

        # Video renditions (if any)
        if len(video_renditions):
            for r in video_renditions:
                # TODO - must be done on the basis of the codec
                # Ensure that the resolutions are even
                r["resolution"] = Resolution(*r["resolution"]).make_even()

                # Ensure that we have a framerate for all video renditions
                if "framerate" not in r:
                    r["framerate"] = FrameRate(self.config.get("framerate"))
                    self.messages.append(
                        WarningMessage(
                            f"Default video framerate of {self.config.get('framerate')} was selected, "
                            f"since it could not be detected in the source",
                            topic="framerate",
                        )
                    )
                else:
                    if r["framerate"] is not None:
                        r["framerate"] = FrameRate(r["framerate"])
                    else:
                        r["framerate"] = FrameRate(DEFAULT_FRAMERATE)

            # Get a common framerate
            all_framerates = [r.get("framerate") for r in video_renditions]

            # if they're not all the same, find the common one
            if len(set(all_framerates)) == 1:
                multi_rates = False
                common_framerate = all_framerates[0]
            else:
                multi_rates = True
                try:
                    common_framerate = FrameRate.get_common_framerate(all_framerates)
                except ValueError:
                    common_framerate = all_framerates[0]
                    multi_rates = False
                    self.messages.append(
                        WarningMessage(
                            f"The video frame rates are different and incompatible between the renditions. "
                            f"Forcing the first framerate if {common_framerate} on all other renditions",
                            topic="framerate",
                        )
                    )
                    for r in video_renditions:
                        r["framerate"] = common_framerate

            video_ladder = {
                "common": {
                    "perf": perf_level,
                }
            }

            if not multi_rates:
                video_ladder["common"]["framerate"] = {
                    "num": common_framerate.numerator,
                    "den": common_framerate.denominator,
                }

            for i, r in enumerate(video_renditions):
                # Adjust the H264 level
                resol, _, bitrate = H264LevelValidator(r["level"]).adjust(
                    resolution=r.get("resolution"),
                    framerate=r.get("framerate"),
                    bitrate=r.get("bitrate"),
                )
                if resol != r.get("resolution"):
                    self.messages.append(
                        WarningMessage(
                            f"Resolution was adjusted to {resol} (from {r.get('resolution')}) to comply with the H264 level {r['level']}",
                            topic="H264 level",
                        )
                    )
                if bitrate != r.get("bitrate"):
                    self.messages.append(
                        WarningMessage(
                            f"Bitrate was adjusted to {bitrate} bps (from {r.get('bitrate')} bps) to comply with the H264 level {r['level']}",
                            topic="H264 level",
                        )
                    )

                rung = {
                    "_codec_info": f"{r['codec']} {r['profile']} {r['level']}",
                    "codec_string": r["codecstring"],
                    "scale": {"width": -2, "height": resol.height},
                    "bitrate": bitrate,
                }
                if multi_rates:
                    rung["framerate"] = {
                        "num": r["framerate"].numerator,
                        "den": r["framerate"].denominator,
                    }

                video_ladder[f"video_{i}"] = rung

        # Audio renditions
        audio_ladder = {
            "common": {
                "sampling_rate": default_audio_sample_rate,
                "loudnorm": {"i": -23, "tp": -1},
            }
        }

        for i, r in enumerate(audio_renditions):
            bitrate = r.get("bitrate")

            # Select the nearest lower AAC bitrate
            if r.get("codecstring").startswith("mp4a.40."):
                bitrate = max(filter(lambda x: x <= bitrate, AAC_BITRATES))

                if bitrate != r.get("bitrate"):
                    self.messages.append(
                        WarningMessage(
                            f"Bitrate was adjusted to {bitrate} bps (from {r.get('bitrate')} bps) to comply with the AAC codec",
                            topic="AAC codec",
                        )
                    )

            audio_ladder[f"audio_{i}"] = {
                "_codec_info": f"{r['codec']} {r['mode']}",
                "codec_string": r["codecstring"],
                "bitrate": bitrate,
                "channel_layout": "stereo",
            }

        # Packaging options
        packaging_options = {}

        # Calculate the segment duration
        target_segment_duration = packaging.get("segment_duration", 4)
        segment_sizer = SegmentSizer(
            framerate=common_framerate, samplerate=default_audio_sample_rate
        )
        if packaging.get("muxed_audio") is True:
            segment_sizer.set_target_duration(
                target_segment_duration, ignore_audio=True
            )
        else:
            segment_sizer.set_target_duration(target_segment_duration)

        if segment_sizer.actual_duration != target_segment_duration:
            self.messages.append(
                WarningMessage(
                    f"Target segment duration of {target_segment_duration} seconds was adjusted to "
                    f"{round(segment_sizer.actual_duration, 3)} seconds for compatibility "
                    f"with the framerate and audio sample rate.",
                    topic="Segment duration",
                )
            )

        # HLS packaging config
        hls_config = {}
        packaging_options["hls"] = hls_config
        hls_config["fragment_length"] = {
            "num": segment_sizer.numerator,
            "den": segment_sizer.denominator,
        }

        # Specific HLS configuration
        if packaging.get("packaging") == "HLS":
            # TODO - not a great default if done alongside DASH...
            hls_config["version"] = packaging.get("version", 3)
            advanced_config = {}

            if packaging.get("container") == "ISOBMFF":
                hls_config["fragmented_mp4"] = True

            if packaging.get("container") == "MPEG-TS":
                if packaging.get("muxed_audio") is False:
                    hls_config["audio_not_multiplex"] = True

                if packaging.get("audio_only") is False:
                    advanced_config["--hls.no_audio_only"] = ""

            if advanced_config:
                hls_config["advanced"] = advanced_config

        dash_config = {}
        packaging_options["dash"] = dash_config

        dash_config["fragment_length"] = {
            "num": segment_sizer.numerator,
            "den": segment_sizer.denominator,
        }

        # TODO - segment template time or number (for compatibility)

        profile = {
            "version": "02.00.05",
            "name": name,
            "type": "OFFLINE_TRANSCODING",
            "audios": audio_ladder,
            "videos": video_ladder,
            "packaging": packaging_options,
            "_generator": "bpkio-python-sdk/" + version("bpkio-python-sdk"),
        }

        return profile
