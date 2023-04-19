from core.utils import FrameCoords


def test_frame_coords():
    # setup
    coords = FrameCoords(1, 2, 3, 4)
    expected_top_left = 1, 2
    expected_bottom_right = 3, 4

    # run
    top_left = coords.top_left_corner
    bottom_right = coords.bottom_right_corner

    # assert
    assert top_left == expected_top_left
    assert bottom_right == expected_bottom_right
