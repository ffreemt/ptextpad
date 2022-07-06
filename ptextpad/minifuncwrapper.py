import logging
import threading
import time

# ~ from PyQt4 import QtCore
from PyQt5 import QtCore

# import multiprocessing


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def func(i):
    print("func", i)


class FuncWrapper(QtCore.QObject):
    total = QtCore.pyqtSignal(int)
    updated = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()

    def __init__(self, func, args):
        super(FuncWrapper, self).__init__()
        self.func = func
        self.args = args
        self.out = None
        self.no_of_ticks = 0
        self.flag = True

    def tick(self):
        self.no_of_ticks = 0
        self.flag = True
        while self.flag:
            self.no_of_ticks += 1
            self.updated.emit(self.no_of_ticks)
            if self.no_of_ticks % 10 == 0:
                LOGGER.debug("updated emitted from tick %s", self.no_of_ticks)
            time.sleep(1)

    def sleep10(self):
        LOGGER.debug(" sleep10 started")
        time.sleep(10)
        self.finished.emit()
        LOGGER.debug(" sleep10: self.finished.emit() ")

    def run_func(self):
        """run_func"""
        self.out = self.func(*self.args)
        if self.out:
            LOGGER.debug(" %s out (len): %s", __name__, len(self.out))
        else:
            LOGGER.debug(" %s out is None", __name__)
        LOGGER.info(" Time elapsed: %s (sec)", self.no_of_ticks)
        self.finished.emit()
        self.flag = False

    def __call__(self):
        self.total.emit(0)
        # self.updated.emit(0)

        # mp = multiprocessing.Process(target=self.tick)
        # mp.start()

        mp = threading.Thread(target=self.tick)
        # mp.setDaemon(True)
        mp.daemon = True
        mp.start()

        # self.tick()

        # self.out = self.func(*self.args)

        # time.sleep(10)
        # th = threading.Thread(target=self.sleep10)

        th = threading.Thread(target=self.run_func)

        # th.setDaemon(True)
        th.daemon = True
        th.start()

        # self.finished.emit()

        # self.finished.connect(mp.terminate)


class FuncWrapper1(QtCore.QObject):
    total = QtCore.pyqtSignal(int)
    updated = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()

    def __init__(self):
        super(FuncWrapper, self).__init__()
        self.func = None
        self.args = None

    def __call__(self, func, args):
        self.func = func
        self.args = args
        self.total.emit(0)  # untimed, progress bar/dialog setMaximu(0)
        self.updated.emit(1)

        try:
            self.func(*self.args)
        except Exception as exc:
            LOGGER.debug(
                "self.func(*self.args), self.func=%s, error: %s", self.func, exc
            )

            LOGGER.warning(" Result obtained may not be legit, be warned.")

        self.finished.emit()
