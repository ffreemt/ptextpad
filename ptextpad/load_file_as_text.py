# coding: utf8
"""
Load text/epub/docx/html/htm/xhtml/xml/tmx/zip file as text.

Use load_text (*.txt), epub to text (*.epub), docx to text (docx to txt).
"""
import os
import sys

from clapse_text import clapse_text
from docx_to_txt import docx_to_txt
from epub_to_txt import epub_to_txt
from html2txt import html2txt
from load_zipped import load_zipped
from logzero import logger
from pdf_to_text_h import pdf_to_text
from srt_to_txt import srt_to_txt
from srtass_to_txt import srtass_to_txt
from xml_to_txt import xml_to_txt

from .detect_file import detect_file
from .load_text import load_text

# logger = logging.getLogger(__name__)
# logger.addHandler(logging.NullHandler())


def load_file_as_text(filepath):  # noqa: C901
    """
    Load text/epub/docx/html/htm/xhtml/xml/tmx/zip file as text.

    :in: filepath
    :out: str

    """
    if (sys.version_info.major == 3) and (not isinstance(filepath, str)):
        logger.warning(" Require a filepath (str), returning ''.")
        logger.info("%s, type: %s", filepath, type(filepath))
        # for pyqt5 QFileDialog.getOpenFileName
        return ""

    filepath = filepath.strip()
    text = ""

    if not filepath:
        logger.warning(" Filename empty, return '' ")
        return ""
    elif not os.path.exists(filepath):
        logger.warning(" File %s does not exist, return ''.", filepath.strip())  # noqa
        return ""

    if filepath.endswith(".txt"):
        try:
            text = load_text(filepath)

        except Exception as exc:
            logger.warning(" Load %s error: %s. Return str(exc).", filepath, exc)
            return str(exc)

    elif filepath.endswith(".epub"):
        try:
            text = epub_to_txt(filepath)

        except Exception as exc:
            logger.warning(" Load %s error: %s. Return ''.", filepath, exc)
            return ""

    elif filepath.endswith(".docx"):
        try:
            text = docx_to_txt(filepath)

        except Exception as exc:
            logger.warning(" Load %s error: %s. Return ''.", filepath, exc)
            return ""

    # filepath.endswith(".htm") or filepath.endswith(".html") or filepath.endswith(".xhtml")
    elif filepath.endswith(".htm"):
        try:
            _ = detect_file(filepath)
        except Exception as exc:
            logger.error(exc)
            raise
            
        try:
            with open(filepath, encoding=_, errors="ignore") as fha:
                text = html2txt(fha.read())
        except Exception as exc:
            logger.warning(" Load %s error: %s. Return ''.", filepath, exc)
            return ""

    elif filepath.endswith(".xml") or filepath.endswith(".tmx"):
        try:
            text = xml_to_txt(filepath)

        except Exception as exc:
            logger.warning(" Load %s error: %s. Return ''.", filepath, exc)
            return ""

    elif filepath.endswith(".srt"):
        try:
            text = srt_to_txt(filepath)

        except Exception as exc:
            logger.warning(" Load %s error: %s. Return ''.", filepath, exc)
            return ""
    elif filepath.endswith(".ass"):
        try:
            text = srtass_to_txt(filepath)

        except Exception as exc:
            logger.warning(" Load %s error: %s. Return ''.", filepath, exc)
            return ""
    elif filepath.endswith(".zip"):
        try:
            text = load_zipped(filepath)

        except Exception as exc:
            logger.warning(" Load %s error: %s. Return ''.", filepath, exc)
            return ""
    elif filepath.endswith(".pdf"):
        try:
            # text = load_zipped(filepath)
            text1 = pdf_to_text(filepath)
            text = clapse_text(text1)
        except Exception as exc:
            logger.warning(" Load %s error: %s. Return ''.", filepath, exc)
            return ""
    else:
        logger.warning(
            "Unable to deduce %s file type from file extension %s, try to load as txt.",
            os.path.basename(filepath),
            os.path.splitext(filepath)[1],
        )
        try:
            text = load_text(filepath)

        except Exception as exc:
            logger.warning(" Load %s error: %s. Return str(exc).", filepath, exc)
            return str(exc)

    try:
        _ = text.strip()
    except Exception as exc:
        logger.warning("%s", exc)
        _ = str(exc)

    return _

    # other file extensions
    # try zipped
