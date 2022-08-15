"""Det chardet file."""
import logging
import os

# from nose.tools import eq_, with_setup
import chardet

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def chardet_file(filepath, checklen=30000):
    """
    in: filepath
    out: encoding
    """
    if not os.path.exists(filepath):
        LOGGER.warning(" %s does not exist, retunr None ", filepath)
        return None
    try:
        encoding = "{encoding}".format_map(
            chardet.detect(open(filepath, "rb").read()[:checklen])
        )
        # encoding = "{encoding}".format_map(chardet.detect(open(filepath, 'rb').read()))
    except Exception as exc:
        LOGGER.error("Something not right: %s", exc)
        return None
    return encoding
