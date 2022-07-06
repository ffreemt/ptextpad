"""Pop up a Yes/No/Cancel message box.

QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel
"""
import sys

# ~ from PyQt4.QtGui import (QApplication, QMessageBox, QIcon)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox


def msg_popup(
    title="Untitled",
    text="",
    info="",
    details="",
    ytext="Yes",
    ntext="No",
    ctext="Cancel",
):
    """
    Pop up a Yes/No/Cancel message box.

    msg_popup(title="fixMe", text="fixMe", info="", details="", yestext='Yes', notext='No', canceltext='Cancel')

    msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel)  # noqa
    """
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setWindowIcon(QIcon("images/Anchor-48.png"))
    msg.setIcon(
        QMessageBox.Question
    )  # Question, Information, Warning, Critical  # noqa
    msg.setText(text)

    msg.setInformativeText(info)
    msg.setDetailedText(details)

    msg.setStandardButtons(
        QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel
    )  # noqa

    msg.setDefaultButton(QMessageBox.Yes)

    # http://stackoverflow.com/questions/35887523/qmessagebox-change-text-of-standard-button
    msg.button(QMessageBox.Yes).setText(ytext)
    msg.button(QMessageBox.No).setText(ntext)
    msg.button(QMessageBox.Cancel).setText(ctext)

    ret_val = msg.exec_()

    return ret_val


def main():
    """main."""
    mainapp = QApplication(sys.argv)
    while True:
        # ret_val = msg_popup('Title', 'text', 'Info1', 'Detail','yes', 'no', '取消')
        srclang = "chinese"
        tgtlang = "english"
        yestext = srclang + ":" + tgtlang
        notext = tgtlang + ":" + srclang
        ret_val = msg_popup("Title", "text", "Info1", ytext=yestext, ntext=notext)
        if ret_val == QMessageBox.Cancel:
            sys.exit()
    sys.exit(mainapp.exec_())


if __name__ == "__main__":
    main()
