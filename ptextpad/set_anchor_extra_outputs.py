"""Get_anchor_set(list0).

set_anchor: Set an anchor on an nx3 list.

based on set_anchor with minor modification
"""
# import logging

from logzero import logger

# from nose.tools import eq_, with_setup
from .get_anchor_set import get_anchor_set
from .set_anchor import set_anchor
from .zip_longest_middle import zip_longest_middle

# import numpy as np

# LOGGER = logging.getLogger(__name__)
# LOGGER.addHandler(logging.NullHandler())


def set_anchor_extra_outputs(list0, lpos, rpos, merit=1):
    """Set an anchor in list0 at lpos, rpos."""
    # logger.debug("\n **enter** set_anchor_extra_outputs ")

    # logger.debug("list0 lpos, rpos, merit: \n%s\n %s %s %s ", list0, lpos, rpos, merit)
    # logger.debug("list0 lpos, rpos, merit: \n%s\n %s %s %s ", np.array(list0), lpos, rpos, merit)

    try:
        colno = len(list0[0])
    except (NameError, IndexError) as exc:
        logger.critical(" exc: %s ", exc)
        return None

    if colno < 3:
        logger.warning(" merit col not available, exiting...")
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
        at_row = 0
        row_numbers = 0
        rows_to_add = []
        if lpos < 0 or lpos > listlen - 1:
            return list1, at_row, row_numbers, rows_to_add

        if rpos < 0 or rpos > listlen - 1:
            return list1, at_row, row_numbers, rows_to_add

        if lpos == rpos:  # modi
            at_row = lpos
            row_numbers = 1
            list1 = list0[:]
            list1[lpos][2] = merit
            rows_to_add = [list1[lpos]]
            return list1, at_row, row_numbers, rows_to_add

        # remove possible '' first
        # seq1aupper = [elm for elm in seq1a[:lpos] if elm.strip()]
        # seq2aupper = [elm for elm in seq2a[:rpos] if elm.strip()]

        seq1aupper = [elm for elm in seq1a[:lpos] if str(elm)]
        seq2aupper = [elm for elm in seq2a[:rpos] if str(elm)]

        seq1alower = [elm for elm in seq1a[lpos:] if str(elm).strip()]
        seq2alower = [elm for elm in seq2a[rpos:] if str(elm).strip()]

        tmpzip1 = list(zip_longest_middle(seq1aupper, seq2aupper, fillvalue=""))
        tmpzip2 = list(zip_longest_middle(seq1alower, seq2alower, fillvalue=""))

        list1 = [
            list(elm) + [merit11[ith] if isinstance(merit11[ith], (int, float)) else ""]
            for ith, elm in enumerate(tmpzip1)
        ] + [
            list(elm) + [merit11[ith] if isinstance(merit11[ith], (int, float)) else ""]
            for ith, elm in enumerate(tmpzip2)
        ]
        list1[len(tmpzip1)][2] = merit  # set merit11 to merit

        at_row = 0
        row_numbers = len(list0)
        rows_to_add = list1
        return list1, at_row, row_numbers, rows_to_add

    # non empty anchor_list
    # normal case (lpos<anchor_list0[-1] or rpos<anchor_list0[-1]:

    # !!! note this:
    # linterval is the smallest anchor that is larger or equal to lpos OR (special tail case) the last anchor
    # (similar for rpos)
    #
    # linterval (next anchor) >= lpos
    # except special tail case
    # where linter is the prev anchor
    # rinterval (next anchor) >= rpos
    #
    for elm in anchor_list:
        if elm >= lpos:
            # if lpos <= elm:
            break
    linterval = elm
    for elm in anchor_list:
        if elm >= rpos:
            # if rpos <= elm:
            break
    rinterval = elm

    # linterval >= lpos  !!
    # rinterval >= rpos  !!

    anchor_list0 = anchor_list[:]
    merit0 = merit11[:]

    if merit <= 0:
        if (
            lpos == linterval and rpos == rinterval and lpos == rpos
        ):  # <=0 debugged? *branch*1

            # if only one anchor left, do nothing
            if len(anchor_list) == 1:
                logger.debug(" The last anchor should not be removed. 玩野啊……")
                return list1, 0, 0, []

            merit0 = merit0[:lpos] + merit0[lpos + 1 :]
            anchor_list0.remove(lpos)
            anchor_list0 = [
                elm - (1 if elm > lpos else 0) for elm in anchor_list0
            ]  # shift 1 for elm>lpos

            logger.debug("anchor removed ")
            at_row = lpos
            row_numbers = 1
            list1 = list0[:]
            # list1[lpos][2] = merit  # update merit
            list1[lpos][2] = ""  # debugged
            rows_to_add = [list1[lpos]]
            return list1, at_row, row_numbers, rows_to_add
        else:
            return list1, 0, 0, []

    # >>> merit > 0 ==========

    logger.debug(
        "lpos %s, linterval %s, rpos %s, rinterval  %s, merit %s",
        lpos,
        linterval,
        rpos,
        rinterval,
        merit,
    )

    if linterval != rinterval:
        return list1, 0, 0, []

    # special case: only one anchor, linterval == rinterval
    # but lpos and rpos on the two sides of the anchor, do nothing
    if linterval == rinterval and (lpos - linterval) * (rpos - rinterval) < 0:
        return list1, 0, 0, []

    if lpos == linterval and rpos == rinterval:
        tmpvec = [list1[lpos]][:]  # copy
        tmpvec[0][2] = merit  # modify the merit
        return list1, lpos, 1, tmpvec

    # do nothing, note the previous op already filtered
    # out lpos == linterval and rpos == rinterval
    if lpos == linterval or rpos == rinterval:
        return list1, 0, 0, []

    # >>> merit > 0 and linterval == rinterval (lpos and rpos in the same interval)

    # if lpos < anchor_list0[0] or rpos < anchor_list0[0]:  # head
    if lpos < anchor_list0[0] or rpos < anchor_list0[0]:

        at_row = 0
        row_numbers = linterval  # linterval - at_row

        logger.debug("  lpos<linterval or rpos<rinterval: special case head")
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

    # elif lpos > anchor_list0[-1] or rpos > anchor_list0[-1]:  # tail
    elif lpos > anchor_list0[-1] or rpos > anchor_list0[-1] and merit > 0:  # debugged
        logger.debug("  lpos>linterval or rpos>rinterval: special case tail")
        """ lpos = rpos = 292 """

        at_row = linterval + 1  # linterval = rinterval
        row_numbers = (
            len(list0) - linterval - 1
        )  # len(list0) - at_row  (  [pos1, pos2): pos2 - pos1)

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
        logger.debug("  normal case")

        # linterval: the smallest anchor that is greater than lpos
        # tmpn the previous anchor
        tmpn = anchor_list0[anchor_list0.index(linterval) - 1]  # prev linterval

        at_row = tmpn + 1
        row_numbers = linterval - tmpn - 1  # linterval - at_row

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

    # tmpanchor_list = [i for i, elm in enumerate(merit0) if elm]

    list1 = [[elm, tmpseq2[ith], merit0[ith]] for ith, elm in enumerate(tmpseq1)]

    # row_numbers =
    rows_to_add = list1[at_row : at_row + len(tmpzip1 + tmpzip2)]

    return list1, at_row, row_numbers, rows_to_add
