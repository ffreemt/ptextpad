"""Load find_replace.ui."""
from pathlib import Path
from textwrap import dedent

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class QDialog_Ptextpad(QDialog):
    """Load find_replace.ui."""

    def __init__(self, parent=None):
        super().__init__(parent)

        _ = Path(__file__).resolve().parent
        _ = Path(_, "ui/qdialog-ptextpad.ui")
        print(_)
        assert _.is_file(), f"File [{_}] does not exist."
        loadUi(_, self)

        help = dedent(
            """
            Auto-anchoring relies on a network service (at huggingface) that make use of some machine learning algorithms. This typically lasts a few tens of seconds (10-20 seconds/10000 lines).

            Manual-anchoring: there is no need to set too many anchors -- one per 10-20 lines should be sufficient to obtain reasonably good result.
            """
        )
        # self.setWhatsThis("Help on FindReplaceDialog")
        self.setWhatsThis(help)

        _ = Path(__file__).parent
        _ = Path(_, "ui/images/3cols.png")
        assert _.is_file(), f"File [{_}] does not exit."
        self.setWindowIcon(QtGui.QIcon(_.as_posix()))
