from core.exceptions import EmptyMapException
from core.mixins import AsciiToBinaryMixin, BinaryToAsciiMixin
from core.types import Frame
from core.utils import FrameCoords
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

    def get_frame_at(self, frame_coords: FrameCoords) -> Frame:
        frame = Frame([])
        for i in range(frame_coords.y_top, frame_coords.y_bottom + 1):
            row = self.representation[i][frame_coords.x_left:frame_coords.x_right + 1]
            frame.append(row)
        return frame

    def print_frame_at(self, frame_coords: FrameCoords):
        frame = self.get_frame_at(frame_coords)
        ascii_string = self.convert_binary_matrix_to_ascii(frame)
        print(ascii_string)


class AsciiSphericalMap(AsciiMap, Map):
    """
    A map represented as ASCII characters.
    """

    def get_frame_at(self, frame_coords: FrameCoords) -> Frame:
        """
        Allows retrieval of frames assuming the map is spherical and coordinates
        can wrap (i.e. x_end and y_end coordinates can be smaller than x_start and
        y_start).

        :param frame_coords: The coordinates of the frame
        :return: The frame.
        """
        frame = Frame([])
        if frame_coords.y_top <= frame_coords.y_bottom:
            for row in self.representation[frame_coords.y_top:frame_coords.y_bottom + 1]:
                frame.append(self.get_row_subset(row, frame_coords.x_left, frame_coords.x_right))
        else:
            for row in self.representation[frame_coords.y_top:]:
                frame.append(self.get_row_subset(row, frame_coords.x_left, frame_coords.x_right))
            for row in self.representation[:frame_coords.y_bottom + 1]:
                frame.append(self.get_row_subset(row, frame_coords.x_left, frame_coords.x_right))

        return frame

    @staticmethod
    def get_row_subset(row: list[int], x_start: int, x_end: int):
        if x_start <= x_end:
            return row[x_start:x_end + 1]
        else:
            return row[x_start:] + row[: x_end + 1]
