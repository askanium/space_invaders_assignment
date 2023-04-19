from abc import ABC, abstractmethod

from core.types import Frame


class Map(ABC):
    """
    An abstract class for a Map.

    The map is represented as a matrix of 0 and 1.

    Below is an example of a Map:

    001001001110100
    000101111001000
    001110110001100
    010101110010110
    111011000111111
    101111000011101
    101000001000001
    000110110000000
    """

    def __init__(self, representation: Frame):
        self.representation = representation

    @abstractmethod
    def print_frame_at(self, x_start: int, y_start: int, x_end: int, y_end: int):
        raise NotImplementedError("Method not implemented.")

    def get_binary_representation(self):
        return self.representation

    @property
    def width(self):
        return len(self.representation[0])

    @property
    def height(self):
        return len(self.representation)

    @abstractmethod
    def get_frame_at(self, x_start: int, y_start: int, x_end: int, y_end: int) -> Frame:
        frame = Frame([])
        for i in range(y_start, y_end + 1):
            row = self.representation[i][x_start:x_end + 1]
            frame.append(row)
        return frame

    def __str__(self):
        return "\n".join(["".join(map(str, row)) for row in self.representation])
