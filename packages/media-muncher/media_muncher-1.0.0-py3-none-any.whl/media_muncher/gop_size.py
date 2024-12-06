import math

from media_muncher.framerate import FrameRate


class GopSizeCalculator(object):
    def __init__(
        self,
        video_frame_rate: FrameRate,
        audio_sample_rate: int,
        audio_frames_per_packet: int = 1024,
    ):
        # Input data
        self.video_frame_rate: FrameRate = video_frame_rate
        self.audio_sample_rate: int = audio_sample_rate
        self.audio_frames_per_packet: int = audio_frames_per_packet

        self.gop_size: int = None
        self._calculate_compatible_gop_size()

    def _calculate_compatible_gop_size(self):
        # Not possible with ATSC frame rates
        if not self.video_frame_rate.is_integer():
            return

        vrate = int(float(self.video_frame_rate))
        self.gop_size = (
            vrate
            * self.audio_frames_per_packet
            / math.gcd(vrate * self.audio_frames_per_packet, self.audio_sample_rate)
        )

    def for_target_duration(
        self,
        max_duration: float,
    ) -> float:
        # Calculate the nearest duration to the target duration that is compatible
        # between video frame rate and audio sample rate

        if self.gop_size is None:
            return None

        candidate_durations = []
        dur = 0
        i = 1
        selected_duration = None
        while dur < 12:
            dur = self.gop_size * i / float(self.video_frame_rate)
            candidate_durations.append(dur)

            if dur <= max_duration:
                selected_duration = dur

            i += 1
        return selected_duration
