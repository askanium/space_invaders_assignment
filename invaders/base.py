from abc import ABC, abstractmethod

from core.types import Frame


class Invader(ABC):
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

    @abstractmethod
    def pretty_representation(self):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def match_against_frame(self, frame: Frame) -> float:
        raise NotImplementedError("Method not implemented")

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

    def compute_number_of_signal_bits(self) -> int:
        """
        Compute the amount of 1s in the invader pattern.
        :return: The number of signal bits in an invader pattern.
        """
        return sum(sum(self.pattern, []))

    def compute_number_of_total_bits(self) -> int:
        return len(self.pattern) * len(self.pattern[0])

    def __str__(self):
        return '\n'.join([''.join(map(str, row)) for row in self.pattern])
