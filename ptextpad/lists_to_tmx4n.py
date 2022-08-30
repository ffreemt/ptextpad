# coding: utf-8
"""
lists to tmx
based on lxml.etree
"""

import logging

import lxml.etree as et
import tqdm

from .tqdmlogginghandler import TqdmLoggingHandler

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

LOGGER.addHandler(TqdmLoggingHandler())


def lists_to_tmx(
    srclist,
    tgtlist,
    srclang="en-US",
    tgtlang="zh-CN",
    encoding=None,
    method="xml",
    xml_declaration=True,
    pretty_print=True,
    doctype='<!DOCTYPE tmx SYSTEM "tmx14a.dtd">',
):
    """Log.

     4n for neualigner, remove tqdm if it causes problem in cx_freeze packing

     lists_to_tmx(srclist, tgtlist, srclang='en-US',
     tgtlang='zh-CN',
     encoding=None, method="xml", xml_declaration=True,
     pretty_print=False, doctype='<!DOCTYPE tmx SYSTEM "tmx14a.dtd">')

     return: bytes

     et.tostring(tostring(element_or_tree, encoding=None, method="xml",
              xml_declaration=None, pretty_print=False, with_tail=True,
              standalone=None, doctype=None,
              exclusive=False, with_comments=True, inclusive_ns_prefixes=None)
     wite out with:
     with open('test2tu.tmx','w') as fh:
    .....:     fh.write(tmx.decode())
    """
    if len(srclist) != len(tgtlist):
        LOGGER.warning(" len(srclist) != len(tgtlist), return None...")
        return None

    root = et.Element("tmx", attrib={"version": "1.4"})

    # header =  # gen header
    et.SubElement(root, "header", attrib={"amdinlang": srclang, "srclang": srclang})

    body = et.SubElement(root, "body")

    # tuv_en = et.SubElement(tu, "tuv", xml:lang="en")  # 'xml:lang' gets error
    # tuv_zh = et.SubElement(tu, "tuv", xml:lang="zh")

    len0 = min(len(srclist), len(tgtlist))
    for itrange in tqdm.trange(len0):
        tu = et.SubElement(body, "tu")
        tuv_en = et.SubElement(tu, "tuv", attrib={"lang": srclang})
        tuv_zh = et.SubElement(tu, "tuv", attrib={"lang": tgtlang})
        # attach tuv to tree
        et.SubElement(tuv_en, "seg").text = srclist[itrange]  # seg_en =
        et.SubElement(tuv_zh, "seg").text = tgtlist[itrange]  # seg_zh =

    tree = et.ElementTree(root)
    treestr = et.tostring(
        tree,
        encoding="utf-8",
        pretty_print=pretty_print,
        xml_declaration=xml_declaration,
        doctype=doctype,
    )
    return treestr.decode()

    # return et.tostring(
    #             tree, encoding='utf-8', pretty_print=pretty_print,
    #             xml_declaration=xml_declaration, doctype=doctype)
