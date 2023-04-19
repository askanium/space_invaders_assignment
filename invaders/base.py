from abc import ABC, abstractmethod

from core.exceptions import NoSignalException
from core.types import Frame


class PrettyRepresentationABC(ABC):
    @abstractmethod
    def pretty_representation(self):
        raise NotImplementedError("Method not implemented")


class Invader(PrettyRepresentationABC, ABC):
    """
    An abstract class for an Invader.

    The invader shape is represented as a matrix of 0 and 1.

    Below is an example of an Invader:

    00100000100
    00010001000
    00111111100
    01101110110
    11111111111
    10111111101
    10100000101
    00011011000
    """

    def __init__(self, binary_matrix: Frame):
        self._pattern = binary_matrix
        self._number_of_signal_bits = self.compute_number_of_signal_bits()
        self._number_of_total_bits = self.compute_number_of_total_bits()
        self._signal_ratio = self.number_of_signal_bits / self.number_of_total_bits

        if self._number_of_signal_bits == 0:
            raise NoSignalException("Invader pattern does not contain any signal! You won't be able to search for invisible Invaders. At least not now ;)")

    @property
    def pattern(self) -> Frame:
        return self._pattern

    @property
    def number_of_signal_bits(self) -> int:
        return self._number_of_signal_bits

    @property
    def number_of_total_bits(self) -> int:
        return self._number_of_total_bits

    @property
    def signal_ratio(self) -> float:
        return self._signal_ratio

    @property
    def width(self):
        return len(self.pattern[0])

    @property
    def height(self):
        return len(self.pattern)

    def match_against_frame(self, frame: Frame) -> float:
        """
        Matches Invader's known shape against a provided frame (segment of a map)
        and computes the probability that the invader is represented in the noisy
        frame.

        :param frame: The area of the map that has the size of the invader.
        :return: The probability that the invader is represented in the frame.
        """
        matched_bits = 0

        for i, row in enumerate(frame):
            for j, bit in enumerate(row):
                if frame[i][j] == self.pattern[i][j]:
                    matched_bits += 1

        return matched_bits / self.number_of_total_bits

    def compute_number_of_signal_bits(self) -> int:
        """
        Compute the amount of 1s in the invader pattern.
        :return: The number of signal bits in an invader pattern.
        """
        return sum(sum(self.pattern, []))

    def compute_number_of_total_bits(self) -> int:
        """
        Compute the amount of total bits in the invader pattern.
        :return: The number of total bits in the invader pattern.
        """
        return len(self.pattern) * len(self.pattern[0])

    def __str__(self):
        return '\n'.join([''.join(map(str, row)) for row in self.pattern])


class IdentifiedInvader(PrettyRepresentationABC, ABC):
    """
    An invader that was identified by a Radar. Alongside its binary matrix,
    contains information about the similarity ratio, coordinates on map, and
    original Invader it was matched against.
    """
    def __init__(self, original: Invader, binary_matrix: Frame, similarity_ratio: float, frame_coords_on_map: list[int]):
        self.original_invader = original
        self.pattern = binary_matrix
        self.similarity_ratio = similarity_ratio
        self.frame_coords_on_map = frame_coords_on_map
