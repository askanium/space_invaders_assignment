from core.mixins import DynamicProgrammingMixin
from core.utils import FrameCoords
from invaders.base import IdentifiedInvader
from maps.base import Map
from radars.base import Radar
from scanners.base import Scanner


class DPAreaRadar(DynamicProgrammingMixin, Radar):
    """
    A Radar that treats the provided Map as a rectangular area of space.
    Uses dynamic programming to improve performance of search.
    """

    def __init__(self, map_: Map, scanner: Scanner):
        super().__init__(map_, scanner)
        self.dp_matrix = self.compute_dp_matrix(map_)
        self.current_coords = [0, 0]
        self.map_scanned = False
        self.identified_invaders: list[IdentifiedInvader] = []

    def get_next_frame_coords(self) -> FrameCoords | None:
        """
        Compute the coordinates of the next available frame within the map.
        :return: A list made of the coordinates of the top left and bottom right points.
        """
        if self.map_scanned:
            return None

        invader_width, invader_height = self.scanner.required_frame_size
        current_x, current_y = self.current_coords
        map_width, map_height = self.map.width, self.map.height

        if current_x + invader_width - 1 < map_width:
            if current_y + invader_height - 1 < map_height:
                self.current_coords[0] += 1
                return FrameCoords(current_x, current_y, current_x + invader_width - 1, current_y + invader_height - 1)
            else:
                self.map_scanned = True
                return None
        else:
            self.current_coords = [0, current_y + 1]
            return self.get_next_frame_coords()

    def compute_frame_signal_bits_amount(
        self, frame_coords: FrameCoords
    ) -> int:
        """
        Compute how many signal bits are there in the frame with the provided coordinates.
        In order to optimize this process and not parse the entire frame each time this
        method is called, make use of the pre-populated dynamic programming matrix.

        For instance, the number of signal digits in this subsection of the map is 3:

        1 0 1 1 0
           +-----+
        1 0|1 0 1|
        1 1|0 0 1|
           +-----+

        Can be computed in O(1) time as follows, using the DP matrix:

         A    B
        1 1|2 3 3
        ---+-----
        2 2|4 5 6
        3 4|6 7 9
         C    D

        1. Take the total signal bits from (0,0) to D region of interest bottom corner. Result = 9
        2. Subtract total signal bits of the C frame, up until the D frame starts. Result -= 4
        3. Subtract total signal bits of the B frame, up until the D frame starts. Result -= 3
        4. Add total signal of bits of the A frame, since it was subtracted twice, as it
           is part of both B and C frames. Result += 1

        Thus, 9 - 4 - 3 + 1 = 3. (qed)

        :param frame_coords: The coordinates of the frame for which to compute the signal bits
        :return: Number of signal bits in the frame.
        """
        a_signal_bits = 0
        b_signal_bits = 0
        c_signal_bits = 0
        d_signal_bits = self.dp_matrix[frame_coords.y_bottom][frame_coords.x_right]
        if frame_coords.x_left > 0:
            c_signal_bits = self.dp_matrix[frame_coords.y_bottom][frame_coords.x_left - 1]
        if frame_coords.y_top > 0:
            b_signal_bits = self.dp_matrix[frame_coords.y_top - 1][frame_coords.x_right]
        if frame_coords.x_left > 0 and frame_coords.y_top > 0:
            a_signal_bits = self.dp_matrix[frame_coords.y_top - 1][frame_coords.x_left - 1]

        return d_signal_bits - c_signal_bits - b_signal_bits + a_signal_bits

    def scan(self):
        """
        Scan the map one frame at a time and decide, based on the signal threshold,
        whether the frame should be analyzed more in-depth
        :return:
        """
        while frame_coords := self.get_next_frame_coords():
            frame_signal_bits_amount = self.compute_frame_signal_bits_amount(
                frame_coords
            )
            if self.scanner.is_worth_processing_frame(frame_signal_bits_amount):
                frame = self.map.get_frame_at(frame_coords)
                similarity_ratio = self.scanner.process_frame(frame)
                if similarity_ratio >= self.scanner.similarity_threshold:
                    identified_invader = self.identified_invader_class(
                        self.scanner.invader_target,
                        frame,
                        similarity_ratio,
                        frame_coords,
                    )
                    self.identified_invaders.append(identified_invader)

    def get_identified_invaders(self) -> list[IdentifiedInvader]:
        return self.identified_invaders
