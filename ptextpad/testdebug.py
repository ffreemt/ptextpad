# coding: utf8
"""
Tests debug.


"""

import logging

from nose.tools import eq_, with_setup

# from nose import with_setup

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def testdebug():
    """
    Test.
    """
    LOGGER.debug(" **debug...** ")
    LOGGER.info(" **info...** ")
    LOGGER.warning(" **warning...** ")
    LOGGER.critical(" **critical...** ")


"""
nosetests file.py
"""


def my_setup_function():
    """
    my_setup_function
    """
    pass


def my_teardown_function():
    """
    my_teardown_function
    """
    pass


@with_setup(my_setup_function, my_teardown_function)
def test_numbers_3_4():
    """
    test_numbers_3_4
    """
    # assert multiply(3,4) == 12
    # assert 3*4 == 12
    # eq_(3*4, 11)
    eq_(3 * 4, 12)


def test1_numbers_3_4():
    """
    test_numbers_3_4
    """
    # assert multiply(3,4) == 12
    # assert 3*4 == 12
    # eq_(3*4, 11)
    eq_(3 * 4, 12)
    eq_(3 * 4, 11)


def main():
    """
    Main.
    """
    format0 = "%(asctime)s : %(name)s - %(filename)s"
    format0 += "[line:%(lineno)d] : %(levelname)s : %(message)s"
    logging.basicConfig(format=format0)
    root = logging.getLogger()
    root.level = 10

    testdebug()


if __name__ == "__main__":
    main()
