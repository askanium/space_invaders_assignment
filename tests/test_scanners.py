from unittest import mock

import pytest

from core.types import Frame
from scanners.basic import BasicScanner


@pytest.mark.parametrize(
    "invader_signal,signal,similarity,expected_signal,expected_similarity",
    [
        (0.6, None, None, 0.4, 0.7),
        (0.1, 0.75, 0.85, 0.75, 0.85),
        (0.25, None, 0.85, 0.1, 0.85),
    ],
)
def test_basic_scanner_init(
    invader_signal, signal, similarity, expected_signal, expected_similarity
):
    # setup
    invader = mock.Mock()
    invader.signal_ratio = invader_signal

    # run
    scanner = BasicScanner(
        invader, signal_threshold=signal, similarity_threshold=similarity
    )

    # assert
    assert scanner.signal_threshold == pytest.approx(expected_signal)
    assert scanner.similarity_threshold == expected_similarity


def test_basic_scanner_process_frame():
    # setup
    invader = mock.Mock()
    invader.match_against_frame.return_value = 0.2
    invader.signal_ratio = 0.4
    scanner = BasicScanner(invader)
    frame = Frame([[1, 2]])
    expected_result = 0.2

    # run
    actual_result = scanner.process_frame(frame)

    # assert
    assert actual_result == expected_result
    invader.match_against_frame.assert_called_once_with(frame)


def test_basic_scanner_is_worth_processing_frame():
    # setup
    invader = mock.Mock()
    invader.number_of_total_bits = 10
    invader.signal_threshold = 0.5
    invader.signal_ratio = 0.4
    scanner = BasicScanner(invader)
    expected_result = True

    # run
    actual_result = scanner.is_worth_processing_frame(6)

    # assert
    assert actual_result == expected_result


def test_basic_scanner_required_frame_size():
    # setup
    invader = mock.Mock()
    invader.width = 8
    invader.height = 5
    invader.number_of_total_bits = 10
    invader.signal_threshold = 0.5
    invader.signal_ratio = 0.4
    scanner = BasicScanner(invader)
    expected_result = 8, 5

    # run
    actual_result = scanner.required_frame_size

    # assert
    assert actual_result == expected_result
