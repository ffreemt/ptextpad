"""Get_anchor_set(list0):

set_anchor: Set an anchor on an nx3 list.

!! BUG BUG !! seems only used in set_anchor_extra_outputs for verification purpose
TODO: need to rewrite (refer to set_anchor_extra_outputs.py)
"""
import logging

from .get_anchor_set import get_anchor_set
from .zip_longest_middle import zip_longest_middle

# from nose.tools import (eq_, with_setup)


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def set_anchor(list0, lpos, rpos, merit=1):
    """Set an anchor in list0 at lpos, rpos."""
    try:
        colno = len(list0[0])
    except (NameError, IndexError) as exc:
        LOGGER.critical(" exc: %s ", exc)
        return None

    if colno < 3:
        LOGGER.warning(" merit col not available, exiting...")
        return None

    # list0

    # refer to pyqt\aligner\set_anchors_pilot.py
    list1 = list0[:]

    anchor_list = get_anchor_set(list1)

    # seq1a = [elm[0] for elm in aligned_seqs]
    # seq2a = [elm[1] for elm in aligned_seqs]
    seq1a = [elm[0] for elm in list1]
    seq2a = [elm[1] for elm in list1]
    merit11 = [elm[2] if isinstance(elm[2], (int, float)) else "" for elm in list1]

    if not anchor_list:  # empty anchor_list ust insert lpos rpos
        # check lpos and rpos validility
        listlen = len(list1)
        if lpos < 0 or lpos > listlen - 1:
            return list1

        if rpos < 0 or rpos > listlen - 1:
            return list1

        # remove possible '' first
        # seq1aupper = [elm for elm in seq1a[:lpos] if elm.strip()]
        # seq2aupper = [elm for elm in seq2a[:rpos] if elm.strip()]

        seq1aupper = [elm for elm in seq1a[:lpos] if str(elm)]
        seq2aupper = [elm for elm in seq2a[:rpos] if str(elm)]

        seq1alower = [elm for elm in seq1a[lpos:] if str(elm).strip()]
        seq2alower = [elm for elm in seq2a[rpos:] if str(elm).strip()]

        tmpzip1 = list(zip_longest_middle(seq1aupper, seq2aupper, fillvalue=""))
        tmpzip2 = list(zip_longest_middle(seq1alower, seq2alower, fillvalue=""))

        list2 = [
            list(elm) + [merit11[ith] if isinstance(merit11[ith], (int, float)) else ""]
            for ith, elm in enumerate(tmpzip1)
        ] + [
            list(elm) + [merit11[ith] if isinstance(merit11[ith], (int, float)) else ""]
            for ith, elm in enumerate(tmpzip2)
        ]
        list2[len(tmpzip1)][2] = merit  # set merit11 to merit

        return list2

    # non empty anchor_list
    for elm in anchor_list:
        if lpos <= elm:
            break
    linterval = elm
    for elm in anchor_list:
        if rpos <= elm:
            break
    rinterval = elm

    anchor_list0 = anchor_list[:]
    merit0 = merit11[:]

    # refer to set_anchors_pilot.py
    if (
        lpos == linterval and rpos == rinterval and lpos == rpos
    ):  # lpos, rpos on the anchor, remove anchor
        merit0 = merit0[:lpos] + merit0[lpos + 1 :]
        anchor_list0.remove(lpos)
        anchor_list0 = [
            elm - (1 if elm > lpos else 0) for elm in anchor_list0
        ]  # shift 1 for elm>lpos
        # print('anchor_list0==[i for i, elm in enumerate(merit0) if elm]:',anchor_list0==[i for i, elm in enumerate(merit0) if elm])
        # print("anchor removed ")
        LOGGER.debug("anchor removed ")
        list1 = list0[:]
        list1[lpos][2] = merit
        return list1
    elif lpos == linterval or rpos == rinterval or linterval != rinterval:  # do nothing
        if lpos == linterval:
            LOGGER.debug("    lpos %s, anchor: %s" % (lpos, linterval))
        if rpos == rinterval:
            LOGGER.debug("    rpos %s, anchor: %s" % (rpos, rinterval))
        if linterval != rinterval:
            LOGGER.debug(
                "    not in the same interval: lpos %s, anchor %s; rpos %s, anchor %s"
                % (lpos, linterval, rpos, rinterval)
            )
        LOGGER.debug(
            "  the anchor set conflicts with previous anchor(s), reset the anchor(s) first. exiting..."
        )
        # SystemExit()
        # print("after SystemExit")
        # sys.exit(0)  # shows "An exception has occurred...", replace with return in function #print("    atfer sys.exit(0)")
        # os._exit(1)  # quits ipython
        # print("    os._exit(0)")
        return list1
    else:  # insert an anchor
        LOGGER.debug(
            "lpos %s, linterval, %s, rpos %s, rinterval, %s"
            % (lpos, linterval, rpos, rinterval)
        )
        if lpos < anchor_list0[0] or rpos < anchor_list0[0]:  # head
            LOGGER.debug("  lpos<linterval or rpos<rinterval: special case head")
            """ lpos = rpos = 0 """

            seq1aupper = [elm for elm in seq1a[:lpos] if str(elm)]
            seq2aupper = [elm for elm in seq2a[:rpos] if str(elm)]

            seq1alower = [elm for elm in seq1a[lpos:linterval] if str(elm).strip()]
            seq2alower = [elm for elm in seq2a[rpos:rinterval] if str(elm).strip()]

            tmpzip1 = list(zip_longest_middle(seq1aupper, seq2aupper, fillvalue=""))
            tmpzip2 = list(zip_longest_middle(seq1alower, seq2alower, fillvalue=""))

            # tmpzip1 = list(zip_longest_middle(seq1a[:lpos], seq2a[:rpos], fillvalue=''))
            # tmpzip2 = list(zip_longest_middle(seq1a[lpos:linterval], seq2a[rpos:rinterval], fillvalue=''))

            tmpseq1 = (
                [elm[0] for elm in tmpzip1]
                + [elm[0] for elm in tmpzip2]
                + seq1a[linterval:]
            )
            tmpseq2 = (
                [elm[1] for elm in tmpzip1]
                + [elm[1] for elm in tmpzip2]
                + seq2a[rinterval:]
            )

            tmpmerit0 = [""] * len(tmpzip1 + tmpzip2)
            merit0 = tmpmerit0 + merit0[linterval:]
            merit0[len(tmpzip1)] = 1.0

        elif lpos > anchor_list0[-1] or rpos > anchor_list0[-1]:  # tail
            LOGGER.debug("  lpos>linterval or rpos>rinterval: special case tail")
            """ lpos = rpos = 292 """

            # remove '' first
            seq1aupper = [elm for elm in seq1a[linterval + 1 : lpos] if str(elm)]
            seq2aupper = [elm for elm in seq2a[rinterval + 1 : rpos] if str(elm)]

            seq1alower = [elm for elm in seq1a[lpos:] if str(elm).strip()]
            seq2alower = [elm for elm in seq2a[rpos:] if str(elm).strip()]

            tmpzip1 = list(zip_longest_middle(seq1aupper, seq2aupper, fillvalue=""))
            tmpzip2 = list(zip_longest_middle(seq1alower, seq2alower, fillvalue=""))

            # tmpzip1 = list(zip_longest_middle(seq1a[linterval+1:lpos], seq2a[rinterval+1:rpos], fillvalue=''))
            # tmpzip2 = list(zip_longest_middle(seq1a[lpos:], seq2a[rpos:], fillvalue=''))

            tmpseq1 = (
                seq1a[: linterval + 1]
                + [elm[0] for elm in tmpzip1]
                + [elm[0] for elm in tmpzip2]
            )
            tmpseq2 = (
                seq2a[: rinterval + 1]
                + [elm[1] for elm in tmpzip1]
                + [elm[1] for elm in tmpzip2]
            )

            tmpmerit0 = [""] * len(tmpzip1 + tmpzip2)
            merit0 = merit0[: linterval + 1] + tmpmerit0
            merit0[linterval + 1 + len(tmpzip1)] = 1.0
        else:
            # LOGGER.debug("  normal case")
            LOGGER.debug("  normal case")

            # linterval: the smallest anchor that is greater than lpos
            # tmpn the previous anchor
            tmpn = anchor_list0[anchor_list0.index(linterval) - 1]

            # remove '' first
            seq1aupper = [elm for elm in seq1a[tmpn + 1 : lpos] if str(elm)]
            seq2aupper = [elm for elm in seq2a[tmpn + 1 : rpos] if str(elm)]

            seq1alower = [elm for elm in seq1a[lpos:linterval] if str(elm).strip()]
            seq2alower = [elm for elm in seq2a[rpos:rinterval] if str(elm).strip()]

            tmpzip1 = list(zip_longest_middle(seq1aupper, seq2aupper, fillvalue=""))
            tmpzip2 = list(zip_longest_middle(seq1alower, seq2alower, fillvalue=""))

            # tmpzip1 = list(zip_longest_middle(seq1a[tmpn+1:lpos], seq2a[tmpn+1:rpos], fillvalue=''))
            # tmpzip2 = list(zip_longest_middle(seq1a[lpos:linterval], seq2a[rpos:rinterval], fillvalue=''))

            tmpseq1 = (
                seq1a[: tmpn + 1]
                + [elm[0] for elm in tmpzip1]
                + [elm[0] for elm in tmpzip2]
                + seq1a[linterval:]
            )

            tmpseq2 = (
                seq2a[: tmpn + 1]
                + [elm[1] for elm in tmpzip1]
                + [elm[1] for elm in tmpzip2]
                + seq2a[rinterval:]
            )

            # fpiece_merit0 = merit0[:linterval+1]
            # bpiece_merit0 = merit0[tmpn:]

            tmpmerit0 = [""] * len(tmpzip1 + tmpzip2)
            merit0 = merit0[: tmpn + 1] + tmpmerit0 + merit0[linterval:]
            merit0[tmpn + 1 + len(tmpzip1)] = 1.0

        list1 = [[elm, tmpseq2[ith], merit0[ith]] for ith, elm in enumerate(tmpseq1)]

        return list1
