# encoding: utf8
"""
Segments Chinese text(2016 10 17).


"""

import logging
import re

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# '[\\w\\W]*?[！？?。\\n][」﹂”』’》）］｝〕〗??〉】]*|[\\w\\W]+'
ZHSENT = b"[\\w\\W]*?[\xef\xbc\x81\xef\xbc\x9f?\xe3\x80\x82\\n][\xe3\x80\x8d\xef\xb9\x82\xe2\x80\x9d\xe3\x80\x8f\xe2\x80\x99\xe3\x80\x8b\xef\xbc\x89\xef\xbc\xbd\xef\xbd\x9d\xe3\x80\x95\xe3\x80\x97??\xe3\x80\x89\xe3\x80\x91]*|[\\w\\W]+"
ZHSENTSTR = ZHSENT.decode("utf8")
ZHPATTERN = re.compile(ZHSENTSTR)


def seg_chinese(text):
    """
    Converts text (str) to a list of sents.


    """
    if not isinstance(text, str):
        LOGGER.warning(" Inout not a string, exising with None...")
        return None
    try:
        sents = ZHPATTERN.findall(text)
    except TypeError as exc:
        LOGGER.error(" %s " % exc)
        return None
        raise exc

    sents = [elm.strip() for elm in sents if elm.strip()]

    return sents
