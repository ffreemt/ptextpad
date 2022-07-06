# coding: utf8
"""
Loads file content to text.

Check encoding and load a file to text.

load_paras(filepath='') ==> paralist, lenlist =

refer to load_paras.py
"""
from pathlib import Path
from typing import Union

from logzero import logger

from .detect_file import detect_file


def load_text(filepath: Union[str, Path]) -> str:
    """Check encoding and load a file to text.

    load_paras(filepath='') ==> paralist, lenlist =
    """

    # encoding = guess_zhencoding(filepath)
    try:
        encoding = detect_file(filepath)
    except Exception as exc:
        logger.error(exc)
        raise

    if not encoding:
        raise Exception("Unable to detect file encoding, is it a binary file?")

    try:
        with open(filepath, encoding=encoding, errors="ignore") as fha:
            text = fha.read()
    except Exception as exc:
        logger.error("Opening %s resulted in errors: %s", filepath, exc)
        raise

    return text
    # return text.encode('gbk','ignore').decode("gbk")
