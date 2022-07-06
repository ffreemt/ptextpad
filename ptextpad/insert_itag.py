"""Insert ITAG ("|||")."""
# pylint: disable=invaid-name

from typing import Tuple, Optional, Union

itag_ = "|||"


def insert_itag(text: str, pos: Union[int, Tuple[int, int]], itag: Optional[str] = None) -> str:
    """Insert itag.

    Args:
        text: stuff to process
        pos: where to insert
        itag: default "|||"
    """
    if itag is None:
        itag = itag_

    if isinstance(pos, int):
        if pos > len(text):
            return text + itag
        if pos < 0:
            return itag_ + text

        return text[:pos] + itag + text[pos:]

    # 2-d pos, for QTextEdit and QPlainTextEdit
    pos1, pos2, *_ = pos

    if pos1 < 0:
        pos1 = 0
    if pos2 < 0:
        pos2 = 0

    lines = text.splitlines()

    # handle empty text
    if not lines:
        lines = [""]

    if pos1 >= len(lines):  # invalid
        pos1 = len(lines) - 1

    # alter lines[pos1]
    lines[pos1] = insert_itag(lines[pos1], pos2, itag)

    # reassemble
    return "\n".join(lines[:pos1] + [lines[pos1]] + lines[pos1 + 1:])
