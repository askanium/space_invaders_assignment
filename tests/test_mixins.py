import pytest

from core.exceptions import InvalidAsciiCharacterException
from core.mixins import AsciiToBinaryMixin, DynamicProgrammingMixin
from maps.ascii import AsciiMap


def test_ascii_to_binary_mixin_convert_ascii_to_binary_matrix():
    # setup
    ascii_string = """
--o--
-o-o-
--o--
    """
    expected_result = [
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
    ]

    # run
    actual_result = AsciiToBinaryMixin.convert_ascii_to_binary_matrix(
        ascii_string.strip()
    )

    # assert
    assert actual_result == expected_result


def test_convert_ascii_to_binary_matrix_raises_invalid_character_exception():
    # setup
    ascii_string = """
-ao--
-o-o-
--o--
    """

    # run & assert
    with pytest.raises(InvalidAsciiCharacterException):
        AsciiToBinaryMixin.convert_ascii_to_binary_matrix(ascii_string)


def test_convert_ascii_to_binary_matrix_return_empty_matrix_on_empty_input():
    # setup
    ascii_string = ""
    expected_result = []

    # run
    actual_result = AsciiToBinaryMixin.convert_ascii_to_binary_matrix(ascii_string)

    # assert
    assert actual_result == expected_result


def test_dp_programming_mixin_compute_dp_matrix():
    # setup
    map_ = AsciiMap(f"o-oo-\n" f"o-o-o\n" f"oo--o\n")
    expected_result = [
        [1, 1, 2, 3, 3],
        [2, 2, 4, 5, 6],
        [3, 4, 6, 7, 9],
    ]

    # run
    actual_result = DynamicProgrammingMixin.compute_dp_matrix(map_)

    # assert
    assert actual_result == expected_result
