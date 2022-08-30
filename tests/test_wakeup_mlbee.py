"""Test wakeup_mlbee."""
from ptextpad.wakeup_mlbee import wakeup_mlbee


def test_wakeup_mlbee():
    """Test wakeup_mlbee."""
    res = wakeup_mlbee()
    assert res
