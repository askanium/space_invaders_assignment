from core.types import Frame
from invaders.base import Invader
from scanners.base import Scanner


class BasicScanner(Scanner):
    def __init__(self, target: Invader, threshold=None):
        self.invader_target = target

        # in case no threshold is provided, consider it as the target
        # invader's signal ratio - a constant factor of 0.2 (taken at random).
        if not threshold:
            threshold = max(0.1, target.signal_ratio - 0.2)

        self.probability_threshold = threshold

    def process_frame(self, frame: Frame) -> float:
        """
        Process the frame and return the probability that there is an
        invader represented in it.
        :param frame: The frame to process.
        :return: The probability that it contains an invader.
        """
        return self.invader_target.match_against_frame(frame)
