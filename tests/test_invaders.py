import pytest

from core.exceptions import EmptyFrameException
from invaders.ascii import AsciiInvader


def test_ascii_invader_validate_frame_raises_empty_frame_exception():
    # setup
    frame = []
    invader = AsciiInvader("-o-")

    # run & assert
    with pytest.raises(EmptyFrameException):
        invader.validate_frame(frame)
