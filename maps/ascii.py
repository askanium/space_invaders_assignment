from core.exceptions import EmptyMapException
from core.mixins import AsciiToBinaryMixin
from maps.base import Map


class AsciiMap(AsciiToBinaryMixin, Map):
    """
    A map represented as ASCII characters.
    """
    def __init__(self, ascii_map: str):
        cleaned_ascii_string = ascii_map.strip(" ~\n")
        self.representation = self.convert_ascii_to_binary_matrix(cleaned_ascii_string)

        if not self.representation:
            raise EmptyMapException("A Map should not be empty.")
