from abc import ABC, abstractmethod

from core.types import Frame
from invaders.base import Invader


class Scanner(ABC):
    invader_target: Invader
    probability_threshold: float

    @property
    def required_frame_coords(self):
        return self.invader_target.width, self.invader_target.height

    @abstractmethod
    def process_frame(self, frame: Frame) -> float:
        raise NotImplementedError("Method not implemented.")

    def is_worth_analysing_frame(self, signal_bits_in_frame: int) -> bool:
        frame_signal_ratio = signal_bits_in_frame / self.invader_target.number_of_total_bits
        return frame_signal_ratio >= self.probability_threshold
