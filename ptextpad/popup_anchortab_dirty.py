"""
popup_anchortab_dirty.

"""

import sys

# ~ from PyQt4.QtGui import (QApplication, QMessageBox, QIcon)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox

# from PyQt4 import QtWidget
# from PyQt4 import QtGui

# from PyQt4 import ( QtCore)

# from PyQt4 import QtGui
# import PyQt4.QtGui
# import PyQt4


# import PyQt5
# from PyQt5 import QtCore, QtGui, QtWidgets

# from QtWidgets import (QApplication)
# from PyQt5 import (QtWidgets.QApplication, QMessageBox, QIcon)

# from PyQt5.QtWidgets import QApplication, QMessageBox
# from PyQt5.QtGui import QIcon


def popup_anchortab_dirty():
    r"""
    Popup dialog if self.anchortab_dirty == True (modified but nore saved or sent to senttab).

    refer to D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\example_codes\parastab_yescancel_extra_arg.py
    """  # noqa
    # Create a basic message box
    # msg = QtWidgets.QMessageBox()
    msg = QMessageBox()
    msg.setWindowTitle("Wait...")
    msg.setWindowIcon(QIcon("images/Anchor-48.png"))
    msg.setIcon(QMessageBox.Information)
    msg.setText("You really want to clear the Anchor Tab and import new stuff?")  # noqa

    msg.setInformativeText(
        "The Anchor Tab has been modified but not exported nor sent to the Sent Tab."
    )  # noqa
    msg.setDetailedText(
        "If you click Yes, you will lose the stuff on the Anchor Tab. If you want to save the stuff on the Anchor, click No and then export or press the Alighn button to send the stuff to the Sent Tab."
    )  # NOQA

    # Add the standard buttons "Ok" and "Cancel"
    # msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)  # noqa  # noqa

    # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.setStandardButtons(
        QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel
    )  # noqa
    msg.setDefaultButton(QMessageBox.No)

    ret_val = msg.exec_()

    return ret_val


def main():
    """main."""
    mainapp = QApplication(sys.argv)
    while True:
        ret_val = popup_anchortab_dirty()
        if ret_val == QMessageBox.Cancel:
            sys.exit()

    sys.exit(mainapp.exec_())


if __name__ == "__main__":
    main()
