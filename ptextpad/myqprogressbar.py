"""MyQProgressBar"""
import logging
import time

# ~ from PyQt4 import QtGui, QtCore, Qt
from PyQt5 import Qt, QtCore, QtGui, QtWidgets

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


# ~ class MyQProgressBar(QtGui.QProgressBar):
class MyQProgressBar(QtWidgets.QProgressBar):
    """MyQProgressBar"""

    def __init__(self, parent=None, qobj=None):
        super(MyQProgressBar, self).__init__(parent=None)

        if qobj is None:
            return
        # self.setWindowModality(QtCore.Qt.NonModal)

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("images/Anchor-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)
        self.setWindowOpacity(0.5)
        self.setWindowTitle("Processing...")
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.qobj = qobj

        self.qobj.total.connect(self.setMaximum)
        # self.qobj.total.connect(self.setrange)
        self.qobj.updated.connect(self.update)

        # self.thread.myclass.total.connect(self.setrange)
        # self.qobj.updated.connect(self.update)

        self.qobj.finished.connect(self.close)

    @QtCore.pyqtSlot(int)
    def update(self, i):
        """update"""
        self.setValue(i)
        if i % 100 == 0:
            LOGGER.debug(" updated received %s", i)

    @QtCore.pyqtSlot(int)
    def setrange(self, maxn):
        """Set range"""
        LOGGER.debug(" total signal received.")
        self.setRange(0, maxn)

        # self.thread.start()
