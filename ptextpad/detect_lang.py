"""Detect language using longid.classify.

detct as Chinese if chinese_char_ratio>= threthold else dectect_language()

"""
# import logging
from typing import Optional

from fastlid import fastlid
from logzero import logger

# LOGGER = logging.getLogger(__name__)
# LOGGER.addHandler(logging.NullHandler())


def detect_lang(text1: str, checklen: Optional[int] = None) -> str:
    """Detect Chinese and other languages.

    Args:
        text1: to detect which lang
        checklen: number of chars to process, default 3000
    """
    if checklen is None:
        checklen = 3000
    else:
        try:
            checklen = int(checklen)
        except Exception:
            checklen = 3000
    if checklen <= 1:
        checklen = 3000

    text1 = str(text1)

    # langid.set_languages(langs)
    text0 = text1[:checklen]

    detected = "en"
    try:
        # detected = langid.classify(text0)[0]
        detected = fastlid(text0)[0]
    except Exception as exc:
        # LOGGER.debug(" langid.classify failed: %s", exc)
        LOGGER.debug(" fastlid failed: %s", exc)

    return detected
