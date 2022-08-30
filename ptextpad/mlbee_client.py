"""Wrap radio_mlbee_client with runnable.Worker."""
import threading

from icecream import ic
from logzero import logger
from radio_mlbee_client import radio_mlbee_client


def mlbee_client(*args, progress_callback=None, **kwargs):
    """Wrap radio_mlbee_client with progress_callback.

    For runnable.Worker (signal: progress = pyqtSignal(dict),
    refer to ptextpad.runnable.WorkerSignals.
    """
    logger.debug("mlbee_client")

    # progress_callback set to Worker.sig.progress in runnable
    # if progress_callback is not None:
    def emit(**kw):
        if progress_callback is not None:
            progress_callback.emit(kw)

    thread_ident = threading.get_ident()

    _ = """
    progress_callback.emit(
        {
            "thread_ident": _,
            "max_step": 0,
        }
    )
    # """

    logger.debug("thread_ident: %s", thread_ident)
    emit(**{"thread_ident": thread_ident, "max_step": 0})
    try:
        _ = "diggin...radio_mlbee_client(*args, **kwargs)"
        logger.debug(_)

        # self.log_message(ic.format(_))
        emit(log_message=ic.format(_))
        logger.debug(" emit(log_message=ic.format(_)) ")

        res = radio_mlbee_client(*args, **kwargs)

        _ = "done radio_mlbee_client(*args)"
        logger.debug(_)

        # self.log_message(ic.format(_))
        emit(log_message=ic.format(_))
    except InterruptedError:
        _ = "interrupted radio_mlbee_client(*args, **kwargs)"
        logger.error(_)
        emit(**{"aborted": thread_ident})

        # self.log_message(ic.format(_))
        emit(log_message=ic.format(_))
    except Exception as exc:
        logger.error(exc)
        _ = str(exc)

        # self.log_message(ic.format(_))
        emit(log_message=ic.format(_))
    else:
        return res
    finally:
        emit(**{"done": thread_ident})
        _ = "emit done"
        logger.debug(_)

        # self.log_message(ic.format(_))
        emit(log_message=ic.format(_))

    return None
