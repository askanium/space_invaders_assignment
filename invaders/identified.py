from core.mixins import BinaryToAsciiMixin
from invaders.base import IdentifiedInvader


class AsciiIdentifiedInvader(BinaryToAsciiMixin, IdentifiedInvader):
    """
    An identified Invader that can be represented in ASCII.
    """

    def pretty_representation(self):
        invader_string = self.convert_binary_matrix_to_ascii(self.pattern)

        str_repr = (
            f"Similarity ratio: {self.similarity_ratio}\n"
            f"Coords on map: {self.frame_coords_on_map}\n"
            f"Visual representation:\n"
            f"{invader_string}"
        )

        return str_repr
