"""Log progress."""
from time import sleep
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


# Print iterations progress
def logging_progress(
    iteration, total, steps=10, prefix="", suffix="", decimals=1, bar_length=10
):  # noqa
    """Call in a loop to create terminal progress bar.

    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals
        in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    # if total > steps:
    #     total = total // steps
    #     iteration = iteration // steps

    seg = 1
    if total > steps:
        seg = int(total / steps)

    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = "█" * filled_length + "-" * (bar_length - filled_length)

    # sys.stdout.wri te('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),  # noqa

    if iteration % seg == 0:
        # LOGGER.debug('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),  # noqa
        LOGGER.info("\r%s |%s| %s%s %s", prefix, bar, percents, "%", suffix)

    if iteration >= total:
        LOGGER.info("\r%s |%s| %s%s %s", prefix, bar, percents, "%", suffix)
    #     # sys.stdout.write('\n')
    #     LOGGER.debug('\n')
    # sys.stdout.flush()


def my_setup():
    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]:"
    fmt += "%(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)


if __name__ == "__main__":
    my_setup()

    # make a list
    # items = list(range(0, 57))
    items = list(range(0, 100))
    i = 0
    len_ = len(items)

    # Initial call to print 0% progress
    # printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length=50)  # noqa
    # logging_progress(i, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)# noqa
    for item in items:
        # Do stuff...
        sleep(0.1)
        # Update Progress Bar
        i += 1
        # printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)  # noqa

        # logging_progress(i, l, prefix = 'Progress:', suffix = 'Complete', bar_length =100)  # noqa
        # logging_progress(i, l, prefix = 'Progress:', suffix = 'Complete', bar_length =50)  # noqa
        # logging_progress(i, l, steps=100, prefix = 'Progress:', suffix = 'Complete', bar_length =50)  # noqa
        logging_progress(
            i, len_, steps=11, prefix="Progress:", suffix="Complete", bar_length=50
        )  # noqa
