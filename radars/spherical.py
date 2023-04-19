from radars.area import DPAreaRadar


class DPSphericalRadar(DPAreaRadar):
    """
    A Radar that treats the provided Map as a sphere.
    Uses dynamic programming to improve performance of search.
    """

    def get_next_frame_coords(self) -> [[int, int], [int, int]]:
        """
        Compute the coordinates of the next available frame within the map.

        Note that given the fact the radar treats the map as a spherical one,
        it means that its coordinates can wrap over to the other side, both
        horizontally and vertically.

        For instance, this frame whose top left corner is at row idx 1 and
        col idx 3 and bottom right corner is at row idx 2 and col idx 0 is
        a valid frame in a spherical map:

        0 0 1 0
        -+   +-
        1|0 0|1
        1|1 0|0
        -+   +-
        0 1 1 1

        The frame starts at
        :return: A list made of the coordinates of the top left and bottom right points.
        """
        if self.map_scanned:
            return []

        invader_width, invader_height = self.scanner.required_frame_coords
        current_x, current_y = self.current_coords
        map_width, map_height = self.map.width, self.map.height

        if current_x < map_width:
            if current_y < map_height:
                self.current_coords[0] += 1
                x_right = current_x + invader_width - 1
                y_bottom = current_y + invader_height - 1

                # if x overflows the provided rectangular region of the map,
                # it means it wraps over to the left side of the map
                if x_right >= map_width:
                    x_right -= map_width

                # likewise, if y overflows, it wraps up to the top of the map
                if y_bottom >= map_height:
                    y_bottom -= map_height

                return [[current_x, current_y], [x_right, y_bottom]]
            else:
                self.map_scanned = True
                return []
        else:
            self.current_coords = [0, current_y + 1]
            return self.get_next_frame_coords()

    def compute_frame_signal_bits_amount(
        self, frame_coords: [[int, int], [int, int]]
    ) -> int:
        """
        If the frame does not wrap around on any direction, use the inherited way
        of DP matrix, which is optimized.
        Otherwise, compute signal ratio of the wrapped areas and add them up.

        The worst case scenario is when the map wraps around both horizontally
        and vertically.

         A    B
        0 1|1|1
        ---+ +-
        1 0 1 0
        ---+ +-
        1 0|0|1
         C    D

        A 3x2 frame that starts in the bottom-right corner of the map (D) wraps
        around horizontally (C), vertically (B), and diagonally (A). In such case,
        the signal ratio of the wrapped frame consists of the sum of A + B + C + D.

        :param frame_coords: The coordinates of the frame for which to compute the signal bits
        :return: Number of signal bits in the frame.
        """
        [top_x, top_y], [bottom_x, bottom_y] = frame_coords
        if top_x <= bottom_x and top_y <= bottom_y:
            return super().compute_frame_signal_bits_amount(frame_coords)

        a_signal_bits = 0
        b_signal_bits = 0
        c_signal_bits = 0

        # first, count the signal bits in the non-wrapped map area, from the
        # top-left corner of the frame, to the bottom-right corner of the map
        map_width_x = self.map.width - 1
        map_height_y = self.map.height - 1
        d_bottom_x = bottom_x
        d_bottom_y = bottom_y

        # if bottom_y coordinates are wrapped, they will be smaller that the top
        # coordinates, meaning the frame was wrapped vertically, and we need to
        # compute the signal ratio of the wrapped square as well.
        if bottom_y < top_y:
            d_bottom_y = map_height_y
            b_frame_bottom_x = bottom_x if bottom_x > top_x else map_width_x
            b_frame_coords = [[top_x, 0], [b_frame_bottom_x, bottom_y]]
            b_signal_bits = super().compute_frame_signal_bits_amount(b_frame_coords)

        if bottom_x < top_x:
            d_bottom_x = map_width_x
            c_frame_bottom_y = bottom_y if bottom_y > top_y else map_height_y
            c_frame_coords = [[0, top_y], [bottom_x, c_frame_bottom_y]]
            c_signal_bits = super().compute_frame_signal_bits_amount(c_frame_coords)

        # if the frame wraps on both directions, we need to compute signal bits in A
        if bottom_x < top_x and bottom_y < top_y:
            a_frame_coords = [[0, 0], [bottom_x, bottom_y]]
            a_signal_bits = super().compute_frame_signal_bits_amount(a_frame_coords)

        d_frame_coords = [[top_x, top_y], [d_bottom_x, d_bottom_y]]
        d_signal_bits = super().compute_frame_signal_bits_amount(d_frame_coords)

        return a_signal_bits + b_signal_bits + c_signal_bits + d_signal_bits
