"""Run pyqt logging."""
# pylint: disable=bare-except, invalid-name, c-extension-no-member,

import logging
import sys

# from neualigner.testdebug import testdebug  # testing logging

# QtCore,
from PyQt5 import QtGui, QtWidgets

# ~ from PyQt4 import QtCore, QtGui

# Uncomment below for terminal log messages
FORMAT = "%(name)s - %(filename)s [line:%(lineno)d]"
FORMAT += "%(asctime)s:%(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

# disables connectionpool
logging.getLogger("requests.packages.urllib3.connectionpool").level = 30

# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')


class QPlainTextEditLogger(logging.Handler):
    """QPlainTextEditLogger(logging.Handler)"""

    def __init__(self, parent=None):
        super(QPlainTextEditLogger, self).__init__()
        # self.widget = QtGui.QPlainTextEdit(parent)
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


# class MyDialog(QtGui.QDialog, QPlainTextEditLogger):
# class MyDialog(QtGui.QMainWindow, QPlainTextEditLogger):
# ~ class MyDialog(QtGui.QPlainTextEdit, QPlainTextEditLogger):
class MyDialog(QtWidgets.QPlainTextEdit, QPlainTextEditLogger):
    """MyDialog(QtWidgets.QPlainTextEdit, QPlainTextEditLogger)"""

    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        logTextBox = QPlainTextEditLogger(self)
        # You can format what is printed to text box
        logTextBox.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(logTextBox)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)

        # self._button = QtGui.QPushButton(self)
        # self._button.setText('Test Me')

        # layout = QtGui.QVBoxLayout()
        # layout = QtGui.QVBoxLayout(self)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout = QtWidgets.QVBoxLayout(self)

        # Add the new logging box widget to the layout
        # layout.addWidget(logTextBox.widget)
        self.layout.addWidget(logTextBox.widget)
        # layout.addWidget(self._button)
        # self.setLayout(layout)
        self.setLayout(self.layout)

        # Connect signal to slot
        # self._button.clicked.connect(self.test)

    def test(self):  # pylint: disable=no-self-use
        """test"""
        logging.debug("damn, a bug")
        logging.info("something to remember")
        logging.warning("that's not right")
        logging.error("foobar")

        # testdebug()


if __name__ == "__main__":
    # may run this in python interactively
    from .stream_to_logger import StreamToLogger

    stderr_logger = logging.getLogger("STDERR")
    sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)
    # sl = ...; sys.stderr = sl

    app = None
    if not QtGui.QApplication.instance():
        app = QtGui.QApplication([])

    dlg = MyDialog()
    dlg.show()

    # dlg.raise_()
    try:
        raise Exception("Test to standard error")
    except Exception:
        pass

    if app:
        app.exec_()
