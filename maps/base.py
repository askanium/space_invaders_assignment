from core.types import Frame


class Map:
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
    representation: Frame

    def get_binary_representation(self):
        return self.representation

    @property
    def width(self):
        return len(self.representation[0])

    @property
    def height(self):
        return len(self.representation)

    def __str__(self):
        return '\n'.join([''.join(map(str, row)) for row in self.representation])
