from abc import ABC, abstractmethod

from maps.base import Map
from scanners.base import Scanner


class Radar(ABC):
    map: Map
    scanner: Scanner

    @abstractmethod
    def scan(self) -> list[[[int, int], [int, int]]]:
        raise NotImplementedError("Method not implemented.")
