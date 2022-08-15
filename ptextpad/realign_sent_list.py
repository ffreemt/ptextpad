"""Align two lists of sents (for use in neualigner's (re)Align action).

Check repeated entries in the target column; remove empty rows and align, auxch.join(), auxch = '' if lang=='chinese' else ' '  # noqa

seg_sent, align_sent)
"""
import logging
from nose.tools import eq_, with_setup

# from seg_sent import seg_sent
from .align_text import align_text


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def list_to_text(lst, lang):
    """
    Join list of sents.

    Remove repeated sents and empty rows.
    """
    if not lst:
        LOGGER.warning(" Input empty, return None.")
        return None

    auxch = "" if lang == "chinese" else " "

    LOGGER.debug("***>>>lst: %s, lang: %s", lst, lang)

    text = lst[0] + auxch

    # for idx, elm in enumerate(lst[1:]):
    for idx in range(1, len(lst)):
        # LOGGER.debug(" idx: %s", idx)
        if lst[idx] != lst[idx - 1]:  # remove identical rows
            temp = lst[idx].strip()
            if temp:  # remove empty rows
                text += temp + auxch  # attach with auxch at the end  # noqa
            # LOGGER.debug("temp %s, text %s", temp, text)

    # text = text.strip()
    # return seg_sent(text, lang=lang)

    LOGGER.debug("***>>>text: %s", text)

    return text.strip()


def realign_sent_list(srclist, tgtlist, srclang="english", tgtlang="chinese"):
    """
    Align two lists of sents (for use in neualigner's (re)Align action).

    realign_sent(srclist, tgtlist, srclang='english', tgtlang='chinese')
    :in: two lists of sents, srclang, tgtlang
    :out: srclist0, tgtlist0
    """

    LOGGER.debug(
        " srclist, tgtlist, srclang, tgtlang: %s : %s : %s : %s",
        srclist,
        tgtlist,
        srclang,
        tgtlang,
    )

    srctext = list_to_text(srclist, srclang)
    tgttext = list_to_text(tgtlist, tgtlang)

    LOGGER.debug(" srctext, tgttext: %s * %s", srctext, tgttext)

    # align_text0(srctext, tgttext, srclang='engilsh', tgtlang='chinese')
    srclist0 = []
    tgtlist0 = []
    list2 = align_text(srctext, tgttext, srclang=srclang, tgtlang=tgtlang)  # noqa
    for elm in list2:
        srclist0 += [elm[0]]
        tgtlist0 += [elm[1]]

    return srclist0, tgtlist0


def my_setup():
    """my_setup."""

    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


@with_setup(my_setup)
def test_289():
    """test_289 len(text) 289 +++."""
    lst = [
        "Five years ago, we lost He Zhihong, a peacekeeping policewoman in the UN peacekeeping mission in Haiti.",
        "She left a four-year-old son and elderly parents.",
        'She once wrote: "In this vast world, I may be just like a small feather.',
        'But even so, I want this feather to carry the wish for peace."',
    ]
    lang = "english"
    text = list_to_text(lst, lang)

    LOGGER.debug(" text:%s:, len: %s", text, len(text))

    out = len(text)
    eq_(289, out)


@with_setup(my_setup)
def test_realign_sent_list0():
    """test_realign_sent_list 0"""
    srclist = [
        "Xi Jinping, President of the People's Republic of China",
        "",
        "New York, September 28, 2015",
    ]
    tgtlist = ["中华人民共和国主席 习近平", "（2015年9月28日，纽约）", ""]
    srclang = "english"
    tgtlang = "chinese"
    exp = (
        [
            "Xi Jinping, President of the People's Republic of China New York, September 28, 2015"
        ],
        ["中华人民共和国主席 习近平（2015年9月28日，纽约）"],
    )
    out = realign_sent_list(srclist, tgtlist, srclang, tgtlang)
    eq_(exp, out)


@with_setup(my_setup)
def test_realign_sent_list1():
    """test_realign_sent_list 1"""
    srclist = [
        "It was for the purpose of securing peace that the UN peacekeeping operations came into being.",
        "",
        "Now as an important means of upholding world peace and security, these peacekeeping operations bring confidence to areas beset by conflict and hope to the local people who are its victims.",
    ]
    tgtlist = ["", "联合国维和行动为和平而生，为和平而存，成为维护世界和平与安全的重要途径。", "维和行动给冲突地区带去信心，让当地民众看到希望。"]
    srclang = "english"
    tgtlang = "chinese"
    exp = (
        [
            "It was for the purpose of securing peace that the UN peacekeeping operations came into being.",
            "Now as an important means of upholding world peace and security, these peacekeeping operations bring confidence to areas beset by conflict and hope to the local people who are its victims.",
        ],
        ["联合国维和行动为和平而生，为和平而存，成为维护世界和平与安全的重要途径。", "维和行动给冲突地区带去信心，让当地民众看到希望。"],
    )
    out = realign_sent_list(srclist, tgtlist, srclang, tgtlang)
    eq_(exp, out)
