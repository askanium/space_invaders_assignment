from unittest import mock

import pytest

from core.exceptions import MapTooSmallException
from core.types import Frame
from invaders.identified import AsciiIdentifiedInvader
from maps.ascii import AsciiMap
from radars.area import DPAreaRadar
from radars.spherical import DPSphericalRadar


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
    actual_result = radar.compute_frame_signal_bits_amount([[2, 1], [4, 2]])

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
    actual_result = radar.compute_frame_signal_bits_amount([[1, 0], [4, 1]])

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
    actual_result = radar.compute_frame_signal_bits_amount([[0, 1], [0, 2]])

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


@mock.patch.object(DPAreaRadar, 'get_next_frame_coords')
@mock.patch.object(DPAreaRadar, 'compute_frame_signal_bits_amount')
@mock.patch.object(DPAreaRadar, 'compute_dp_matrix')
def test_dp_area_radar_scan_low_frame_signal_amount(mocked_compute_dp, mocket_compute_frame_signal, mocked_get_next_frame):
    # setup
    dummy_frames = [[[0, 1], [1, 1]], []]
    map_ = mock.Mock()
    map_.width = 3
    map_.height = 4
    scanner = mock.Mock()
    scanner.is_worth_processing_frame.return_value = False
    scanner.required_frame_coords = [2, 3]
    radar = DPAreaRadar(map_, scanner)
    mocked_get_next_frame.side_effect = dummy_frames

    # run
    radar.scan()

    # assert
    mocked_get_next_frame.assert_called()
    mocket_compute_frame_signal.assert_called_once_with(dummy_frames[0])
    map_.get_frame_at.assert_not_called()
    scanner.process_frame.assert_not_called()


@mock.patch.object(DPAreaRadar, 'get_next_frame_coords')
@mock.patch.object(DPAreaRadar, 'compute_frame_signal_bits_amount')
@mock.patch.object(DPAreaRadar, 'compute_dp_matrix')
def test_dp_area_radar_scan_high_frame_signal_amount(mocked_compute_dp, mocket_compute_frame_signal, mocked_get_next_frame):
    # setup
    dummy_frames = [[[0, 1], [1, 2]], []]
    map_frame = Frame([[1, 1], [1, 0], [1, 1]])
    processed_similarity_ratio = 0.7

    map_ = mock.Mock()
    map_.width = 3
    map_.height = 4
    map_.get_frame_at.return_value = map_frame

    scanner = mock.Mock()
    scanner.required_frame_coords = [2, 3]
    scanner.similarity_threshold = 0.6
    scanner.is_worth_processing_frame.return_value = True
    scanner.process_frame.return_value = processed_similarity_ratio

    radar = DPAreaRadar(map_, scanner)
    mocked_get_next_frame.side_effect = dummy_frames
    expected_identified_invader = AsciiIdentifiedInvader(mock.Mock(), map_frame, processed_similarity_ratio, dummy_frames[0])

    # run
    radar.scan()

    # assert
    mocked_get_next_frame.assert_called()
    mocket_compute_frame_signal.assert_called_once_with(dummy_frames[0])
    map_.get_frame_at.assert_called_once_with(0, 1, 1, 2)
    scanner.process_frame.assert_called_once_with(map_frame)

    assert len(radar.get_identified_invaders()) == 1
    assert radar.get_identified_invaders()[0].pretty_representation() == expected_identified_invader.pretty_representation()


@mock.patch.object(DPAreaRadar, 'compute_dp_matrix')
def test_dp_spherical_radar_get_next_frame_coords(mocked_method):
    # setup
    map_ = mock.Mock()
    map_.width = 3
    map_.height = 4

    scanner = mock.Mock()
    scanner.required_frame_coords = [2, 3]
    radar = DPSphericalRadar(map_, scanner)
    expected_result = [
        [[0, 0], [1, 2]],
        [[1, 0], [2, 2]],
        [[2, 0], [0, 2]],
        [[0, 1], [1, 3]],
        [[1, 1], [2, 3]],
        [[2, 1], [0, 3]],
        [[0, 2], [1, 0]],
        [[1, 2], [2, 0]],
        [[2, 2], [0, 0]],
        [[0, 3], [1, 1]],
        [[1, 3], [2, 1]],
        [[2, 3], [0, 1]],
    ]
    actual_result = []

    # run
    while frame_coords := radar.get_next_frame_coords():
        actual_result.append(frame_coords)

    # assert
    assert actual_result == expected_result


def test_dp_spherical_radar_compute_frame_signal_bits_amount_case_frame_does_not_wrap():
    # setup
    map_ = AsciiMap(
        f"-ooo\n"
        f"o-o-\n"
        f"o--o\n"
    )
    scanner = mock.Mock()
    scanner.required_frame_coords = [1, 1]
    radar = DPSphericalRadar(map_, scanner)
    expected_result = 5

    # run
    actual_result = radar.compute_frame_signal_bits_amount([[0, 0], [2, 2]])

    # assert
    assert actual_result == expected_result


def test_dp_spherical_radar_compute_frame_signal_bits_amount_case_frame_wraps_horizontally():
    # setup
    map_ = AsciiMap(
        f"-ooo\n"
        f"o-o-\n"
        f"o--o\n"
    )
    scanner = mock.Mock()
    scanner.required_frame_coords = [1, 1]
    radar = DPSphericalRadar(map_, scanner)
    expected_result = 4

    # run
    actual_result = radar.compute_frame_signal_bits_amount([[2, 0], [0, 1]])

    # assert
    assert actual_result == expected_result


def test_dp_spherical_radar_compute_frame_signal_bits_amount_case_frame_wraps_vertically():
    # setup
    map_ = AsciiMap(
        f"-ooo\n"
        f"o-o-\n"
        f"o--o\n"
    )
    scanner = mock.Mock()
    scanner.required_frame_coords = [1, 1]
    radar = DPSphericalRadar(map_, scanner)
    expected_result = 5

    # run
    actual_result = radar.compute_frame_signal_bits_amount([[0, 2], [2, 1]])

    # assert
    assert actual_result == expected_result


def test_dp_spherical_radar_compute_frame_signal_bits_amount_case_frame_wraps_both_ways():
    # setup
    map_ = AsciiMap(
        f"-ooo\n"
        f"o-o-\n"
        f"o--o\n"
    )
    scanner = mock.Mock()
    scanner.required_frame_coords = [1, 1]
    radar = DPSphericalRadar(map_, scanner)
    expected_result = 7

    # run
    actual_result = radar.compute_frame_signal_bits_amount([[3, 2], [2, 1]])

    # assert
    assert actual_result == expected_result
