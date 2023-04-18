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
    pattern: Frame
    number_of_signal_bits: int
    number_of_total_bits: int
    signal_ratio: float

    @abstractmethod
    def match_against_frame(self, frame: Frame) -> float:
        """
        Matches Invader's known shape against a provided frame (segment of a map)
        and computes the probability that the invader is represented in the noisy
        frame.

        :param frame: The area of the map that has the size of the invader.
        :return: The probability that the invader is represented in the frame.
        """
        raise NotImplementedError("Method not implemented")

    @property
    def width(self):
        # TODO address edge case when there might not be first element in self.pattern
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

    def __str__(self):
        return '\n'.join([''.join(map(str, row)) for row in self.pattern])
