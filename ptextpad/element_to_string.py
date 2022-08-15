# encoding='utf8'

# [http://stackoverflow.com/questions/380603/how-do-i-get-the-whole-text-of-an-element-using-elementtree]

import lxml

# from lxml import etree

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# def get_deep_text( element ):  # ok in python3
def element_to_string(element):  # ok in python3
    if element is None:
        text = ""
        return ""

    # logger.debug("element etree.tostring[:100] {} ".format( etree.tostring(element)[:100]))
    # print("element etree.tostring[:100] {} ".format( etree.tostring(element)[:100]))

    if not (
        type(element) == lxml.etree._Element or type(element) == lxml.html.HtmlElement
    ):
        logger.warning(
            "Input: {} is not of the type lxml.etree._Element or lxml.html.HtmlElement, returning None... ".format(
                element
            )
        )
        # logger.warning(" Input_ is not of the type lxml.etree._Element, returning None... ")
        return None

    text = element.text or ""
    for subelement in element:
        # text += get_deep_text( subelement )
        if subelement is not None:
            # text += element_to_string( subelement )
            try:
                text += element_to_string(subelement) + " "
            except Exception:
                pass  # crude way to handle <!-- <bar> -->
        # text += element_to_string( subelement )
    if element.tail:
        text += element.tail
        # text += element.tail+' '
        # text += element.tail+' ' or ''

    return text.replace("\xa0", " ")  # rid of \xa0 nbsp
