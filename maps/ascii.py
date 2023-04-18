from core.exceptions import EmptyMapException
from core.mixins import AsciiToBinaryMixin, BinaryToAsciiMixin
from maps.base import Map


class AsciiMap(AsciiToBinaryMixin, BinaryToAsciiMixin, Map):
    """
    A map represented as ASCII characters.
    """

    def __init__(self, ascii_map: str):
        cleaned_ascii_string = ascii_map.strip(" ~\n")
        self.representation = self.convert_ascii_to_binary_matrix(cleaned_ascii_string)

        if not self.representation:
            raise EmptyMapException("A Map should not be empty.")

    def print_frame_at(self, x_start: int, y_start: int, x_end: int, y_end: int):
        frame = self.get_frame_at(x_start, y_start, x_end, y_end)
        ascii_string = self.convert_binary_matrix_to_ascii(frame)
        print(ascii_string)
