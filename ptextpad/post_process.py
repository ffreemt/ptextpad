import logging
import re

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def post_process(text):
    """Post process for html2text."""

    if not isinstance(text, str):
        LOGGER.warning(" Input not a str, return None")
        return None

    # replace \n in [ ]
    # lst = re.findall('\[[^]]*?\]', text)
    lst = re.findall(r"\[[^]]*?\]", text)

    lst0 = [elm.replace("\n", " ") for elm in lst]
    for idx, elm in enumerate(lst):
        text = text.replace(lst[idx], lst0[idx])

    # replace &amp; with &
    text = text.replace("&amp;", "&")

    # \[This article appeared[\w\W]*?\]\([\w\W]*?\)
    # ^[#* !>]+([a-zA-Z[]) \1  # remove # * ! > as bullets
    # ^[#* !>]+([a-zA-Z[])
    # \[([^]]*?)\]\([\w\W]*?\) \1  # remove (...) in [...](...) ref links

    text = re.sub(
        r"\[This article appeared[\w\W]*?\]\([\w\W]*?\)", "", text
    )  # remove "This article..."

    # regex = re.compile(r'(^[#* !>]+([a-zA-Z[])|\[([^]]*?)\]\([\w\W]*?\))')
    # text = regex.sub(r'\2', text)

    text = re.sub(
        r"^[#* !>]+(.*?)$", r"\n\1\n", text, flags=re.MULTILINE
    )  # markdown bullets
    # text = re.sub(r'^[#* !>]+([a-zA-Z[])', r'\1', text, flags=re.MULTILINE)
    text = re.sub(r"!?\[([^]]*?)\]\([\w\W]*?\)[ ]?", r"\1", text)  # Markdown image

    # clapse paras
    text = re.sub("\n\n+", "_para_", text)
    text = text.replace("\n", " ")
    text = text.replace("_para_", "\n\n")

    return text
