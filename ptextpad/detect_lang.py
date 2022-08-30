"""Detect language using fastlid.

Detect language using longid.classify.
detct as Chinese if chinese_char_ratio>= threthold else dectect_language()
"""
# import logging
from typing import Optional

import logzero
from fastlid import fastlid
from logzero import logger
from set_loglevel import set_loglevel


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
        logger.warning(" fastlid failed: %s, set to en", exc)
    # due to a logzero.setup_default_logger/loglevel(20) used in fastlid in 0.1.7
    logzero.loglevel(set_loglevel())

    return detected
