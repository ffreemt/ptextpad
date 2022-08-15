"""Detect file's encoding."""
import os
from pathlib import Path
from typing import Optional, Union

import cchardet
from logzero import logger


def detect_file(filepath: Union[str, Path], checklen: Optional[int] = None) -> str:
    """Detect file's encoding.

    Args:
        filepath: str or Path
        checklen: number of bytes to check, if None, check all bytes

    Returns:
        string of encoding
    """
    if not Path(filepath).is_file():
        raise Exception(f" {filepath} does not exist, retunr None ")

    try:
        # encoding = "{encoding}".format_map(chardet.detect(open(filepath, 'rb').read()[:checklen]))

        # encoding = chardet.detect(open(filepath, 'rb').read()[:checklen])['encoding']
        with open(filepath, "rb") as fha:
            if checklen:
                _ = fha.read()[:checklen]
            else:
                _ = fha.read()
    except Exception as exc:
        logger.error("Something not right: %s", exc)
        # return None
        raise

    try:
        _ = cchardet.detect(_)
    except Exception as exc:
        logger.warning(exc)
        # encoding = "utf8"
        raise

    encoding = _.get("encoding")
    if not _:
        raise Exception("None detected, a binary file?")

    return encoding
