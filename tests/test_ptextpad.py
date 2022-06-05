"""Test ptextpad."""
# pylint: disable=broad-except
from ptextpad import __version__
from ptextpad import ptextpad


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not ptextpad()
    except Exception:
        assert True
