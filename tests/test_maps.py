from unittest.mock import patch

import pytest

from core.exceptions import EmptyMapException
from maps.ascii import AsciiMap, AsciiSphericalMap


@pytest.fixture
def map_binary_repr():
    return [
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
    ]


def test_ascii_map_initialization(map_binary_repr):
    # setup
    ascii_string = """
--o--
-o-o-
--o--
    """

    # run
    ascii_map = AsciiMap(ascii_string)

    # assert
    assert ascii_map.representation == map_binary_repr


def test_ascii_map_initialization_raises():
    # setup
    ascii_string = "~~~~~~"

    # run & assert
    with pytest.raises(EmptyMapException):
        AsciiMap(ascii_string)


@patch.object(AsciiMap, "convert_ascii_to_binary_matrix")
def test_ascii_map_get_frame_at(mocked_convert_method, map_binary_repr):
    # setup
    mocked_convert_method.return_value = map_binary_repr
    ascii_map = AsciiMap("")
    expected_result = [
        [1, 0, 1],
        [0, 1, 0],
    ]

    # run
    frame = ascii_map.get_frame_at(1, 1, 3, 2)

    # assert
    assert frame == expected_result


@pytest.mark.parametrize(
    "x_start,y_start,x_end,y_end,expected_result",
    [
        (1, 1, 3, 2, [[1, 0, 1], [0, 1, 0]]),  # doesn't wrap
        (4, 1, 1, 2, [[0, 0, 1], [0, 0, 0]]),  # wrap horizontally
        (1, 2, 3, 0, [[0, 1, 0], [0, 1, 0]]),  # wrap vertically
        (4, 2, 1, 1, [[0, 0, 0], [0, 0, 0], [0, 0, 1]]),  # wrap both ways
    ],
)
@patch.object(AsciiSphericalMap, "convert_ascii_to_binary_matrix")
def test_ascii_spherical_map_get_frame_at(
    mocked_convert_method,
    x_start,
    y_start,
    x_end,
    y_end,
    expected_result,
    map_binary_repr,
):
    # setup
    mocked_convert_method.return_value = map_binary_repr
    ascii_map = AsciiSphericalMap("")

    # run
    frame = ascii_map.get_frame_at(x_start, y_start, x_end, y_end)

    # assert
    assert frame == expected_result
