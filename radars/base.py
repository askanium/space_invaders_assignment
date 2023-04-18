from abc import ABC, abstractmethod

from core.exceptions import MapTooSmallException
from invaders.base import IdentifiedInvader
from invaders.identified import AsciiIdentifiedInvader
from maps.base import Map
from scanners.base import Scanner


class Radar(ABC):
    """
    A radar class that can scan a map and identify potential locations of an invader.
    """
    identified_invader_class: IdentifiedInvader = AsciiIdentifiedInvader

    def __init__(self, map_: Map, scanner: Scanner):
        self.map = map_
        self.scanner = scanner

        self.validate_inputs()

    @abstractmethod
    def scan(self):
        """
        Scans the map and identifies invader locations.
        """
        raise NotImplementedError("Method not implemented.")

    @abstractmethod
    def get_identified_invaders(self) -> list[IdentifiedInvader]:
        """
        Returns potential invader frame locations.
        :return:
        """
        raise NotImplementedError("Method not implemented.")

    def validate_inputs(self):
        invader_width, invader_height = self.scanner.required_frame_coords
        if invader_width > self.map.width or invader_height > self.map.height:
            raise MapTooSmallException("Invader pattern size cannot be bigger than map size.")
