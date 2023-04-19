class FrameCoords:
    def __init__(self, x_left: int, y_top: int, x_right: int, y_bottom: int):
        self.x_left: int = x_left
        self.y_top: int = y_top
        self.x_right: int = x_right
        self.y_bottom: int = y_bottom

    @property
    def top_left_corner(self) -> [int, int]:
        return self.x_left, self.y_top

    @property
    def bottom_right_corner(self) -> [int, int]:
        return self.x_right, self.y_bottom
