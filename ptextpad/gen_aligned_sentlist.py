# coding: utf-8
"""
gen_aligned_sentlist(nx3 list, srclang=srclang, tgtlang=tgtlang)

    uses align_text.py

    output: nx3 list

"""

import logging
from copy import deepcopy

from .align_text import align_text
from .get_anchor_set import get_anchor_set
from .load_text import load_text

# from nose.tools import eq_, with_setup

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def gen_aligned_sentlist(
    list0, srclang="english", tgtlang="chinese", ratio_diff=1
):  # noqa
    """Generate an nx3 list of aligned sents, based on nx3 list0 anchored paras.

    output: nx3 list

    test file D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\splitbutton\aligned\news_anchored_paras_bk.txt
    """  # noqa
    inlist = deepcopy(list0)

    # from pprint import pprint
    # pprint(list0)
    # pprint(inlist)
    anchor_set = get_anchor_set(inlist)

    # LOGGER.debug(" anchor_set %s", anchor_set)

    # srcsepch = ' '
    # tgtsepch = ' '
    # if srclang == 'chinese':        # srcsepch = ''
    # if tgtlang == 'chinese':        # tgtsepch = ''

    anchor0 = -1

    outlist = []

    LOGGER.debug("anchor set: %s", anchor_set)

    for anchor in anchor_set:

        LOGGER.debug(" anchor %s", anchor)
        srctextlist = [elm[0] for elm in inlist[anchor0 + 1 : anchor]]
        tgttextlist = [elm[1] for elm in inlist[anchor0 + 1 : anchor]]

        srctext = ""
        for elm in srctextlist:
            if elm.strip():
                srctext += elm.strip() + "\n"
        tgttext = ""
        for elm in tgttextlist:
            if elm.strip():
                tgttext += elm.strip() + "\n"

        LOGGER.debug(" srctext %s, tgttext %s", srctext, tgttext)

        try:  # FIXME
            aligned_sents = align_text(
                srctext, tgttext, srclang, tgtlang, ratio_diff=ratio_diff
            )  # noqa
        except Exception as exc:
            LOGGER.error(exc)
            continue

        # LOGGER.debug(" aligned_sents %s", aligned_sents)

        if aligned_sents is not None:
            for elm in aligned_sents:
                outlist.append([elm[0], elm[1], ""])

        # gen aligned pairs for anchor itself
        aligned_sents = align_text(
            inlist[anchor][0],
            inlist[anchor][1],
            srclang,
            tgtlang,
            ratio_diff=ratio_diff,
        )  # noqa

        if len(aligned_sents) > 0:
            elm = aligned_sents[0]

            outlist.append(
                [elm[0], elm[1], inlist[anchor][2]]
            )  # set merit for the first sent in the anchor para  # noqa
        else:
            LOGGER.debug(" *** debug >>>")
            LOGGER.debug(
                " empty output from aligned_sents = align_text(inlist[anchor][0], inlist[anchor][1], srclang, tgtlang, ratio_diff=ratio_diff) "
            )  # noqa
            LOGGER.debug(" anchor: %s", anchor)
            LOGGER.debug(
                "inlist[anchor][0], inlist[anchor][1], srclang, tgtlang, ratio_diff=ratio_diff: %s, %s, %s, %s, %s",
                inlist[anchor][0],
                inlist[anchor][1],
                srclang,
                tgtlang,
                ratio_diff,
            )  # noqa
            LOGGER.debug(" <<< debug ***")

        if len(aligned_sents) > 1:
            for elm in aligned_sents[1:]:
                outlist.append([elm[0], elm[1], ""])

        anchor0 = anchor  # for the next anchor

    # possible tail
    if anchor0 < len(inlist) - 1:  # anchor0 + 1 <= len(inlist) - 1
        srctextlist = [elm[0] for elm in inlist[anchor0 + 1 :]]
        tgttextlist = [elm[1] for elm in inlist[anchor0 + 1 :]]

        srctext = ""
        for elm in srctextlist:
            if elm.strip():
                srctext += elm.strip() + "\n"
        tgttext = ""
        for elm in tgttextlist:
            if elm.strip():
                tgttext += elm.strip() + "\n"

        # gen aligned pairs
        aligned_sents = align_text(
            srctext, tgttext, srclang, tgtlang, ratio_diff=ratio_diff
        )
        for elm in aligned_sents:
            outlist.append([elm[0], elm[1], ""])

    return outlist


def my_setup():
    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


# nosetests --nologcapture
# @with_setup(my_setup)
def test_news():
    """Test news.

    **>>>**      test_news news_anchored_paras_bk.txt

    **<<<**

    """
    # filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\splitbutton\aligned\news_anchored_paras_bk.txt"
    filepath = "data/news_anchored_paras_bk.txt"

    text = load_text(filepath)
    lines = text.split("\n")
    lines = [elm for elm in lines if elm]

    inlist = [[elm0.strip() for elm0 in elm.split("\t", 2)] for elm in lines]

    srclang = "english"
    tgtlang = "chinese"
    outlist = gen_aligned_sentlist(inlist, srclang, tgtlang)

    assert len(outlist) == 5

    assert outlist[2][2] == "1.0"


# @with_setup(my_setup)
def test_news_ratio_diff03():
    """Test news_ratio.

    **>>>**      test_news_radtio_diff0 news_anchored_paras_bk.txt

    **<<<**

    """
    filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\splitbutton\aligned\news_anchored_paras_bk.txt"
    filepath = r"data/news_anchored_paras_bk.txt"

    text = load_text(filepath)
    lines = text.split("\n")
    lines = [elm for elm in lines if elm]

    inlist = [[elm0.strip() for elm0 in elm.split("\t", 2)] for elm in lines]

    srclang = "english"
    tgtlang = "chinese"
    ratio_diff = 0.3
    outlist = gen_aligned_sentlist(inlist, srclang, tgtlang, ratio_diff=ratio_diff)

    assert len(outlist) == 6

    assert outlist[3][2] == "1.0"


# @with_setup(my_setup)
def test_realdata_radtio_diff04():
    """Test realdata_radtio_diff04.

    **>>>**      test_realdata_radtio_diff04

    **<<<**

    """
    list1 = [
        ["China Is Here for Peace", "中国为和平而来", ""],
        ["-- Speech at the UN Peacekeeping Summit", "——在联合国维和峰会上的讲话", 1.0],
        [
            "Xi Jinping, President of the People's Republic of China",
            "中华人民共和国主席 习近平",
            "",
        ],
        ["New York, September 28, 2015", "（2015年9月28日，纽约）", 0.68],
        ["Your Excellency President Obama,", "尊敬的奥巴马总统，", ""],
        ["Your Excellency Secretary General Ban Ki-moon,", "尊敬的潘基文秘书长，", ""],
        ["Dear Colleagues,", "各位同事：", ""],
        [
            "I appreciate President Obama's initiative in convening this peacekeeping summit.",
            "我赞赏奥巴马总统倡议召开这次维和峰会。",
            0.65,
        ],
        [
            "Peace is the common aspiration and lofty goal shared by all mankind. It was for the purpose of securing peace that the UN peacekeeping operations came into being. Now as an important means of upholding world peace and security, these peacekeeping operations bring confidence to areas beset by conflict and hope to the local people who are its victims.",
            "和平是人类共同愿望和崇高目标。联合国维和行动为和平而生，为和平而存，成为维护世界和平与安全的重要途径。维和行动给冲突地区带去信心，让当地民众看到希望。",
            0.57,
        ],
        [
            "As we speak, people in many conflict-ridden places around the world are still suffering. They have a deep yearning for peace, higher hopes for the United Nations, and greater expectations for its peacekeeping operations. The following is what China stands for:",
            "当前，在世界很多地方，冲突地区民众依然饱受战乱之苦，对和平的渴望更加强烈，对联合国的期待更加殷切，对维和行动的期盼更加凸显。中国主张：",
            "",
        ],
    ]  # noqa

    tabdata = gen_aligned_sentlist(list1, "english", "chinese", 0.4)
    LOGGER.debug(" len of tabdata", len(tabdata))
