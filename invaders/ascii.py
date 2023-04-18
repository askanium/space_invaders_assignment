from core.exceptions import EmptyFrameException, NonMatchingFramesException, EmptyInvaderException
from core.mixins import AsciiToBinaryMixin
from core.types import Frame
from invaders.base import Invader


class AsciiInvader(AsciiToBinaryMixin, Invader):
    """
    An invader represented as ASCII characters.
    """

    def __init__(self, ascii_string: str):
        cleaned_ascii_string = ascii_string.strip("~\n")
        binary_matrix = self.convert_ascii_to_binary_matrix(cleaned_ascii_string)

        if not binary_matrix:
            raise EmptyInvaderException("An Invader's pattern should not be empty.")

        super().__init__(binary_matrix)

    def match_against_frame(self, frame: Frame) -> float:
        """
        Matches Invader's known shape against a provided frame (segment of a map)
        and computes the probability that the invader is represented in the noisy
        frame.

        :param frame: The area of the map that has the size of the invader.
        :return: The probability that the invader is represented in the frame.
        """
        self.validate_frame(frame)

        matched_bits = 0

        for i, row in enumerate(frame):
            for j, bit in enumerate(row):
                if frame[i][j] == self.pattern[i][j]:
                    matched_bits += 1

        return matched_bits / self.number_of_total_bits

    def validate_frame(self, frame: Frame):
        if not frame:
            raise EmptyFrameException()
        if len(frame) != len(self.pattern) or len(frame[0]) != len(self.pattern[0]):
            raise NonMatchingFramesException()

    def pretty_representation(self):
        ascii_string = ''
        for row in self.pattern:
            ascii_string = f"{ascii_string}{''.join('o' if bit else '-' for bit in row)}\n"
        return ascii_string
