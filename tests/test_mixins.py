import pytest

from core.exceptions import InvalidAsciiCharacterException
from core.mixins import AsciiToBinaryMixin


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
    actual_result = AsciiToBinaryMixin.convert_ascii_to_binary_matrix(ascii_string.strip())

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
