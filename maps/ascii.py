from core.exceptions import EmptyMapException
from core.mixins import AsciiToBinaryMixin, BinaryToAsciiMixin
from core.types import Frame
from maps.base import Map


class AsciiMap(AsciiToBinaryMixin, BinaryToAsciiMixin, Map):
    """
    A map represented as ASCII characters.
    """

    def __init__(self, ascii_map: str):
        cleaned_ascii_string = ascii_map.strip(" ~\n")
        binary_matrix = self.convert_ascii_to_binary_matrix(cleaned_ascii_string)
        super().__init__(binary_matrix)

        if not binary_matrix:
            raise EmptyMapException("A Map should not be empty.")

    def get_frame_at(self, x_start: int, y_start: int, x_end: int, y_end: int) -> Frame:
        frame = Frame([])
        for i in range(y_start, y_end + 1):
            row = self.representation[i][x_start:x_end+1]
            frame.append(row)
        return frame

    def print_frame_at(self, x_start: int, y_start: int, x_end: int, y_end: int):
        frame = self.get_frame_at(x_start, y_start, x_end, y_end)
        ascii_string = self.convert_binary_matrix_to_ascii(frame)
        print(ascii_string)


class AsciiSphericalMap(AsciiMap, Map):
    """
    A map represented as ASCII characters.
    """
    def get_frame_at(self, x_start: int, y_start: int, x_end: int, y_end: int) -> Frame:
        """
        Allows retrieval of frames assuming the map is spherical and coordinates
        can wrap (i.e. x_end and y_end coordinates can be smaller than x_start and
        y_start).

        :param x_start: X coordinate of top-left corner of the frame.
        :param y_start: Y coordinate of top-left corner of the frame.
        :param x_end: X coordinate of bottom-right corner of the frame.
        :param y_end: Y coordinate of bottom-right corner of the frame.
        :return: The frame.
        """
        frame = Frame([])
        if y_start <= y_end:
            for row in self.representation[y_start:y_end+1]:
                frame.append(self.get_row_subset(row, x_start, x_end))
        else:
            for row in self.representation[y_start:]:
                frame.append(self.get_row_subset(row, x_start, x_end))
            for row in self.representation[:y_end+1]:
                frame.append(self.get_row_subset(row, x_start, x_end))

        return frame

    @staticmethod
    def get_row_subset(row: list[int], x_start: int, x_end: int):
        if x_start <= x_end:
            return row[x_start:x_end + 1]
        else:
            return row[x_start:] + row[:x_end + 1]