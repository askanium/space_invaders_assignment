from unittest import mock

import pytest

from core.exceptions import MapTooSmallException
from maps.ascii import AsciiMap
from radars.area import DPAreaRadar


@mock.patch.object(DPAreaRadar, 'compute_dp_matrix')
def test_dp_area_radar_validate_inputs_successfully(mock_compute_dp_matrix):
    # setup
    map_ = mock.Mock()
    map_.width = 3
    map_.height = 3
    scanner = mock.Mock()
    scanner.required_frame_coords = [2, 3]

    # run & assert
    DPAreaRadar(map_, scanner)
    mock_compute_dp_matrix.assert_called_once()


@mock.patch.object(DPAreaRadar, 'compute_dp_matrix')
def test_dp_area_radar_validate_inputs_raises_exception(mock_compute_dp_matrix):
    # setup
    map_ = mock.Mock()
    map_.width = 3
    map_.height = 3
    scanner = mock.Mock()
    scanner.required_frame_coords = [2, 4]

    # run & assert
    with pytest.raises(MapTooSmallException):
        DPAreaRadar(map_, scanner)


def test_dp_area_radar_compute_frame_signal_bits_amount():
    # setup
    map_ = AsciiMap(
        f"o-oo-\n"
        f"o-o-o\n"
        f"oo--o\n"
    )
    scanner = mock.Mock()
    scanner.required_frame_coords = [1, 1]
    radar = DPAreaRadar(map_, scanner)
    expected_result = 3

    # run
    actual_result = radar.compute_frame_signal_bits_amount([[1, 2], [2, 4]])

    # assert
    assert actual_result == expected_result


def test_dp_area_radar_compute_frame_signal_bits_amount_case_frame_at_top_of_map():
    # setup
    map_ = AsciiMap(
        f"o-oo-\n"
        f"o-o-o\n"
        f"oo--o\n"
    )
    scanner = mock.Mock()
    scanner.required_frame_coords = [1, 1]
    radar = DPAreaRadar(map_, scanner)
    expected_result = 4

    # run
    actual_result = radar.compute_frame_signal_bits_amount([[0, 1], [1, 4]])

    # assert
    assert actual_result == expected_result


def test_dp_area_radar_compute_frame_signal_bits_amount_case_frame_at_left_of_map():
    # setup
    map_ = AsciiMap(
        f"o-oo-\n"
        f"o-o-o\n"
        f"oo--o\n"
    )
    scanner = mock.Mock()
    scanner.required_frame_coords = [1, 1]
    radar = DPAreaRadar(map_, scanner)
    expected_result = 2

    # run
    actual_result = radar.compute_frame_signal_bits_amount([[1, 0], [2, 0]])

    # assert
    assert actual_result == expected_result


def test_dp_area_radar_compute_frame_signal_bits_amount_case_frame_at_top_left_of_map():
    # setup
    map_ = AsciiMap(
        f"o-oo-\n"
        f"o-o-o\n"
        f"oo--o\n"
    )
    scanner = mock.Mock()
    scanner.required_frame_coords = [1, 1]
    radar = DPAreaRadar(map_, scanner)
    expected_result = 6

    # run
    actual_result = radar.compute_frame_signal_bits_amount([[0, 0], [2, 2]])

    # assert
    assert actual_result == expected_result


@mock.patch.object(DPAreaRadar, 'compute_dp_matrix')
def test_dp_area_radar_get_next_frame_coords(mocked_method):
    # setup
    map_ = mock.Mock()
    map_.width = 3
    map_.height = 4

    scanner = mock.Mock()
    scanner.required_frame_coords = [2, 3]
    radar = DPAreaRadar(map_, scanner)
    expected_result = [
        [[0, 0], [1, 2]],
        [[1, 0], [2, 2]],
        [[0, 1], [1, 3]],
        [[1, 1], [2, 3]],
    ]
    actual_result = []

    # run
    while frame_coords := radar.get_next_frame_coords():
        actual_result.append(frame_coords)

    # assert
    assert actual_result == expected_result
