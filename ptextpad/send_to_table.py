"""Refactor from send_to_table in neualigner.py"""
import logging

# ~ from PyQt4 import QtCore
from PyQt5 import QtCore
from sep_chinese import sep_chinese

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class Worker(QtCore.QObject):
    """Worker."""

    def __init__(self, page):
        """Init."""
        super(Worker, self).__init__()
        self.page = page

    workRequested = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    tabdata_ready = QtCore.pyqtSignal(list)
    # relay=pyqtSignal(int)

    def request_work(self):
        """request_work."""
        self.workRequested.emit()
        LOGGER.debug(" workRequested.emitted ")

    def send_to_table(self):
        """Set fetch_url.page"""

        LOGGER.debug(" send_to_table started ")
        if not self.page.strip():
            return None

        tabdata1 = sep_chinese(self.page.strip())  # nx2 list

        # attache the last col
        tabdata1 = [elm + [""] for elm in tabdata1]

        # self.set_anchors(tabdata1)  # process: QThread?

        # self.anchortab_dirty = True

        # self.actionAnchor.setEnabled(True)

        # self.fetch_url.close()

        self.tabdata_ready.emit(tabdata1)
        self.finished.emit()
