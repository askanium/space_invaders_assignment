from core.exceptions import EmptyFrameException, NonMatchingFramesException, EmptyInvaderException
from core.mixins import AsciiToBinaryMixin
from invaders.base import Invader


class AsciiInvader(AsciiToBinaryMixin, Invader):
    """
    An invader represented as ASCII characters.
    """

    def __init__(self, ascii_string: str):
        cleaned_ascii_string = ascii_string.strip("~\n")
        self.pattern = self.convert_ascii_to_binary_matrix(cleaned_ascii_string)

        if not self.pattern:
            raise EmptyInvaderException("An Invader's pattern should not be empty.")

        self.number_of_signal_bits = self.compute_number_of_signal_bits()
        self.number_of_total_bits = len(self.pattern) * len(self.pattern[0])

    def match_against_frame(self, frame: list[list[int]]):
        self.validate_frame(frame)

        matched_bits = 0

        for i, row in enumerate(frame):
            for j, bit in enumerate(row):
                if frame[i][j] == self.pattern[i][j]:
                    matched_bits += 1

        return matched_bits / self.number_of_total_bits

    def validate_frame(self, frame: list[list[int]]):
        if not frame:
            raise EmptyFrameException()
        if len(frame) != len(self.pattern) or len(frame[0]) != len(self.pattern[0]):
            raise NonMatchingFramesException()
