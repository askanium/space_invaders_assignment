from abc import ABC, abstractmethod

from core.types import Frame
from invaders.base import Invader


class Scanner(ABC):
    """
    Scans frames to search for a given invader target.

    Frame processing is conditional. There is a method that can decide whether
    the amount of signal in the frame is sufficient to contain a potential invader.
    """
    def __init__(self, invader: Invader, similarity_threshold: float):
        self.invader_target = invader
        self.similarity_threshold = similarity_threshold

    @abstractmethod
    def process_frame(self, frame: Frame) -> float:
        """
        Processes a frame and returns the similarity ratio to the searched invader.
        :param frame: The frame to be processed.
        :return: The probability of an invader being in the frame.
        """
        raise NotImplementedError("Method not implemented.")

    @abstractmethod
    def is_worth_processing_frame(self, signal_bits_in_frame: int) -> bool:
        """
        Decide whether the frame should be processed based on the amount of
        information it holds.
        :param signal_bits_in_frame: The amount of information in frame.
        :return: A boolean whether the frame should undergo processing.
        """
        raise NotImplementedError("Method not implemented.")

    @property
    def required_frame_coords(self) -> tuple[int, int]:
        """
        The size of the necessary frame to be provided to the scanner.
        :return: The width and height of the expected frame.
        """
        return self.invader_target.width, self.invader_target.height
