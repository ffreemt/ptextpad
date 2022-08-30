"""Refer to Martin Fritzpatrick/pythonguis.

in fn add
    def emit(**kwargs):
        if progress_callback is not None:
            progress_callback.emit(kwargs)

    emit(thread_ident=threading.get_ident(), max_step=0)

    emit(step=idx)

    emit(done=True)

in main
    worker = Worker(
        # self.execute_this_fn
        fn,
        *args,
        **kwargs,
    )
    # worker.sig.result.connect(self.print_output)
    # worker.sig.finished.connect(self.thread_complete)
    worker.sig.progress.connect(self.progress_fn)

    self.threadpool.start(worker)

    def progress_fn(self, progress):
        ...
        # process progress (dict: thread_ident, max_step, step, done)
---
from PyQt5.Qt import QApplication

app = QApplication([])
window = MainWindow()
app.exec_()

, no-name-in-module
"""
# pylint: disable=too-few-public-methods
import sys
import traceback

from logzero import logger
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot


class WorkerSignals(QObject):
    """Define the signals available from a running worker thread.

    Supported signals:
        progress
            dict: thread_ident (int (threading.get_ident()) for strop_thead),
                    max_step, step, done
        result
            object data returned from processing, anything
        finished
            No data
        error
            tuple (exctype, value, traceback.format_exc() )
    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(dict)
    # progress: thread_ident, max_step, step, done, log_message
    # (for log tab self.plainTextEditLog.appendPlainText(msg))


class Worker(QRunnable):
    """Prep worker thread.

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn, *args, **kwargs):
        """Init."""
        # super(Worker, self).__init__()
        super().__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.sig = WorkerSignals()

        # blinker signal seems to have problems

        # Add the callback to our kwargs
        self.kwargs["progress_callback"] = self.sig.progress

        # data, key: thread_ident {result: done: aborted:}
        self.data = {}

    @pyqtSlot()
    def run(self):
        """Initialize the runner function with passed args, kwargs."""
        # Retrieve args/kwargs here; and fire processing using them
        try:
            logger.debug(" result = self.fn(*self.args, **self.kwargs) ")

            result = self.fn(*self.args, **self.kwargs)

            logger.debug("self.fn.__name__: %s", self.fn.__name__)
            logger.debug("type(result): %s", type(result))
        except Exception as exc:
            logger.error(" fn error: %s", exc)
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.sig.error.emit((exctype, value, traceback.format_exc()))
        else:
            logger.debug("self.sig.result.emit(result)")
            self.sig.result.emit(result)  # Return the result of the processing
        finally:
            logger.debug("self.sig.finished.emit() ")
            self.sig.finished.emit()  # Done
