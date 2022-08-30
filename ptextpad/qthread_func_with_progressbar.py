"""Furnish a progressbar QThreadFuncWithQProgressBar."""
import logging
import sys

# from PyQt4 import QtCore, QtGui
from PyQt5 import QtCore, QtWidgets

# ~ import mypyqt.minifuncwrapper as mini
import ptextpad.minifuncwrapper as mini

# import mypyqt.myqprogressbar
from ptextpad.myqprogressbar import MyQProgressBar

from .csv_to_list import csv_to_list

# from nose.tools import eq_, with_setup


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class QThreadFuncWithQProgressBar(QtCore.QObject):
    """QThreaded function with QProgressBar."""

    outdata_ready = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(QThreadFuncWithQProgressBar, self).__init__(parent)
        # from myqclass import self
        self.parent = parent
        self.out = None
        self.qth = QtCore.QThread()
        LOGGER.debug(" __init__() ")

    def __call__(self, func, args):
        """call"""

        LOGGER.debug(" __call__ ")
        self.func = func
        self.args = args

        # Refer to test_func_wrapper in qthread in Sandbox\pyqt

        # myobj = mini.FuncWrapper(csv_to_list, (filepath,))
        self.myobj = mini.FuncWrapper(self.func, self.args)

        # self.qth = QtCore.QThread()
        self.myobj.moveToThread(self.qth)

        self.qth.started.connect(self.myobj)  # __call__/run_func

        self.myobj.finished.connect(self.on_func_finished)

        # progressWidget = MyQProgressBar(None, myclass)
        # self.progressWidget = mypyqt.myqprogressbar.MyQProgressBar(
        self.progressWidget = MyQProgressBar(self.parent, self.myobj)  # noqa

        self.qth.start()
        # LOGGER.debug(" QThreadFuncWithQProgressBar self.qth.start() ")

        # self.progressWidget.move(300, 300)
        self.progressWidget.resize(420, 30)

        self.progressWidget.show()

    def on_func_finished(self):
        """func finished running.

        quit thread
        emit outdata_ready
        """
        self.out = self.myobj.out
        self.qth.quit()

        if self.myobj.out is not None:
            self.outdata_ready.emit(self.myobj.out)

        # transfer data to outside, tap data (self.myobj.out) to func for further processing: qthobj.outdata_ready.connect(func)  # noqa

        LOGGER.debug(" on_func_finished/outdata_ready.emit ")

    def on_outdata_ready(self, out):
        """outdata_ready.

        Set out
        """
        self.out = self.myobj.out
        # self.out = out
        # LOGGER.debug(" Out data_ready: %s", len(self.out))


def setup_module(module):
    print("")  # this is to get a newline after the dots
    print("setup_module before anything in this file")


def teardown_module(module):
    print("teardown_module after everything in this file")


def my_setup():
    """my_setup."""

    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


def my_teardown():
    """Teardown"""


# @with_setup(my_setup, my_teardown)
def test_():
    """Test _+++."""

    # from mypyqt.qthread_func_with_progressbar import QThreadFuncWithQProgressBar  # noqa
    # exec(myreload("mypyqt.qthread_func_with_progressbar", "QThreadFuncWithQProgressBar"))  # noqa

    # app = QtGui.QApplication([])  # pyqt4
    app = QtWidgets.QApplication([])  # pyqt5

    filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\test_files\files_for_testing_load\aligned\rousseau-the-social-contract00.txt"  # noqa
    # filepath = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\test_files\files_for_testing_load\aligned\rousseau-the-social-contract.txt'  # noqa

    filepath = "data/Folding_Beijing_12.txt"

    func = csv_to_list
    args = (filepath,)

    qthread_func_w_progressbar = QThreadFuncWithQProgressBar()

    qthread_func_w_progressbar.outdata_ready.connect(
        qthread_func_w_progressbar.on_outdata_ready
    )  # noqa

    def receive_out(out):
        """Use signal to activate."""
        data = out[:]
        LOGGER.debug("further process out...")

        # eq_(1501, len(data))
        # assert len(data) >= 1501
        assert len(data) >= 1112

    qthread_func_w_progressbar.outdata_ready.connect(receive_out)

    qthread_func_w_progressbar(func, args)

    # out = qthread_func_w_progressbar.out
    # LOGGER.debug("out: %s", out)

    # eq_(1501, len(out))
    LOGGER.debug(" test output ")

    # LOGGER.debug(" %s ", var)

    # sys.exit(app.exec_())
    # appout = app.exec_()
    # LOGGER.debug(" appout: %s", appout)

    # eq_ test after this? ok
    # LOGGER.debug(" eq_ ...")
    # eq_(1501, len(qthread_func_w_progressbar.out))

    app.exec_()


if __name__ == "__main__":

    my_setup()
    test_()
    # my_teardown()
