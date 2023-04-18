from core.types import Frame
from invaders.base import Invader
from scanners.base import Scanner


class BasicScanner(Scanner):
    """
    A basic scanner that performs rough frame processing to search for the target invader.

    Frame processing is conditional
    """
    def __init__(self, target: Invader, signal_threshold=None, similarity_threshold=None):
        # similarity threshold is the value that defines the ratio of bits
        # that have to be in their correct position in order for the radar
        # to treat it as an invader.
        if not similarity_threshold:
            similarity_threshold = 0.7

        super().__init__(target, similarity_threshold)

        # in case no threshold is provided, consider it as the target
        # invader's signal ratio - a constant factor of 0.2 (taken at random).
        if not signal_threshold:
            signal_threshold = max(0.1, target.signal_ratio - 0.2)

        self.signal_threshold = signal_threshold

    def process_frame(self, frame: Frame) -> float:
        """
        Compute the ratio of similarity of the frame to the invader.
        :param frame: The frame to process.
        :return: The similarity ratio to the invader.
        """
        return self.invader_target.match_against_frame(frame)

    def is_worth_processing_frame(self, signal_bits_in_frame: int) -> bool:
        """
        Check if frame's signal ratio is greater than the expected signal ratio
        :param signal_bits_in_frame: Amount of signal bits in frame.
        :return: A boolean whether there is sufficient signal to process the frame.
        """
        frame_signal_ratio = signal_bits_in_frame / self.invader_target.number_of_total_bits
        return frame_signal_ratio >= self.signal_threshold
