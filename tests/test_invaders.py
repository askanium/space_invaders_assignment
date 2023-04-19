import pytest

from core.exceptions import (
    EmptyFrameException,
    EmptyInvaderException,
    NonMatchingFramesException,
    NoSignalException,
)
from core.types import Frame
from invaders.ascii import AsciiInvader


def test_invader_raises_exception_on_empty_signal():
    # run & assert
    with pytest.raises(NoSignalException):
        AsciiInvader("---")


def test_ascii_invader_validate_frame_raises_empty_frame_exception():
    # setup
    frame = []
    invader = AsciiInvader("-o-")

    # run & assert
    with pytest.raises(EmptyFrameException):
        invader.validate_frame(Frame(frame))


def test_ascii_invader_raises_empty_invader_exception():
    # setup
    ascii_input = "~~~\n~~~"

    # run & assert
    with pytest.raises(EmptyInvaderException):
        AsciiInvader(ascii_input)


def test_ascii_invader_validate_frame_raises_non_matching_frames_exception():
    # setup
    frame = [[0, 1, 0]]
    invader = AsciiInvader("-o")

    # run & assert
    with pytest.raises(NonMatchingFramesException):
        invader.validate_frame(Frame(frame))


def test_ascii_invader_match_against_frame():
    # setup
    frame = [
        [0, 1, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
    ]
    invader = AsciiInvader("~~~\n" "oo--\n" "oooo\n" "--oo\n" "~~~")
    expected_probability = 0.75

    # run
    match_probability = invader.match_against_frame(Frame(frame))

    # assert
    assert match_probability == expected_probability
