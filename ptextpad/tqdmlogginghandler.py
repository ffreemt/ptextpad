"""Log.

https://stackoverflow.com/questions/38543506/change-logging-print-function-to-tqdm-write-so-logging-doesnt-interfere-wit

and then add this to the logging chain:
import time

log = logging.getLogger (__name__)
log.setLevel (logging.INFO)
log.addHandler (TqdmLoggingHandler ())
for i in tqdm.tqdm (range (100)):
    if i == 50:
        log.info ("Half-way there!")
    time.sleep (0.1)
"""
import logging
import tqdm


class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super(self.__class__, self).__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except Exception (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)
