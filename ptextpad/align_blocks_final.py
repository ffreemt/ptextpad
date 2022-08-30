"""Align blocks final.

Moved from para_gc.py
"""
from logzero import logger

from .amend_avec import amend_avec
from .para_gc import align_blocks_modi, check_avec


def align_blocks_final(s1, s2):
    len1 = len(s1)
    len2 = len(s2)
    avec = align_blocks_modi(s1, s2)
    cvec = check_avec(avec, len1 - 1, len2 - 1)
    avec0 = amend_avec(avec, cvec)

    # sanity check
    cvec0 = check_avec(avec0, len1 - 1, len2 - 1)
    if cvec0[0] or cvec0[1]:
        logger.warning(" s1={} s2={} ".format(s1, s2))
        logger.warning(
            " cvec0={} not empty, something is wrong... needs a fix. ".format(cvec0)
        )
        logger.warning("avec: %s, avec0: %s", avec, avec0)
        logger.warning("len1: %s, len2: %s", len1, len2)
        # SystemExit(1)

    return avec0
