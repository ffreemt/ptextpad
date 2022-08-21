r"""Align two texts.

def on_align/self.on_align
f[ .]on_align

def paras_to_senttab/self.paras_to_senttab
f[ .]paras_to_senttab

texts_to_anchored_paras.py

Modi copy of mat-dir\pyqt\neualigner-pyqt5\neualigner\__main__.py
Copy of cp ..\..\Sandbox\workpad\neualigner_py36pyqt5\neualigner.py neualigner\__main__.py

refer to run_test_set_anchor1.py, alignernb.py alignertabnb_ui2

TODO    auto-height
TODO    align/realign sents on and between anchors in senttab
TODO    QSetting (don't show something (os.startfile('readme.html') next time)
TODO    statusBar
TODO    pyqtdroid

DONE D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\neualigner003\neualigner.py

    removed selected rows
    set/reset all merit
    actionAlign
    [refer to self.actionAnchor.triggered.connect(self.files_to_anchortab)]
    actionExport_Sents
    actionExport_TMX
    1 ui, widens log
    2 anchor tab
        0.33 ==> color?
        anchor tab, 0=>''
        anchor tab, merit: click to change
    3 anchor tab
        3rd col hidden, shrink 1, 2 columns
    4 threading to display logging
    1 Done Export [use twofiles_trunk, list_to_csv]
    2 Done Set anchor fct/ui
    update_mytable2()
    gen_aligned_sentlist(nx3 list, srclang=srclang, tgtlang=tgtlang)

self.plainTextEditLog = QtWidgets.QPlainTextEdit(self.tab_4)
    self.plainTextEditLog.text.append()
"""
# pylint: disable=inconsistent-return-statements, too-many-statements, too-many-public-methods, unused-import, invalid-name, pointless-string-statement, too-many-instance-attributes, too-few-public-methods, line-too-long, no-name-in-module, too-many-lines, too-many-locals, unused-variable,

import logging
import os
import sys
from copy import deepcopy
from itertools import zip_longest
from pathlib import Path
from textwrap import dedent

import logzero
import numpy as np
from icecream import ic
from logzero import logger
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QElapsedTimer, QObject, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (  # noqa
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QProgressDialog,
    QSplashScreen,
)
from radio_mlbee_client import radio_mlbee_client
from set_loglevel import set_loglevel

from ptextpad import __version__
from ptextpad.fetch_url import FetchURL
from ptextpad.help_manual import help_manual
from ptextpad.load_text import load_text
from ptextpad.msg_popup import msg_popup
from ptextpad.popup_anchortab_dirty import popup_anchortab_dirty
from ptextpad.qthread_func_with_progressbar import QThreadFuncWithQProgressBar  # noqa

# from .send_to_table import Worker
from . import send_to_table
from .data_for_updating import (
    data_for_mergedown,
    data_for_mergeup,
    data_for_movedown,
    data_for_moveup,
    data_for_splitdouble,
)
from .detect_lang import detect_lang
from .gen_aligned_sentlist import gen_aligned_sentlist
from .insert_itag import insert_itag
from .list_to_csv import list_to_csv
from .lists_to_tmx4n import lists_to_tmx

# from load_text import load_text
from .load_file_as_text import load_file_as_text
from .logging_progress import logging_progress
from .realign_selected_rows import realign_selected_rows
from .remove_selected_rows import remove_selected_rows
from .runnable import Worker as Rworker
from .sep_chinese import sep_chinese

# from texts_to_anchored_paras import texts_to_anchored_paras
from .text_to_paras import text_to_paras
from .twofiles_trunk import twofiles_trunk
from .update_tablemodel import update_cell, update_layout
from .zip_longest_middle import zip_longest_middle

# from ptextpad.ui.neualigner_ui import Ui_MainWindow

# from csv_to_list import csv_to_list
# from excel_to_list import excel_to_list
# from tmx_to_list import tmx_to_list

# from select_last_selected_rows import select_last_selected_rows

# from reanchor_selected_rows import reanchor_selected_rows

# stream_to_logger
# logger = logging.getLogger(__name__)
# logger.addHandler(logging.NullHandler())

# set env var autoload to turn on
autoload = os.environ.get("AUTOLOAD")

logzero.loglevel(set_loglevel())
logger.info("os.environ.get('LOGLEVEL'): %s", os.environ.get("LOGLEVEL"))
logger.info("log level: %s", set_loglevel())
logger.debug("debug on: %s", set_loglevel())
logger.debug("autoload: %s", autoload)

# __version__ = "0.7.0"  # used in About box
# __version__ = "0.7.0a0"  # used in About box

# turn off uic.loadUi debug messages
uic.properties.logger.setLevel(logging.WARNING)
uic.uiparser.logger.setLevel(logging.WARNING)

# log tab: logtab.text.append(ic.format)
ic.configureOutput(prefix="ptextpad -> ", includeContext=1)


def _translate(context, text, disambig):
    """Translate."""
    # return QtGui.QApplication.translate(context, text, disambig)
    return QApplication.translate(context, text, disambig)


# refer to worker.py main.py
class Worker(QObject):  # [for files_to_anchortab]
    """Worker for QThread."""

    # def __init__(self, text1, text2, tgtlang):
    def __init__(self, text1, text2):
        """init."""
        # super(Worker, self).__init__()
        super().__init__()
        self.text1 = text1
        self.text2 = text2

        # self.tgtlang = tgtlang

    workRequested = pyqtSignal()
    finished = pyqtSignal()
    tabdata_ready = pyqtSignal(list)

    # @pyqtSlot()
    def request_work(self):
        """Emit workRequest for qthread.start."""
        self.workRequested.emit()
        logger.debug("***self.workRequested.emit()***")

    # from worker.py
    # @pyqtSlot()
    def get_tabdata(self):  # slot for thread (QThread)
        """Monitor."""
        # from .texts_to_anchored_paras import texts_to_anchored_paras

        logger.debug("*****radio_mlbee_client/texts_to_anchored_paras starts****")

        # tabdata = texts_to_anchored_paras(self.text1, self.text2, self.tgtlang)

        # tabdata = texts_to_anchored_paras(self.text1, self.text2)
        try:
            tabdata = radio_mlbee_client(self.text1, self.text2)
        except Exception as exc:
            logger.error(exc)
            tabdata = [[str(exc), "", ""]]

            # log tab self.plainTextEditLog
            _ = str(exc)
            self.plainTextEditLog.append(ic.format(_))

        # selftabdataloaded = True
        # time.sleep(1)  # can this prevent crash?
        self.tabdata_ready.emit(tabdata)
        logger.debug("self.tabdata_ready.emit(tabdata)")

        # time.sleep(1)  # can this prevent crash?
        self.finished.emit()


_ = """
class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()  # Harwani callFirstApp.pyw
        self.ui.setupUi(self)
# """


# class MyWindow(QMainWindow, Ui_MainWindow):
class MyWindow(QMainWindow):
    """Define mainwin."""

    srclang = ""
    tgtlang = ""

    def __init__(self, parent=None):
        """Init."""
        # QtGui.QWidget.__init__(self, parent)
        # super(MyWindow, self).__init__(parent)
        super().__init__(parent)

        # ui_file = Path(__file__).with_name("ui") / "neualigner.ui"
        ui_file = Path(__file__).with_name("ui") / "ptextpad.ui"

        # promted MyTable to self.tableView_0 1 2
        uic.loadUi(ui_file, self)

        # self.setupUi(self)  # Summerfield
        # self.updateUi()

        # self.tabdataloaded = False

        # self.runno = 0  # for self.tableView_2.myarray.remove(['', '', ''])
        # changed to use try: except ErrorValue: pass

        self.file1 = ""  # for gen filename trunk for output file names
        self.file2 = ""
        self.import_paras_filename = ""
        self.thread = QThread()
        self.lrowno = 0
        self.rrowno = 0
        self.merit = 0
        self.obj = QObject()
        self.fetch_url = None
        self.qth = None
        self.progressdialog = None

        # self.aligned_trunk = ''

        # if first time is from the web or cut and paste: home dir/cutnpaste.xyz
        self.aligned_trunk = twofiles_trunk(
            os.path.join(os.path.expanduser("~"), "aligned", "cutnpaste.txt")
        )  # noqa

        self.parafile = self.aligned_trunk + "_anchored_paras.txt"
        self.sentfile = self.aligned_trunk + ".txt"
        self.tmxfile = self.aligned_trunk + ".tmx"

        self.tgtlang = "zh"
        self.no_of_loadfiles = 0

        self.anchortab_dirty = False  # __init__
        # set True in set_anchors, set False in export_paras self.actionExport_Paras.triggered.connect(export_paras)  # noqa

        self.senttab_dirty = False

        self.anchorValid1 = False
        self.anchorValid2 = False
        self.anchorValid3 = False

        self.actionAnchor.setEnabled(True)
        self.actionAlign.setEnabled(False)

        # self.button = self.findChild(QtWidgets.QPushButton, 'printButton')
        # self.actionAnchor = self.findChild(
        # self.actionAnchor.setEnabled(True)

        # to be defined in ui
        # self.actionAlign = QtGui.QAction(MainWindow)
        # self.actionQexit.setShortcut(_translate("MainWindow", "Ctrl+X", None))  # noqa
        # self.actionAlign.triggered.connect(self.test)

        # self.actionMoveup.setShortcut(_translate("MainWindow", "Ctrl+Up", None))  # noqa

        # self.actionMoveup = QtGui.QAction(self)
        # self.actionMoveup.setShortcut(_translate("MainWindow", "Ctrl+M", None))  # noqa

        # self.actionDown
        # self.actionMergeUp
        # self.actionMergeUp

        self.setWindowTitle(f"Ptextpad {__version__}")

        # self.setWindowIcon(QIcon("ui/images/Anchor-48.png"))

        # by https://www.flaticon.com/authors/iyahicon
        _ = f"{Path(__file__).parent}/ui/images/3cols.png"
        if not Path(_).is_file():
            logger.warning("File [%s] not found", _)
        self.setWindowIcon(QIcon(_))

        # connect toolbar triggered() signal to slot
        # self.connect(self.actionPlus, QtCore.SIGNAL('triggered()'), self.plusmessage)  # works  # noqa

        # self.connect(self.actionPlus, QtCore.SIGNAL('triggered()'), self.mytable.delegate.plusmessage)  # noqa

        # self.connect(self.actionPlus, QtCore.SIGNAL('triggered()'), self.tableView_1.delegate.plusmessage)  # okok  # noqa
        # self.connect(self.actionPlus, QtCore.SIGNAL('triggered()'), self.tableView_2.delegate.plusmessage)  # noqa
        # self.connect(self.actionPlus, QtCore.SIGNAL('triggered()'), self.tableView_3.delegate.plusmessage)  # noqa

        # self.connect(self.actionPlus, QtCore.SIGNAL('triggered()'), self.tableView_1.test)  # okok  # noqa
        # self.connect(self.actionPlus, QtCore.SIGNAL('triggered()'), self.tableView_2.test)  # noqa
        # self.connect(self.actionPlus, QtCore.SIGNAL('triggered()'), self.tableView_3.test)  # noqa

        # self.connect(self.actionPlus, QtCore.SIGNAL('triggered()'), self.xxxx.delegate.plusmessage)  # noqa

        # connects
        # self.actionPlus.triggered.connect(lambda file: self.open(file=1))
        # self.actionPlus.triggered.connect(self.plainTextEdit.test)

        # self.actionImport.triggered.connect(self.plainTextEdit.test)

        # self.actionNew.triggered.connect(lambda file: self.open(file=1))

        self.actionFile1.triggered.connect(self.open)

        # open file 2
        self.actionFile2.triggered.connect(lambda: self.open(file=2))

        self.actionImport_URL_Xpath.triggered.connect(self.fetch_urlpop)

        # process file contents and send to the anchor tab
        # '''actionAnchor'''
        # self.actionAnchor.triggered.connect(self.files_to_anchortab)
        self.actionAnchor.triggered.connect(self.on_anchor)

        # self.actionAlign.triggered.connect(self.paras_to_senttab)
        self.actionAlign.triggered.connect(self.on_align)

        # QtCore.QObject.connect(self.ui.setAnchor, QtCore.SIGNAL('clicked()'), self.dispsum)  # noqa
        # '''setAnchorButton'''
        # self.setAnchorButton.clicked.connect(self.dispmsg)
        self.setAnchorButton.clicked.connect(self.update_mytable2)

        # instant display anchormsg
        self.lineEdit_lrow.textEdited.connect(self.dispmsg)
        self.lineEdit_rrow.textEdited.connect(self.dispmsg)
        self.lineEdit_merit.textEdited.connect(self.dispmsg)

        # self.actionAlign.triggered.connect(lambda: list_to_csv(self.tableView_2.myarray, self.parafile))  # noqa
        # testing splitting cell split_cell
        # self.actionAlign.triggered.connect(self.split_cell)

        # self.actionAlign.triggered.connect(self.test)  # ok

        # self.actionAlign.triggered.connect(self.moveup)
        self.actionMoveup.triggered.connect(self.moveup)

        self.actionMovedown.triggered.connect(self.movedown)

        self.actionMergedown.triggered.connect(self.mergedown)

        self.actionMergeup.triggered.connect(self.mergeup)

        # self.actionMoveup.triggered.connect(self.moveup)
        # self.actionMoveup.triggered.connect(self.test)

        # Break |||
        self.actionBreak.triggered.connect(self.splitdouble)

        # flip merit
        self.actionMerit_0_or_1.triggered.connect(self.flipmerit)

        # ########## here TODO ##########
        # set row numbers actionSet_Row_Numbers, bound to shortcut Space
        self.actionSet_Row_Numbers.triggered.connect(self.set_row_numbers)

        # manually set anchor bound to shortcut Return
        self.actionSet_Anchor.triggered.connect(self.manual_set_anchor)
        # self.actionSet_Anchor.triggered.connect(self.update_mytable2)

        # delete rows
        '''
        # def call_delete_rows(self):
            """CAll delete_rows."""
            # lambda self: delete_rows(self)
            # delete_rows(self)
        '''

        # self.actionDelete_rows.triggered.connect(call_delete_rows)
        self.actionDelete_rows.triggered.connect(self.delete_rows)

        # Help manual and about
        self.actionAbout.triggered.connect(self.help_about)
        # self.actionAbout.triggered.connect(self.plusmessage)
        self.actionManual.triggered.connect(help_manual)

        self.actionExport_Paras.triggered.connect(self.export_paras)
        self.actionExport_Sents.triggered.connect(self.export_sents)
        self.actionExport_TMX.triggered.connect(self.export_tmx)

        # not implemented yet
        # TODO Import_Paras not_implemented: paras/sents

        self.actionImport_Paras.triggered.connect(self.not_implemented)  # TODO
        # self.actionImport_Paras.triggered.connect(self.import_to_anchortab)

        self.actionImport_Csv.triggered.connect(self.not_implemented)  # TODO
        self.actionImport_TMX.triggered.connect(self.not_implemented)  # TODO

        # switch to log tab
        # self.tabWidget.setCurrentIndex(3)
        self.tabWidget.setCurrentIndex(0)
        # init ends

        if set_loglevel() <= 10 and autoload:  # dev mode/debug mode
            logger.debug("debug mode: load two files directly")

            # autoload data/en.txt zh.txt
            filec1 = "filec1"
            filec2 = "filec2"
            try:
                filec1 = load_text("data/en.txt")
                filec1 = load_text("data/Folding_Beijing_ch1-en.txt")
            except Exception as exc:
                logger.error('load_text("data/en.txt") error: %s', exc)
            try:
                filec2 = load_text("data/zh.txt")
                filec2 = load_text("data/Folding_Beijing_ch1-zh.txt")
            except Exception as exc:
                logger.error('load_text("data/zh.txt") error: %s', exc)

            self.tableView_1.tablemodel.layoutAboutToBeChanged.emit()
            self.tableView_1.tablemodel.arraydata = [[filec1, filec2, ""]]
            self.tableView_1.tablemodel.layoutChanged.emit()
            self.tableView_1.resizeRowsToContents()

            # anchor tab (tab2)
            lines1 = [_.strip() for _ in filec1.splitlines() if _.strip()]
            lines2 = [_.strip() for _ in filec2.splitlines() if _.strip()]
            _ = zip_longest_middle(lines1, lines2, fillvalue="")

            # add third col and convert to list
            _ = [*zip_longest(*zip(*_), [""], fillvalue="")]
            _ = np.array(_).tolist()

            self.tableView_2.tablemodel.layoutAboutToBeChanged.emit()
            self.tableView_2.tablemodel.arraydata = _
            self.tableView_2.tablemodel.layoutChanged.emit()
            self.tableView_2.resizeRowsToContents()

            self.anchortab_dirty = True

        self.init_dir = "."
        if Path("data").is_dir():
            self.init_dir = "data"
        elif Path("../data").is_dir():
            self.init_dir = "data"

        # startup message
        logger.info(
            """
            *******************************
              Welcome to Ptextpad %s!
              (formerly Neualigner)
            To turn on debug, set environ LOGLEVEL=10
            (e.g. in Windows: set LOGLEVEL=10 or
            in Linux and Mac: export LOGLEVEL=10)
            *******************************
            """,
            __version__,
        )
        _ = f"""
            *******************************
              Welcome to Ptextpad {__version__}!
              (formerly Neualigner)
              brought to you by mu@qq:41947782
            *******************************
            """
        self.log_message(_)

    def fetch_urlpop(self):
        """Fetch url."""
        # from  urlxpathtestmainwindow_ui import Ui_MainWindow  # ok
        # import  urlxpathtestmainwindow_ui.Ui_MainWindow  # not a package
        # from fetch_url import MyWindow

        try:
            self.fetch_url = FetchURL(self)
        except Exception as exc:
            _ = f" {exc} (to be fixed)"  # TODO
            QMessageBox.warning(self, "Hint", ic.format(_))
            return None
        # self.fetch_url.page: in fetch_url.py: goButton ==> fetch_xpath

        # self.fetch_url.pushButton_2.clicked.connect(self.send_to_table)
        self.fetch_url.show()
        # self.fetch_url.sendButton.clicked.connect(self.send_to_table)
        self.fetch_url.sendButton.clicked.connect(self.call_send_to_table)

    def call_send_to_table(self):
        """call_send_to_table"""
        self.progressdialog = QProgressDialog("Processing...", "Cancel", 0, 100)  # noqa
        self.progressdialog.setWindowTitle("Process text")
        # self.progressdialog.setWindowFlags(Qt.WindowStaysOnTopHint)  # always on top  # noqa

        # self.fetch_url.sendButton.clicked.connect(self.send_to_table)
        worker = send_to_table.Worker(
            self.fetch_url.page
        )  # import send_to_table worker  # noqa
        self.qth = QThread()
        worker.moveToThread(self.qth)

        # progressdialog = QProgessDialog()
        # progressDialog = QProgressDialog('Uploading %s ...' % file_path, # QString("Cancel"), 0, file_size)  # noqa
        # progressDialog.setWindowTitle('Upload status')

        self.qth.started.connect(worker.send_to_table)
        # worker.update.connect(worker.monitor_work)
        worker.finished.connect(self.on_finished)
        worker.tabdata_ready.connect(self.set_anchors)
        worker.workRequested.connect(self.on_start)

        # self.fetch_url.sendButton.clicked.connect(worker.request_work)

        worker.request_work()
        logger.debug(" send_to_table worker.request_work() ")

        # self.fetch_url.sendButton.clicked.connect(self.qth.start)

        # self.fetch_url.sendButton.clicked.connect(self.send_to_table)
        # send_to_table to Work class

    def on_start(self):
        """on_start"""
        # def on_start(parent):  # ?
        self.qth.start()
        self.progressdialog.setRange(0, 0)
        self.progressdialog.setValue(1)

    def monitor_work(self):
        """progressdialog"""
        pass

    def on_finished(self):
        """on finished"""
        self.progressdialog.setRange(0, 100)
        for elm in range(5):
            self.progressdialog.setValue(96 + elm)
        self.qth.quit()
        self.fetch_url.close()

    def send_to_table(self):
        """Send to anchor tab."""

        if not self.fetch_url.page.strip():
            return None

        # langid.set_languages()

        tabdata1 = sep_chinese(
            self.fetch_url.page.strip()
        )  # nx2 list # QThread()? convert sep_chinese to Class?  # noqa

        # attache the last col
        tabdata1 = [elm + [""] for elm in tabdata1]

        self.set_anchors(tabdata1)  # process: QThread?

        self.anchortab_dirty = True

        self.actionAnchor.setEnabled(True)

        self.fetch_url.close()

    def send_to_table1(self):
        """Set table 0,0 to fetch_url.page"""

        if not self.fetch_url.page.strip():
            return None

        # if len(self.tableView_1.tablemodel.arraydata) == 0:  # modi
        if not self.tableView_1.tablemodel.arraydata:
            self.tableView_1.tablemodel.layoutAboutToBeChanged.emit()
            self.tableView_1.tablemodel.arraydata = [["", "", ""]]
            self.tableView_1.tablemodel.layoutChanged.emit()

        index00 = self.tableView_1.tablemodel.createIndex(0, 0)
        self.tableView_1.tablemodel.arraydata[0][0] = self.fetch_url.page
        self.tableView_1.tablemodel.dataChanged.emit(index00, index00)
        # logger.debug("arraydata: %s", self.tablemodel.arraydata)

        self.fetch_url.close()

    def delete_rows(self):
        """Remove selected rows."""
        if self.tabWidget.currentIndex() == 0:  # text tab
            remove_selected_rows(self.tableView_1)
            logger.debug("Delete rows on anchortab")
        elif self.tabWidget.currentIndex() == 1:  # anchortab
            remove_selected_rows(self.tableView_2)
            logger.debug("Delete rows on anchortab")
        elif self.tabWidget.currentIndex() == 2:  # senttab
            remove_selected_rows(self.tableView_3)
            logger.debug("Delete rows on senttab")

    # Import
    def ximport_excel_to_anchortab(self):
        """Import pandas as pd."""
        # from excel_to_list import excel_to_list

        # refeer to def files_to_anchortab|def set_anchors
        # call self.set_anchors
        self.tabWidget.setCurrentIndex(1)

    # Export
    # self.actionExport_Paras.triggered.connect(lambda: list_to_csv(self.tableView_2.myarray, self.parafile))  # noqa
    def log_message(self, msg):
        """Send msg to log tab self.plainTextEditLog.text.append(msg)."""
        self.plainTextEditLog.appendPlainText(msg)

    def export_paras(self):
        """Export anchored paras."""
        # switch to log tab
        _ = ic.format("diggin...")
        self.log_message(_)

        try:
            self.tabWidget.setCurrentIndex(3)
            # list_to_csv(self.tableView_2.myarray, self.parafile)
            list_to_csv(self.tableView_2.tablemodel.arraydata, self.parafile)
            self.anchortab_dirty = False

            logger.info("\n\n Csv file written to %s \n\n", self.parafile)
            os.startfile(os.path.dirname(self.parafile))
            _ = f"Success: Csv file written to {self.parafile}"
            self.log_message(_)
        except Exception as exc:
            logger.error(exc)
            _ = ic.format(f"{exc} (to be fixed)")
            self.log_message(_)
            QMessageBox(self, "Hint", _)

    def export_sents(self):
        """Export sents."""
        # switch to log tab
        _ = ic.format("diggin...")
        self.log_message(_)
        try:
            self.tabWidget.setCurrentIndex(3)
            # list_to_csv(self.tableView_3.myarray, self.sentfile)
            list_to_csv(self.tableView_3.tablemodel.arraydata, self.sentfile)
            self.senttab_dirty = False

            logger.info("\n\n Csv file written to %s \n\n", self.sentfile)
            self.anchortab_dirty = False
            os.startfile(os.path.dirname(self.sentfile))
            self.log_message(f"Done: Csv file written to {self.sentfile}")
        except Exception as exc:
            logger.error(exc)
            _ = f"{exc} (to be fixed)"
            self.log_message(_)
            QMessageBox(self, "Hint", ic.format(_))

    def export_tmx(self):
        """Export TMX."""
        # switch to log tab
        _ = ic.format("diggin...")
        self.log_message(_)
        try:
            self.tabWidget.setCurrentIndex(3)

            # srclist = [elm[0] for elm in self.tableView_3.myarray]
            # tgtlist = [elm[1] for elm in self.tableView_3.myarray]
            srclist = [elm[0] for elm in self.tableView_3.tablemodel.arraydata]
            tgtlist = [elm[1] for elm in self.tableView_3.tablemodel.arraydata]

            # set language
            lang_set = ["english", "chinese", "french", "italian", "german"]
            lang_set = ["en", "zh", "fr", "it", "de"]
            tmxlang = dict(
                zip(
                    # ["english", "chinese", "french", "italian", "german"],
                    lang_set,
                    ["en-US", "zh-CN", "fr-Fr", "it-IT", "de-DE"],
                )
            )  # noqa
            # http://www.lingoes.net/en/translator/langcode.htm
            # https://github.com/LuminosoInsight/langcodes
            if self.srclang not in lang_set:
                srclang = "en-US"
            else:
                srclang = tmxlang[self.srclang]

            if self.tgtlang not in lang_set:
                tgtlang = "en-US"
            else:
                tgtlang = tmxlang[self.tgtlang]

            title = "Export"
            text = "Save as Tmx"
            info = "Select language pair direction (source:target)"
            yestext = srclang + ":" + tgtlang
            notext = tgtlang + ":" + srclang

            ret_val = msg_popup(
                title=title, text=text, info=info, details="", ytext=yestext, ntext=notext
            )  # noqa
            # ret_val = msg_popup(title=title, text=text, info=info, details='')  # noqa

            if ret_val == QMessageBox.Yes:
                tmxtext = lists_to_tmx(srclist, tgtlist, srclang, tgtlang)
                pairlabel = "-" + srclang + "-" + tgtlang
            elif ret_val == QMessageBox.No:
                tmxtext = lists_to_tmx(tgtlist, srclist, tgtlang, srclang)
                pairlabel = "-" + tgtlang + "-" + srclang
            else:
                return None

            with open(
                self.tmxfile[:-4] + pairlabel + ".tmx", "w", encoding="utf-8"
            ) as tmxfile:  # noqa
                tmxfile.write(tmxtext)
            self.senttab_dirty = False
            self.anchortab_dirty = False
            logger.info("\n\n TMX file written to %s \n\n", self.tmxfile)
            os.startfile(os.path.dirname(self.tmxfile))
            self.log_message(f"Done diggin: TMX file written to {self.tmxfile}")
        except Exception as exc:
            logger.error(exc)
            _ = f"{exc} (to be fixed)"
            self.log_message(_)
            QMessageBox(self, "Hint", ic.format(_))

    # slots functions
    def set_row_numbers(self):
        """set row numbers"""
        from select_last_selected_rows import select_last_selected_rows

        if self.tabWidget.currentIndex() != 1:  # anchor tab
            return None
        index1 = self.tableView_2.selectedIndexes()
        lst = []
        for elm in index1:
            lst += [[elm.row() + 1, elm.column()]]

        lrrows = select_last_selected_rows(lst)
        logger.debug("row # for left right cols: %s", lrrows)

        if lrrows[0] > 0:  # last selected row for left col
            # set lrow = lrrows[0]
            self.lineEdit_lrow.setText(str(lrrows[0]))
            logger.debug("Setting row for left to %s", lrrows[0])
            self.lrowno = lrrows[0]
        if lrrows[1] > 0:  # last selected row for right col
            # set lrow = lrrows[1]
            self.lineEdit_rrow.setText(str(lrrows[1]))
            logger.debug("Setting row for right to %s", lrrows[1])
            self.rrowno = lrrows[1]
        # update dispmsg
        self.dispmsg()

    def manual_set_anchor(self):
        """manually set an anchor with Return."""
        # pass
        logger.debug(" Return pressed while in Anchor tab.")
        logger.debug(" Executing self.update_mytable2()... ")
        self.update_mytable2()

    def flipmerit(self):
        """
        self.actionMerit_0_or_1.

        set/reset merit col = 2 of arraydata/myarray
        """

        def update_table(mytable):  # pass self.tableView_2, 3
            """temp func."""

            # if any rows are selected
            indices = mytable.selectionModel().selectedRows()

            rows = []
            for elm in indices:
                rows += [elm.row()]

            # reversed_rows = list(reversed(sorted(rows)))
            selected_rows = list(sorted(rows))
            logger.info("Selected rows: %s ", selected_rows)

            # if selected rows
            if selected_rows:
                # logger.debug("arraydata: %s", mytable.tablemodel.arraydata)  # to be removed  # noqa  # noqa
                # self.tablemodel.layoutAboutToBeChanged.emit()

                datafloat = 0.0
                try:
                    datafloat = float(
                        mytable.tablemodel.arraydata[selected_rows[0]][2]
                    )  # noqa
                except Exception:  # as exc:  # '' set to 0, invalid input all set to 0  # noqa
                    pass
                if datafloat > 0:
                    datafloat = 0.0
                else:
                    datafloat = 1.0

                for elm in selected_rows:
                    # self.tablemodel.arraydata = self.tablemodel.arraydata[:elm] + self.tablemodel.arraydata[elm + 1:]  # noqa okok
                    indexcol2 = mytable.tablemodel.createIndex(elm, 2)
                    mytable.tablemodel.arraydata[elm][
                        2
                    ] = datafloat  # noqa need to use self.tablemodel.arraydata?
                    mytable.tablemodel.dataChanged.emit(indexcol2, indexcol2)

                # self.tablemodel.layoutChanged.emit()
                logger.info("flipped.")
                # logger.debug("**after** arradata: %s", self.tablemodel.arraydata)  # to be removed  # noqa
                return None

            # if none selected, process the last selectedIndexes
            index1 = mytable.selectedIndexes()
            if index1:
                idxi = index1[-1].row()
                idxj = index1[-1].column()
                datafloat = 0.0
                try:
                    # datafloat = float(mytable.myarray[idxi][2])
                    datafloat = float(mytable.tablemodel.arraydata[idxi][2])
                except Exception:  # as exc:  # '' set to 0, invalid input all set to 0  # noqa
                    pass
                # logger.debug("self.arraydata[idxi][2] %s, float %s ", mytable.myarray[idxi][2], datafloat)  # noqa
                logger.debug(
                    "self.arraydata[idxi][2] %s, float %s ",
                    mytable.tablemodel.arraydata[idxi][2],
                    datafloat,
                )  # noqa

                logger.debug(" before flipping: %s ", datafloat)
                if datafloat > 0:
                    datafloat = 0.0
                else:
                    datafloat = 1.0
                logger.debug(" After flipping: %s ", datafloat)

                indexcol0 = mytable.tablemodel.createIndex(idxi, 0)
                indexcol2 = mytable.tablemodel.createIndex(idxi, 2)
                # mytable.myarray[idxi][2] = datafloat
                mytable.tablemodel.arraydata[idxi][2] = datafloat
                mytable.tablemodel.dataChanged.emit(indexcol0, indexcol2)
                logger.debug(" %s-th row's merit flipped ", idxi + 1)
                indexnr = mytable.tablemodel.createIndex(idxi + 1, idxj)
                mytable.setCurrentIndex(indexnr)

        if self.tabWidget.currentIndex() == 1:  # anchortab
            update_table(self.tableView_2)
            logger.debug("Set/reset merit on anchortab")
        elif self.tabWidget.currentIndex() == 2:  # senttab
            update_table(self.tableView_3)
            logger.debug("Set/reset merit on senttab")

    def splitdouble(self):
        """Splitdouble actionBreak |||."""
        # from data_for_updating import data_for_splitdouble

        def update_table(mytable):  # pass self.tableView_[, 2, 3]]
            """Update_table."""
            logzero.loglevel(set_loglevel())

            # a list!
            index1 = mytable.selectedIndexes()

            logger.info(" index1: %s, type(index1): %s", index1, type(index1))

            _ = """  # leave it as it
            try:
                index1, = index1
            except Exception as exc:
                logger.info(" index1: %s, type(index1): %s", index1, type(index1))
                logger.error("Unable to retrieve index: %s, quit update_table()", exc)
                return None
            # """

            logger.info(" index1: %s, type(index1): %s", index1, type(index1))

            # MyDelegate  self.emit(SIGNAL("commitData(QWidget*)"), self.editor)  # noqa
            # try:
            # mytable.delegate.emit(SIGNAL("commitData(QWidget*)"), mytable.delegate.editor)  # noqa works! pyqt4
            # except Exception: pass

            _ = """
            mytable.delegate.emit(
                pyqtSignal("commitData(QWidget*)"), mytable.delegate.editor
            )  # noqa works! in pyqt4

            # mytable.delegate.commitData.emit()
            # """

            # refer to mat-dir\pyqt\neualigner-pyqt5
            # insert-example-pyqt5.py

            # insert "|||" first at the cursor
            # refer to "def test" in insert-example-qplaintext-pyqt5.py
            # replace self there with mytable
            # index = mytable.currentIndex()

            logger.debug("debug1 resetting logzero.loglevel: %s", set_loglevel())
            logzero.loglevel(set_loglevel())
            logger.info(" resetting logzero.loglevel: %s", set_loglevel())
            logger.debug("debug2 resetting logzero.loglevel: %s", set_loglevel())

            logger.info(" index1: %s, type(index1): %s", index1, type(index1))

            try:
                # item = mytable.tablemodel.data(index1, Qt.DisplayRole)
                item = mytable.tablemodel.data(index1[-1], Qt.DisplayRole)
            except Exception as exc:
                logger.error("Unable to get item: *%s*, setting to ''", exc)
                item = ""

            try:
                cursorpos = mytable.delegate.cursorpos
                logger.debug("cursorpos: %s", cursorpos)
            except Exception:
                cursorpos = -1

            logger.debug("cursorpos: %s", cursorpos)
            if cursorpos == -1:
                logger.debug("Invalid cursorpos: %s", cursorpos)
            else:
                # mytable.tablemodel.layoutAboutToBeChanged.emit()
                _ = insert_itag(item, cursorpos)
                logger.debug("_: %s, item: %s, cursorpos: %s", _, item, cursorpos)
                try:
                    # index1.model().setData(index1, _)
                    mytable.tablemodel.setData(index1[-1], _)
                except Exception as exc:
                    logger.error(exc)

                mytable.tablemodel.dataChanged.emit(index1[-1], index1[-1])

                # mytable.tablemodel.layoutChanged.emit()

                logger.debug(" cell altered? %s", _)

                mytable.delegate.cursorpos = -1

                # no need
                # commit change about inserted itag
                # mytable.delegate.commitData.emit(mytable.delegate.editor)

            if index1:
                idxi = index1[-1].row()
                # idxj = index1[-1].column()
                # vec0 = mytable.myarray[idxi][:]
                vec0 = mytable.tablemodel.arraydata[idxi][:]
                rows_to_add = data_for_splitdouble(vec0)

                if len(rows_to_add) == 1:  # no ||| exists
                    return None
                urow, lrow = rows_to_add
                logger.debug(" urow lrow %s, %s", urow, lrow)

                indexcol0 = mytable.tablemodel.createIndex(idxi, 0)
                indexcol2 = mytable.tablemodel.createIndex(idxi, 2)
                # first update lrow to keep the selected cell
                # mytable.myarray[idxi] = lrow[:]
                mytable.tablemodel.arraydata[idxi] = lrow[:]
                # mytable.tablemodel.dataChanged.emit(index1[-1], index1[-1])
                mytable.tablemodel.dataChanged.emit(indexcol0, indexcol2)
                logger.debug(" update lrow: %s", lrow)

                mytable.tablemodel.layoutAboutToBeChanged.emit()
                # mytable.myarray.insert(idxi, urow)
                mytable.tablemodel.arraydata.insert(idxi, urow)
                mytable.tablemodel.layoutChanged.emit()

                logger.debug(" update urow: %s", urow)

                # something not right, this should not be needed
                # after insertion, the inserted row will be idxi-th row
                # mytable.myarray[idxi] = urow[:]
                mytable.tablemodel.arraydata[idxi] = urow[:]
                mytable.tablemodel.dataChanged.emit(index1[-1], index1[-1])
                # mytable.tablemodel.dataChanged.emit(indexcol0, indexcol2)

                mytable.selectRow(idxi + 1)  # ?

                # works
                # mytable.myarray[idxi] = urow[:]
                # mytable.tablemodel.dataChanged.emit(index1[-1], index1[-1])  # the last selected cell  # noqa

            return None

        logger.debug(
            ">>>Breaking |||...tab index %s <<<", self.tabWidget.currentIndex()
        )  # noqa
        if self.tabWidget.currentIndex() == 1:
            logger.debug(
                "Breaking|||...tab index %s ", self.tabWidget.currentIndex()
            )  # noqa

            update_table(self.tableView_2)

        elif self.tabWidget.currentIndex() == 2:
            logger.debug(
                "Moving up...tab index %s ", self.tabWidget.currentIndex()
            )  # noqa

            update_table(self.tableView_3)

    def moveup(self):
        """
        Move selected cell up for the active tab.

        refer to split_cell()

        index1 = self.tableView_1.selectedIndexes()
        if index1:
            index1[-1].column()

        """

        def update_table(mytable):  # pass self.tableView_[, 2, 3]]
            """update_table."""
            index1 = mytable.selectedIndexes()
            if index1:
                idxi = index1[-1].row()
                idxj = index1[-1].column()

                # vec0 = mytable.myarray[idxi][:]
                vec0 = mytable.tablemodel.arraydata[idxi][:]
                urow, lrow = data_for_moveup(vec0, idxj)

                # if idxj is '', merge with the previous row
                # if str(mytable.myarray[idxi - 1][idxj]).strip() == '':
                if (
                    str(mytable.tablemodel.arraydata[idxi - 1][idxj]).strip() == ""
                ):  # noqa
                    indexpr = mytable.tablemodel.createIndex(idxi - 1, idxj)
                    # mytable.myarray[idxi - 1][idxj] = urow[idxj]
                    mytable.tablemodel.arraydata[idxi - 1][idxj] = urow[idxj]
                    mytable.tablemodel.dataChanged.emit(indexpr, indexpr)

                    # mytable.myarray[idxi] = lrow[:]
                    mytable.tablemodel.arraydata[idxi] = lrow[:]
                    mytable.tablemodel.dataChanged.emit(index1[-1], index1[-1])
                    # set current to prv row
                    mytable.setCurrentIndex(indexpr)
                    logger.debug(
                        " moveup prv index %s %s ", indexpr.row(), indexpr.column()
                    )  # noqa
                else:
                    # mytable.myarray[idxi] = lrow[:]
                    mytable.tablemodel.arraydata[idxi] = lrow[:]
                    mytable.tablemodel.dataChanged.emit(
                        index1[-1], index1[-1]
                    )  # the last selected cell  # noqa

                    mytable.tablemodel.layoutAboutToBeChanged.emit()
                    # mytable.myarray.insert(idxi, urow)
                    mytable.tablemodel.arraydata.insert(idxi, urow)
                    mytable.tablemodel.layoutChanged.emit()

            return None

        logger.debug(
            ">>>Moving up...tab index %s <<<", self.tabWidget.currentIndex()
        )  # noqa
        if self.tabWidget.currentIndex() == 1:
            logger.debug(
                "Moving up...tab index %s ", self.tabWidget.currentIndex()
            )  # noqa

            update_table(self.tableView_2)

        elif self.tabWidget.currentIndex() == 2:
            logger.debug(
                "Moving up...tab index %s ", self.tabWidget.currentIndex()
            )  # noqa

            update_table(self.tableView_3)

    def movedown(self):
        """
        Move selected cell down for the active tab.

        refer to moveup()

        index1 = self.tableView_1.selectedIndexes()
        if index1:
            index1[-1].column()

        """

        def update_table(mytable):  # pass self.tableView_[, 2, 3]]
            """update_table."""
            index1 = mytable.selectedIndexes()
            if index1:
                idxi = index1[-1].row()
                idxj = index1[-1].column()

                # logger.debug(" idxi %s, idxj %s, len(mytable.myarray) - 1: %s ", idxi, idxj, len(mytable.myarray) - 1)  # noqa
                logger.debug(
                    " idxi %s, idxj %s, len(mytable.tablemodel.arraydata) - 1: %s ",
                    idxi,
                    idxj,
                    len(mytable.tablemodel.arraydata) - 1,
                )  # noqa

                # if idxi < len(mytable.myarray) - 1:  # not last row
                if idxi < len(mytable.tablemodel.arraydata) - 1:  # not last row  # noqa
                    # vec0 = mytable.myarray[idxi][:]
                    vec0 = mytable.tablemodel.arraydata[idxi][:]
                    # current row index0 index2
                    indexcr0 = mytable.tablemodel.createIndex(idxi, 0)
                    indexcr2 = mytable.tablemodel.createIndex(idxi, 2)
                    urow, lrow = data_for_movedown(vec0, idxj)
                    mytable.tablemodel.dataChanged.emit(indexcr0, indexcr2)

                    # mytable.myarray[idxi] = urow[:]
                    mytable.tablemodel.arraydata[idxi] = urow[:]
                    mytable.tablemodel.dataChanged.emit(indexcr0, indexcr2)

                    # if idxj is '', merge with the next row
                    indexnr = mytable.tablemodel.createIndex(idxi + 1, idxj)
                    # if str(mytable.myarray[idxi + 1][idxj]).strip() == '':
                    if (
                        str(mytable.tablemodel.arraydata[idxi + 1][idxj]).strip() == ""
                    ):  # noqa

                        # mytable.myarray[idxi + 1][idxj] = lrow[idxj]
                        mytable.tablemodel.arraydata[idxi + 1][idxj] = lrow[
                            idxj
                        ]  # noqa
                        mytable.tablemodel.dataChanged.emit(indexnr, indexnr)

                    else:  # insert lrow at idxi+1
                        mytable.tablemodel.layoutAboutToBeChanged.emit()
                        # mytable.myarray.insert(idxi + 1, lrow)
                        mytable.tablemodel.arraydata.insert(idxi + 1, lrow)
                        mytable.tablemodel.layoutChanged.emit()
                    # set current index to indexnr
                    mytable.setCurrentIndex(indexnr)
                else:  # use append
                    # vec0 = mytable.myarray[idxi][:]
                    vec0 = mytable.tablemodel.arraydata[idxi][:]
                    # current row index0 index2
                    indexcr0 = mytable.tablemodel.createIndex(idxi, 0)
                    indexcr2 = mytable.tablemodel.createIndex(idxi, 2)
                    urow, lrow = data_for_movedown(vec0, idxj)
                    mytable.tablemodel.dataChanged.emit(indexcr0, indexcr2)

                    # mytable.myarray[idxi] = urow[:]
                    mytable.tablemodel.arraydata[idxi] = urow[:]
                    mytable.tablemodel.dataChanged.emit(indexcr0, indexcr2)

                    mytable.tablemodel.layoutAboutToBeChanged.emit()
                    # mytable.myarray.append(lrow)  # modi append
                    mytable.tablemodel.arraydata.append(lrow)  # modi append
                    mytable.tablemodel.layoutChanged.emit()

                    # set current index to indexnr
                    indexnr = mytable.tablemodel.createIndex(idxi + 1, idxj)
                    mytable.setCurrentIndex(indexnr)

            return None

        logger.debug(
            ">>>Moving down...tab index %s <<<", self.tabWidget.currentIndex()
        )  # noqa
        if self.tabWidget.currentIndex() == 1:
            logger.debug(
                "Moving down...tab index %s ", self.tabWidget.currentIndex()
            )  # noqa

            update_table(self.tableView_2)

        elif self.tabWidget.currentIndex() == 2:
            logger.debug(
                "Moving down...tab index %s ", self.tabWidget.currentIndex()
            )  # noqa

            update_table(self.tableView_3)

    def mergedown(self):
        """
        Merge the selected cell down for the active tab.

        refer to movedown()

        index1 = self.tableView_1.selectedIndexes()
        if index1:
            index1[-1].column()

        """
        # from data_for_updating import data_for_mergedown

        def update_table(mytable):  # pass self.tableView_[, 2, 3]]
            """update_table."""
            index1 = mytable.selectedIndexes()
            if index1:
                idxi = index1[-1].row()
                idxj = index1[-1].column()

                # if idxi == len(mytable.myarray) - 1:  # nothing to do
                if (
                    idxi == len(mytable.tablemodel.arraydata) - 1
                ):  # nothing to do  # noqa
                    return None

                # vec0 = mytable.myarray[idxi][:]
                vec0 = mytable.tablemodel.arraydata[idxi][:]
                # vec1 = mytable.myarray[idxi + 1][:]
                vec1 = mytable.tablemodel.arraydata[idxi + 1][:]
                # gen the moerged row

                sepchar = ""
                # idxj=0: self.srclang, idxj=1: self.tgtlang
                col_lang = [self.srclang, self.tgtlang]
                if col_lang[idxj] == "chinese":
                    sepchar = ""
                else:
                    sepchar = " "

                urow, lrow = data_for_mergedown(vec0, vec1, idxj, sepchar)

                # next row, col2 index
                indexnr2 = mytable.tablemodel.createIndex(idxi + 1, 2)
                # update idxi row with lrow
                # mytable.myarray[idxi] = urow[:]
                mytable.tablemodel.arraydata[idxi] = urow[:]
                # mytable.myarray[idxi + 1] = lrow[:]
                mytable.tablemodel.arraydata[idxi + 1] = lrow[:]
                mytable.tablemodel.dataChanged.emit(index1[-1], indexnr2)

                indexnr = mytable.tablemodel.createIndex(idxi + 1, idxj)
                mytable.setCurrentIndex(indexnr)
                # fini

            return None

        logger.debug(
            ">>>Merging down...tab index %s <<<", self.tabWidget.currentIndex()
        )  # noqa
        if self.tabWidget.currentIndex() == 1:
            logger.debug(
                "Merging down...tab index %s ", self.tabWidget.currentIndex()
            )  # noqa

            update_table(self.tableView_2)

        elif self.tabWidget.currentIndex() == 2:
            logger.debug(
                "Merging down...tab index %s ", self.tabWidget.currentIndex()
            )  # noqa

            update_table(self.tableView_3)

    def mergeup(self):
        """Merge the selected cell up for the active tab.

        refer to mergedown()

        index1 = self.tableView_1.selectedIndexes()
        if index1:
            index1[-1].column()
        """

        def update_table(mytable):  # pass self.tableView_[, 2, 3]]
            """update_table."""
            index1 = mytable.selectedIndexes()
            if index1:
                idxi = index1[-1].row()
                idxj = index1[-1].column()

                if idxi == 0:  # nothing to do
                    return None

                # vec0 = mytable.myarray[idxi - 1][:]
                vec0 = mytable.tablemodel.arraydata[idxi - 1][:]
                # vec1 = mytable.myarray[idxi][:]
                vec1 = mytable.tablemodel.arraydata[idxi][:]
                # gen the moerged row

                sepchar = ""
                # idxj=0: self.srclang, idxj=1: self.tgtlang
                col_lang = [self.srclang, self.tgtlang]

                # if col_lang[idxj] == "chinese":
                if col_lang[idxj] == "zh":
                    sepchar = ""
                else:
                    sepchar = " "

                urow, lrow = data_for_mergeup(vec0, vec1, idxj, sepchar)

                # prev row, idxj, next rwo, col2 index
                indexprj = mytable.tablemodel.createIndex(idxi - 1, idxj)
                indexcr2 = mytable.tablemodel.createIndex(idxi, 2)
                # update idxi row with lrow
                # mytable.myarray[idxi - 1] = urow[:]
                mytable.tablemodel.arraydata[idxi - 1] = urow[:]
                # mytable.myarray[idxi] = lrow[:]
                mytable.tablemodel.arraydata[idxi] = lrow[:]
                mytable.tablemodel.dataChanged.emit(indexprj, indexcr2)

                mytable.setCurrentIndex(indexprj)
                # fini

            return None

        logger.debug(
            ">>>Merging up...tab index %s <<<", self.tabWidget.currentIndex()
        )  # noqa
        if self.tabWidget.currentIndex() == 1:
            logger.debug(
                "Merging up...tab index %s ", self.tabWidget.currentIndex()
            )  # noqa

            update_table(self.tableView_2)

        elif self.tabWidget.currentIndex() == 2:
            logger.debug(
                "Merging up...tab index %s ", self.tabWidget.currentIndex()
            )  # noqa

            update_table(self.tableView_3)

    def update_mytable2(self):
        """Update self.tableView_2.

        on
        self.setAnchorButton.clicked.connect()
        based on ui inputs (self.lrowno, self.rrowno, self.merit)
        get
        """
        from set_anchor_extra_outputs import set_anchor_extra_outputs

        # out1, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(testarray, lpos, rpos)  # test_35()  # noqa
        # proceed only when all three are True
        logger.debug(
            "\n   >>>*** update_mytable2 started *** \n self.anchorValid1123: %s %s %s ",
            self.anchorValid1,
            self.anchorValid2,
            self.anchorValid3,
        )  # noqa
        if not (self.anchorValid1 and self.anchorValid2 and self.anchorValid3):
            return None

        if self.lrowno != self.rrowno and self.merit <= 0:
            return None

        # logger.debug(" lrowno rrowno merit %s %s %s %f", self.lrowno, self.rrowno, self.merit, self.merit)  # noqa
        # logger.debug("\n *** Calling set_anchor_extra_outputs *** with ")
        # logger.debug(" %s %s %s %s", self.tableView_2.myarray[:5], self.lrowno - 1, self.rrowno - 1, self.merit)  # noqa

        # _, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(self.tableView_2.myarray, self.lrowno - 1, self.rrowno - 1, merit=self.merit)  # noqa
        _, at_row, row_numbers, rows_to_add = set_anchor_extra_outputs(
            self.tableView_2.tablemodel.arraydata,
            self.lrowno - 1,
            self.rrowno - 1,
            merit=self.merit,
        )  # noqa

        # logger.debug("\n **exit** set_anchor_extra_outputs ")

        # logger.debug(" self.tableView_2.myarray\n     %s ", np.array(self_2.myarray[:5]))  # noqa

        # logger.debug("\n at_row, row_numbers, rows_to_add\n  %s, %s, %s ", at_row, row_numbers, np.array(rows_to_add))  # noqa

        # logger.debug("\n *** Updating tablemodel...*** ")
        self.tableView_2.tablemodel.layoutAboutToBeChanged.emit()
        for ith in range(row_numbers):
            # self.tableView_2.myarray.pop(at_row)
            self.tableView_2.tablemodel.arraydata.pop(at_row)
        self.tableView_2.tablemodel.layoutChanged.emit()

        self.tableView_2.tablemodel.layoutAboutToBeChanged.emit()
        for ith, elm in enumerate(rows_to_add):
            # self.tableView_2.myarray.insert(at_row + ith, elm)
            self.tableView_2.tablemodel.arraydata.insert(at_row + ith, elm)
        self.tableView_2.tablemodel.layoutChanged.emit()

        # out2 = testarray[:]
        # out2 = deepcopy(self.tableView_2.myarray)
        out2 = deepcopy(self.tableView_2.tablemodel.arraydata)
        for ith in range(row_numbers):
            out2.pop(at_row)

        for ith, elm in enumerate(rows_to_add):
            out2.insert(at_row + ith, elm)

        # logger.debug("\n tableView_2.myarray Layoutchanged: \n %s ", np.array(self_2.myarray[:5]))  # noqa

        # logger.debug("\n check out2 \n***** (===end of update_mytable2===) %s ", np.array(out2[:5]))  # noqa

    def closeEvent(self, event):
        """close"""
        result = QMessageBox.question(
            self,
            "Confirm Exit...",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if result == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def plusmessage(self):
        """Test."""
        # self.label.setText("You have selected Plus ")
        # qDebug("You have selected Plus ")
        logger.debug(" You have selected Plus %s", self.merit)

    def test(self):
        """Test."""
        # index2 = self.currentIndex()
        index1 = self.tableView_1.selectedIndexes()
        if index1:
            logger.debug(
                " index1.row() %s index1[0].column() %s ",
                index1[0].row(),
                index1[0].column(),
            )  # noqa
            self.tableView_1.clearSelection()

        index2 = self.tableView_2.selectedIndexes()

        if index2:
            logger.debug(
                " index2.row() %s index2[0].column() %s ",
                index2[0].row(),
                index2[0].column(),
            )  # noqa
            self.tableView_2.clearSelection()

        # logger.debug(" index2 %s " % index2)
        # x = tableView.selectedIndexes()

        logger.debug(
            "self.tabWidget.currentIndex() %s ", self.tabWidget.currentIndex()
        )  # noqa

    def open(self, file=1):
        r"""Open self.filename and send content to
        self.tableView_1.myarray[0][colno], colno = file-1.

        Get filename and show only .writer files
        [pyqt\editor\Writer-Tutorial]
        """
        self.no_of_loadfiles += 1
        logzero.loglevel(set_loglevel())
        logger.debug(" self.no_of_loadfiles: %s", self.no_of_loadfiles)

        # for actionFile1 trigger
        file = int(file)
        if file < 1:
            file = 1

        if int(file) > 2:
            file = 2

        if not (file == 1 or file == 2):  # wont be needed in fact
            logger.debug(
                "open() Invalid file= %s supplied " "(ought to be 1 or 2), exiting...",
                file,
            )
            return None

        fdl = QFileDialog()
        self.filename, _ = fdl.getOpenFileName(
            self,
            "Open File",
            self.init_dir,
            "(*.txt *.docx *.epub *.zip *.srt *.htm *.html *.pdf)",
        )

        logger.debug("getOpenFileName: %s, %s", self.filename, _)

        logger.debug("Opening %s...type: %s", self.filename, type(self.filename))

        if not self.filename:
            return None  # canceled, do nothing

        # set self.file1, self.file2 for gen file trunk
        if file == 1:
            self.file1 = self.filename
            self.no_of_loadfiles = 1
        else:
            self.file2 = self.filename

        # switch to file tab
        logger.debug(" self.tabWidget.setCurrentIndex(0) ")
        self.tabWidget.setCurrentIndex(0)

        try:
            filecontent = load_file_as_text(self.filename)
        except Exception as exc:
            logger.error(exc)
            filecontent = str(exc)

        logger.debug("filecontent[:50]: %s", filecontent[:50])

        if filecontent is None:
            logger.error(
                "Failed to load the file [%s], filecont = load_file_as_text resulted in None.",
                self.filename,
            )
            return None

        filecontent = filecontent.splitlines()
        filecontent = [elm.strip() for elm in filecontent if elm.strip()]
        totlines = len(filecontent)

        filecontent = "\n\n".join(filecontent)
        totlines = filecontent.count("\n\n")

        logger.debug("totlines: %s", totlines)

        # langid.set_languages()
        if file == 1:
            self.srclang = detect_lang(filecontent)
            self.no_of_loadfiles = 1
        else:
            self.tgtlang = detect_lang(filecontent)

        # detect_lang used fastlid, old version of fastlid turns debug off
        logzero.loglevel(set_loglevel())

        if self.srclang == "" or self.srclang is None:
            logger.warning(" Cant detect srclang, setting to english...")
            self.srclang = "english"

        if self.tgtlang == "" or self.tgtlang is None:
            logger.warning(" Cant detect tgtlang, setting to chinese...")
            self.srclang = "zh"

        logger.debug(
            " self.srclang %s, self.tgtlang %s", self.srclang, self.tgtlang
        )  # noqa

        if self.srclang == "zh" and self.no_of_loadfiles == 1:
            _ = """
            msg = QMessageBox()
            msg.setWindowTitle("Wait...")
            msg.setIcon(QMessageBox.Question)  # Question, Information, Warning, Critical  # noqa
            msg.setText("You really want to load Chinese text as source?")

            msg.setInformativeText("Currently, auto-anchor for Chinese text as source language is not yet supported.")  # noqa
            msg.setDetailedText("If you click Yes, you can set anchors manually. Or you can click No or Cancel and reload another text as source text.")  # noqa

            # Add the standard buttons "Ok" and "Cancel"
            # msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)  # noqa

            # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel)  # noqa
            ret_val = msg.exec_()

            if ret_val != QMessageBox.Yes:
                self.srclang == ''
                self.no_of_loadfiles = 0
                return None  # user clicked No or Cancel, reset self.srclang and do nothing  # noqa
            else:
                self.no_of_loadfiles += 1
            # """
            # modi 2017 02 09

        self.no_of_loadfiles += 1

        # self.tableView_1.myarray[0][colno] = filecontent
        if not self.tableView_1.tablemodel.arraydata:  # possible deleted to empty []
            self.tableView_1.tablemodel.layoutAboutToBeChanged.emit()
            self.tableView_1.tablemodel.arraydata = [["", "", ""]]
            self.tableView_1.tablemodel.layoutChanged.emit()

        # -- update self.tableView_1.tablemodel as necessary

        # file=1 to the left column, file=2 to the right col
        colno = file - 1

        logger.debug("colno: %s", colno)
        logger.debug("Update tab0 col: %s", colno)

        _ = """
        # self.resizeColumnsToContents()
        # self.tableView_1.resizeColumnsToContents()
        # self.tableView_1.resizeRowsToContents()
        self.tableView_1.tablemodel.arraydata[0][colno] = filecontent

        # update with signal for index: 0, colno
        index00 = self.tableView_1.tablemodel.createIndex(0, colno)
        self.tableView_1.tablemodel.dataChanged.emit(index00, index00)
        # """
        _ = np.array(self.tableView_1.tablemodel.arraydata, dtype=object)
        logger.debug(" self.tableView_1.tablemodel.arraydata.shape: %s", _.shape)
        if _.shape[0] > 1:
            update_cell(self.tableView_1.tablemodel, 1, colno, filecontent)
        else:
            update_cell(self.tableView_1.tablemodel, 0, colno, filecontent)

        self.tableView_1.resizeRowsToContents()

        logger.debug(" done updating tab1 cell (0, %s) ", colno)

        # enable Tab2 (setAnchor tab)
        logger.debug("set self.actionAnchor.setEnabled(True)")
        self.actionAnchor.setEnabled(True)

        # --------
        _ = """  # does not quite work
        logger.debug(" tableView_1 cell (0, %s) updated", colno)

        # load splitlines() to Tab1's left col
        logger.debug(" load splitlines() to Tab1's left col. ")
        left = [_ for _ in filecontent.splitlines() if _.strip()]
        _ = [*zip_longest_middle(left, [""], fillvalue="")]
        self.tableView_2.tablemodel.layoutAboutToBeChanged.emit()
        self.tableView_2.tablemodel.arraydata[0] = _
        self.tableView_2.tablemodel.layoutChanged.emit()

        logger.debug(" tab 1 updated")
        # ---- """

        taildots = ""
        # if len(self.tableView_1.myarray[0][colno]) > 200:
        if len(self.tableView_1.tablemodel.arraydata[0][colno]) > 200:
            taildots = "......"

        logger.debug(" >>> self.tableView_1.myarray: %s", self.tableView_1.myarray)
        logger.debug(
            " %s: self.tableView_1.tablemodel.arraydata[0][colno][:200].strip() + taildots++  s ++",
            self.filename,
            # self.tableView_1.tablemodel.arraydata[0][colno][:200].strip() + taildots,
        )  # noqa

        logger.debug(" Done self.open ")

    # to anchortab
    def import_to_anchortab(self):
        """
        Import csv, txt, xls, xlsx to Para tab.

        uses set_anchors.

        refer to def open()

        """
        # import pandas as pd
        from .csv_to_list import csv_to_list
        from .excel_to_list import excel_to_list
        from .tmx_to_list import tmx_to_list

        if self.anchortab_dirty:
            # ret_val = self.popup_anchortab_dirty()
            ret_val = popup_anchortab_dirty()
            if ret_val != QMessageBox.Yes:
                return None  # only proceed when Yes is clicked.

        self.tabWidget.setCurrentIndex(3)
        logger.debug(" switched to Log tab.")

        # self.import_para_filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', ".", "Text files (*.txt *.csv)\nExcel files (*.xls *.xlsx)\nTMX files (*.tmx)")  # noqa
        self.import_paras_filename = QFileDialog.getOpenFileName(
            self,
            "Open File",
            self.init_dir,
            "Csv Txt(Tab) Excel Tmx files (*.txt *.csv *.xls *.xlsx *.tmx)",
        )

        logger.debug("This may take a while (up to a few minutes)")
        logger.debug("The bigger the file, the longer it takes, hold on...")
        logger.handlers[0].flush()

        # if open file not executed/aligned_trunk==''
        # set aligned_trunk to
        if not self.aligned_trunk:
            ftrunk = os.path.split(self.import_paras_filename)[0]

            # if the last part is aligned, remove it
            ftrunk01 = os.path.split(ftrunk)
            if ftrunk01[1] == "aligned":
                self.aligned_trunk = ftrunk01[0]
            else:
                self.aligned_trunk = ftrunk

            self.parafile = self.aligned_trunk + "_anchored_paras.txt"
            self.sentfile = self.aligned_trunk + ".txt"
            self.tmxfile = self.aligned_trunk + ".tmx"

            logger.debug(" self.aligned_trunk %s ", self.aligned_trunk)
            logger.debug(" self.parafile %s ", self.parafile)

        tabdata = ""

        if self.import_paras_filename[-4:] in [".csv", ".txt"]:
            tabdata = csv_to_list(self.import_paras_filename)

        if self.import_paras_filename[-4:] in [".xls", "xlsx"]:
            tabdata = excel_to_list(self.import_paras_filename)

        if self.import_paras_filename[-4:] in [".tmx"]:
            tabdata00 = tmx_to_list(self.import_paras_filename)
            tabdata = [elm + [""] for elm in tabdata00]

        # update anchor tab
        if tabdata:
            self.set_anchors(tabdata)

        self.tabWidget.setCurrentIndex(1)
        logger.debug(" switched to Anchor tab")

    def set_anchors(self, tabdata):
        """Set anchors."""
        try:
            len0 = len(tabdata)
        except Exception as exc:
            logger.error("len(tabdata): %s", exc)
            return None

        if len0 <= 0:
            logger.warning(" len(tabdata) %s <= 0: nodata", len0)
            return None

        # self.tableView_2.tablemodel.layoutAboutToBeChanged.emit()
        # pos = 0

        # switch to log tab here
        # logger.debug(" currentIndex %s before", self.tabWidget.currentIndex())  # noqa

        # self.tabWidget.setCurrentIndex(3)

        # logger.debug(" currentIndex %s after", self.tabWidget.currentIndex())

        # self.anchortab_dirty == True
        # popup: done in files_to_anchortab
        #
        # set_anchors
        # always clear table

        # reset
        if self.anchortab_dirty is True:
            self.tableView_2.tablemodel.layoutAboutToBeChanged.emit()
            for _ in range(len(self.tableView_2.tablemodel.arraydata)):
                self.tableView_2.tablemodel.arraydata.pop(0)  # noqa
                # self.tableView_2.myarray.pop(0)  # noqa
                # self.tableView_2.tablemodel.removeRow(0)  # noqa FIXME

            # why doesnt this work? correct format? [["", "", ""]]
            # self.tableView_2.myarray = []

            self.tableView_2.tablemodel.layoutChanged.emit()

        totlines = len(tabdata)

        for ielm, elm in enumerate(tabdata):
            # self.tableView_2.myarray.insert(pos+ielm, elm)  # Summerfield sl.446  # noqa

            self.tableView_2.tablemodel.layoutAboutToBeChanged.emit()
            # self.tableView_2.myarray.append(elm)  # attach in the end
            self.tableView_2.tablemodel.arraydata.append(
                elm
            )  # attach in the end  # noqa
            self.tableView_2.tablemodel.layoutChanged.emit()

            # logger.info(" set_anchors %s of %s", ielm + 1, totlines)
            # logging_progress(ielm, totlines, bar_length=20)

        logger.debug("^ set_anchors ^")

        # remove possible empty row set in initialization
        # try:
        if self.anchortab_dirty is False:
            self.tableView_2.tablemodel.layoutAboutToBeChanged.emit()
            # self.tableView_2.myarray.remove(['', '', ''])
            try:
                self.tableView_2.tablemodel.arraydata.remove(["", "", ""])
            except Exception as exc:
                logger.error(
                    """self.tableView_2.tablemodel.arraydata.remove(["", "", ""] error: %s""",
                    exc,
                )
            self.tableView_2.tablemodel.layoutChanged.emit()

        # self.tableView_2.tablemodel.layoutChanged.emit()
        logger.debug("Done...")

        self.actionAlign.setEnabled(True)
        self.anchortab_dirty = True

        # time.sleep(1)  # to avoid occasional crash?
        self.tabWidget.setCurrentIndex(1)  # switch to anchor tab

    def files_to_anchortab(self):
        """Define slot function for self actionAnchor."""
        logger.debug(
            "files_to_anchortab(self): self.anchortab_dirty: %s ", self.anchortab_dirty
        )

        if self.anchortab_dirty:
            # ret_val = self.popup_anchortab_dirty()
            ret_val = popup_anchortab_dirty()
            if ret_val != QMessageBox.Yes:
                return None  # only proceed when Yes is clicked.

        # get self.aligned_trunk
        try:
            self.aligned_trunk = twofiles_trunk(self.file1, self.file2)

            self.parafile = self.aligned_trunk + "_anchored_paras.txt"
            self.sentfile = self.aligned_trunk + ".txt"
            self.tmxfile = self.aligned_trunk + ".tmx"

            logger.debug("self.file1 +%s+, self.file2 +%s+", self.file1, self.file2)
            logger.debug(" self.aligned_trunk %s ", self.aligned_trunk)
            logger.debug(" self.parafile %s ", self.parafile)

        except Exception as exc:
            logger.debug(
                "self.aligned_trunk = twofiles_trunk(self.file1, self.file2) exc: %s",
                exc,
            )

        # text1 and text 2 from file tab
        # seq1, ll1 = get_para(file1)
        # seq2, ll2 = get_para(file2)

        # switch to log tab
        # self.tabWidget.setCurrentIndex(3)
        # time.sleep(2)

        # disable button to prevent repeated clicked
        # remember to turn it on later on

        # read from the File tab
        # text1 = str(self.tableView_1.myarray[0][0])
        # text2 = str(self.tableView_1.myarray[0][1])
        text1 = str(self.tableView_1.tablemodel.arraydata[0][0])
        text2 = str(self.tableView_1.tablemodel.arraydata[0][1])

        if not text1.strip():
            logger.warning(
                " The source language column in File tabs empty, load files first."
            )
            QMessageBox.about(
                self,
                "The source language column is empty",
                """<html><head/><body><p><span style=" color:#0000ff;">Please load files first. </span>.</p></body></html>""",
            )  # noqa
            self.actionAnchor.setEnabled(True)
            return None

        self.actionAnchor.setEnabled(True)

        logger.debug(" self.actionAnchor.setEnabled(True) ")

        # seq1 = text_to_paras(text1)
        # seq2 = text_to_paras(text2)
        # self.tabdata = texts_to_anchored_paras(seq1, seq2)

        # setup for mixed page: only file 1 contains data
        if text1.strip() and not text2.strip():
            logger.debug(
                " if text1.strip() and not text2.strip(): setup for mixed page: only file 1 contains data "
            )
        if text1.strip() and not text2.strip():

            # seems to have problem with Inno Setup
            # msg = QMessageBox()
            # msg.setWindowTitle("Wait...")
            # msg.setWindowIcon(QIcon('images/Anchor-48.png'))
            # msg.setIcon(QMessageBox.Information)
            # msg.setText("Proceed?")

            # msg.setInformativeText("The target language (right) column of the File tab is empty.")  # noqa
            # msg.setDetailedText("If you click Yes, the left column will be treated as a mixture of dual languge text. Neualigner will attempt to separate and align the texts. If this is not what you want, click No and then load the target language column.")  # noqa

            self.tabWidget.setCurrentIndex(3)  # switch to log tab

            logger.debug(" tabdata1 = sep_chinese() ")
            try:
                tabdata1 = sep_chinese(text1)  # nx2 list
            except Exception as exc:
                logger.debug(" tabdata1 = sep_chinese() exc: %s", exc)
                logger.debug("text1: +%s+", text1)
                return None

            # set self.srclang and self.tgtlang, not really necessary since autoanchoring is not used in this case
            # needed for realign_selected_rows
            text1 = " ".join([elm[0] for elm in tabdata1])
            text2 = " ".join([elm[1] for elm in tabdata1])

            # langid.set_languages()
            try:
                self.srclang = detect_lang(text1[:2000])
            except Exception as exc:
                logger.debug(" self.srclang = detect_lang(text1[:2000]) exc: %s", exc)

            try:
                self.tgtlang = detect_lang(text2[:2000])
            except Exception as exc:
                logger.debug(" self.tgtlang = detect_lang(text2[:2000]): exc: %s", exc)

            logger.debug(
                "self.srclang: %s, self.tgtlang: %s", self.srclang, self.tgtlang
            )
            # attache the last col
            tabdata1 = [elm + [""] for elm in tabdata1]

            # tabdata1 => tabdata
            # use simple zip_longest_middle, anchor more or less there
            self.set_anchors(tabdata1)
            self.anchortab_dirty = True

            self.actionAnchor.setEnabled(True)
            return None

        if text1.strip() and text2.strip():

            # msgpopup to ask for non network
            msg = QMessageBox()
            msg.setWindowTitle("Wait...")

            # Question, Information, Warning, Critical
            msg.setIcon(QMessageBox.Question)
            msg.setText("You really want to do auto-anchoring?")

            msg.setInformativeText(
                "Autoanchoring uses a net service (quota: 1000 paras per 60 minutes) and is slow (~4 min/1000 paras)."
            )  # noqa
            msg.setDetailedText(
                "If you click Yes, autoanchoring will start. (It's "
                "very important to correct anchors wrongly set by "
                "autoanchoring. You may wish to visually examine the "
                "anchor tab and reset those anchors.) Or you can "
                "click No for manually setting the anchors. "
                "There is no need to set too many anchors, one "
                "anchor for about every 20-50 paras is enough. "
                "Or you can click Cancel to do nothing."
            )

            msg.setStandardButtons(
                QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel
            )  # noqa
            ret_val = msg.exec_()

            if ret_val == QMessageBox.Cancel:  # do nothing
                self.actionAnchor.setEnabled(True)
                return None

            # langid.set_languages()

            self.srclang = detect_lang(text1[:2000])
            self.tgtlang = detect_lang(text2[:2000])
            logger.debug(
                "self.srclang: %s, self.tgtlang: %s", self.srclang, self.tgtlang
            )

            # no auto, simple zip_longest_middle
            if ret_val == QMessageBox.No:
                # text1 = self.text1[:]
                # text2 = self.text2[:]
                para1 = text_to_paras(text1)
                para2 = text_to_paras(text2)
                tabdata = zip_longest_middle(para1, para2, fillvalue="")
                tabdata = [[elm[0], elm[1], ""] for elm in tabdata]
                self.set_anchors(tabdata)

                return None

            # continue if user selects Yes
            self.tabWidget.setCurrentIndex(3)  # switch to log tab

            self.obj = Worker(text1, text2)
            self.thread = QThread()  # no parent!
            self.obj.moveToThread(self.thread)
            self.thread.started.connect(self.obj.get_tabdata)
            self.obj.tabdata_ready.connect(self.set_anchors)
            self.obj.finished.connect(self.on_tabdata_finished)
            self.obj.workRequested.connect(self.thread.start)
            self.obj.request_work()
            # self.actionAnchor.setEnabled(True)

        # self.tabdata = [['1', '2', '3'], ['4', '5', '6'],  ['7', '8', '9']]
        # logger.debug(" ***self.tabdata***: %s " % self.tabdata)

        # logger.debug("**self.tableView_2.myarray before** %s " % self_2.myarray)  # noqa

        # self.layoutAboutToBeChanged.emit()
        # self.tableView_2.tablemodel.layoutAboutToBeChanged.emit()

        # set data and emit for anchor tab
        # self.tableView_2.myarray = self.tabdata

        # set data and emit for anchor tab
        # self.tableView_3.tablemodel.layoutAboutToBeChanged.emit()
        # self.tableView_3.myarray = self.tabdata
        # self.tableView_3.tablemodel.layoutChanged.emit()

        # faster for big table, Summerfield
        # self.tableView_2.tablemodel.reset()

        # logger.debug("**self.tableView_2.myarray after** %s " % self_2.myarray)  # noqa

        # index00 = self.tableView_2.tablemodel.createIndex(0, 0)
        # index11 = self.tableView_2.tablemodel.createIndex(len(self.tabdata), 3)  # noqa
        # self.tableView_2.tablemodel.dataChanged.emit(index00, index11)

        # switch to anchor tab
        # self.tabWidget.setCurrentIndex(3)  # switch to log tab

    def on_tabdata_finished(self):
        """Finished."""
        self.thread.quit()
        self.actionAnchor.setEnabled(True)
        logger.debug(" self.thread.quit() ")

    @pyqtSlot(list)
    def set_senttab(self, tabdata):
        """Set senttab."""
        logger.debug(" set_senttab ")
        self.tableView_3.tablemodel.layoutAboutToBeChanged.emit()
        # pos = 0
        totlines = len(tabdata)
        for ielm, elm in enumerate(tabdata):
            # self.tableView_2.myarray.insert(pos+ielm, elm)  # Summerfield sl.446  # noqa
            # self.tableView_3.myarray.append(elm)  # attach in the end
            self.tableView_3.tablemodel.arraydata.append(
                elm
            )  # attach in the end  # noqa

            # logger.debug("set_sent %s of %s", ielm + 1, totlines)
            logging_progress(ielm, totlines, bar_length=20)
        logger.debug("^ ^")

        # remove possible empty row set in initialization
        try:
            # self.tableView_3.myarray.remove(['', '', ''])
            self.tableView_3.tablemodel.arraydata.remove(["", "", ""])
        except ValueError:  # as exc
            pass

        self.tableView_3.tablemodel.layoutChanged.emit()
        logger.debug("Done...")

        self.senttab_dirty = True

        self.tabWidget.setCurrentIndex(2)

    def on_anchor(self):
        """Respond to anchor butt (actionAnchor) clicked.

        self.tabWidget.currentIndex() == 1:  # anchortab
            (self.tableView_2)

        if selected:  # self.tabWidget.currentIndex() == 1
            reanchor_selected_rows
            return

        files_to_anchortab  # self.tabWidget.currentIndex() == 0

        """
        from .reanchor_selected_rows import (
            reanchor_selected_rows,  # will load sseg, takes about 60 sec
        )

        # if self.tabWidget.currentIndex() == 2 or self.tabWidget.currentIndex() == 3:
        _ = self.tabWidget.currentIndex()
        if _ in [2, 3]:  # sent tab or log tab
            _ = f"""You are on {"Sent tab" if _ in [2] else "Log tab"}. Switch to Files tab or Para tab to use this function"""
            QMessageBox.information(self, "Hint", _)
            self.log_message(ic.format(_))
            return None

        # file tab 0 or anchor tab 1

        if self.tabWidget.currentIndex() == 1:  #
            logger.debug(" current tabWidget 1 (para tab), anchor butt pressed. ")

            indices = self.tableView_2.selectionModel().selectedRows()

            if indices and self.tabWidget.currentIndex() == 1:
                logger.debug(
                    " indices = self.tableView_2.selectionModel().selectedRows(), row selectesd: True"
                )
                reanchor_selected_rows(self.tableView_2)
                return None
            return None

        if self.tabWidget.currentIndex() == 0 or self.tabWidget.currentIndex() == 3:  #
            logger.debug(
                " current tabWidget 0 (file tab) or 3 (Log tab): +%s+, anchor butt pressed. --> self.files_to_anchortab()",
                self.tabWidget.currentIndex(),
            )
            self.files_to_anchortab()

    def on_align(self):
        """
        Align clicked.

        self.tabWidget.currentIndex() == 2:  # senttab
            (self.tableView_3)

        if selected:
            realign_selected_rows
            return

        self.paras_to_senttab()
        """
        if self.tabWidget.currentIndex() == 0 or self.tabWidget.currentIndex() == 3:
            return None

        # para tab 1 or sent tab 2
        indices = self.tableView_3.selectionModel().selectedRows()
        if indices and self.tabWidget.currentIndex() == 2:
            # realign_selected_rows(self.tableView_3)
            realign_selected_rows(self.tableView_3, self.srclang, self.tgtlang)
            return None

        # execute only if the current tab is anchtab
        if self.tabWidget.currentIndex() == 1:
            self.paras_to_senttab()  # uses qthread_func_with_progressbar

    def realign_selected_rows(self):
        """
        Realign selected rows.
        """
        logger.debug(" Realign selected rows ")
        if self.tabWidget.currentIndex() == 2:  # sent tab only
            realign_selected_rows(
                self.tableView_3
            )  # fcn from realign_selected_rows.py in mylib # noqa
            self.senttab_dirty = True

    def paras_to_senttab(self):
        """
        Slot function for self.actionAlign.

        Use modified gen_aligned_sentlist:?
            gen_aligned_sentlist( ratio_diff=1)
            abs(len(s1) - len(s2))/max(len(s1), len(s2)) > 25%, use zip_longest_middle
        """  # noqa
        # ratio_diff = 0.4

        # switch to log tab
        self.tabWidget.setCurrentIndex(3)

        # list1 = deepcopy(self.tableView_2.myarray)  # paratab data list
        list1 = deepcopy(
            self.tableView_2.tablemodel.arraydata
        )  # paratab data list  # noqa

        # crude check, if only one row, and either of them contain nothing
        if len(list1) == 1:
            if not (list1[0][0].strip() and list1[0][1].strip()):
                return None  # nothing to do

        # logger.debug(" list1 %s, \n self.srclang %s, self.tgtlang %s, 0.4 %s", list1[:10], self.srclang, self.tgtlang, 0.4)  # noqa

        #

        # langid.set_languages()
        self.srclang = detect_lang(" ".join([elm[0] for elm in list1]))
        self.tgtlang = detect_lang(" ".join([elm[1] for elm in list1]))

        # popup??

        if not (
            self.srclang != self.tgtlang and bool(self.srclang) and bool(self.tgtlang)
        ):  # noqa
            logger.warning(
                " self.srclang, self.tgtlang: %s, %s are the same...",
                self.srclang,
                self.tgtlang,
            )  # noqa
            logger.warning(" Something is not quite right, exiting...")
            return None

        # ==========================
        # ----- non thread version ----- would
        # logger.debug(" tabdata %s", tabdata)
        # tabdata = gen_aligned_sentlist(list1, self.srclang, self.tgtlang, 0.4)
        # self.set_senttab(tabdata)

        # ----- thread version -----
        # TODO threaded gen_aligned_sentlist
        func = gen_aligned_sentlist
        # args = (inlist, srclang, tgtlang,)
        args = (
            list1,
            self.srclang,
            self.tgtlang,
            0.4,
        )

        # qthread_func_w_progressbar = QThreadFuncWithQProgressBar()
        qthread_func_w_progressbar = QThreadFuncWithQProgressBar(self)

        # qthread_func_w_progressbar.outdata_ready.connect(receive_out)
        qthread_func_w_progressbar.outdata_ready.connect(self.set_senttab)

        logger.debug("qthread_func_w_progressbar")
        qthread_func_w_progressbar(func, args)

        # ====================

        # thread:
        # 1 self.obj = worker.Worker(text1, text2)  # no parent!
        # self.obj1 = Worker1(list1, self.srclang, self.tgtlang, 0.4)  # no parent!  # noqa
        # self.thread1 = QThread()  # no parent!

        # 2 - Connect Worker`s Signals to Form method slots to post data.
        # self.obj1.tabdata_ready.connect(self.set_senttab)  #

        # 3 - Move the Worker object to the Thread object
        # self.obj1.moveToThread(self.thread1)

        # 4 - Connect Worker Signals to the Thread slots
        # self.obj1.finished.connect(self.thread1.quit)

        # 5 - Connect Thread started signal to Worker operational slot method
        # self.thread1.started.connect(self.obj1.get_tabdata)

        # * - Thread finished signal will close the app if you want!
        # self.thread.finished.connect(app.exit)

        # 6 - Start the thread
        # time.sleep(2)
        # self.thread1.start()

    def dispmsg(self):
        """Display a message."""
        # self.anchorValid = True  # carry out in adjustment of anchor tab only when anchorValid == True  # noqa
        # self.anchorValid1 = False
        # self.anchorValid2 = False
        # self.anchorValid3 = False
        try:
            # a = int(self.lRowValue.text())
            self.lrowno = int(self.lineEdit_lrow.text())
            self.anchorValid1 = True
        except (ValueError, TypeError) as exc:
            logger.debug("self.lrowno exc %s ", exc)
            self.lrowno = "Invalid"
            self.anchorValid1 = False

        try:
            # b = int(self.rRowValue.text())
            self.rrowno = int(self.lineEdit_rrow.text())
            self.anchorValid2 = True
        except (ValueError, TypeError) as exc:
            logger.debug("self.rrowno exc %s ", exc)
            self.rrowno = "Invalid"
            self.anchorValid2 = False

        try:
            self.merit = float(self.lineEdit_merit.text())
            self.anchorValid3 = True
        except (ValueError, TypeError) as exc:
            logger.debug("self.merit exc %s ", exc)
            self.merit = "Invalid"
            self.anchorValid3 = False

        anchormsg = "LRow#: %s, RRow#: %s, Merit: %s" % (
            self.lrowno,
            self.rrowno,
            self.merit,
        )  # noqa
        # self.labelAddition.setText("Addition: " +str(sum))
        # self.dispLabel.setText(sum)
        # logger.debug(" sum %s ", sum)
        self.dispLabel.setText(anchormsg)
        logger.debug(" anchormsg %s ", anchormsg)
        logger.debug(
            "dispmsg self.anchorValid1123: %s %s %s ",
            self.anchorValid1,
            self.anchorValid2,
            self.anchorValid3,
        )  # noqa

    # help_about
    def help_about(self):
        """Ptextpad About pop up."""
        QMessageBox.about(
            self,
            "About Ptextpad",  # 2017
            """<html><head/><body><p><span style=" font-weight:600; color:#0000ff;">Ptextpad (formerly Neualigner) </span><span style=" color:#0000ff;"> v %s</span></p><p><span style=" color:#0000ff;">Coffeeware 2022 mu qq41947782. All rights reserved.</span></p><p><span style=" color:#0000ff;">This application can be used to perform dual text alignments</span>.</p></body></html>"""
            % __version__,
        )  # noqa

        # <p>Python %s - Qt %s - PyQt %s on %s
        # % (__version__, platform.python_version(),
        # QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def not_implemented(self):
        """Not implemented popup."""
        QMessageBox.about(
            self,
            "Sorry",
            """<html><head/><body><p><span style=" color:#0000ff;">Not implemented/fixed yet, stay tuned. </span></p></body></html>""",
        )  # noqa

    def split_cell(self):
        """Split cell."""
        if self.tabWidget.currentIndex() == 2:
            logger.debug("tab index %s ", self.tabWidget.currentIndex())
            self.tableView_2.delegate.commitAndCloseEditor()
        elif self.tabWidget.currentIndex() == 3:
            logger.debug("tab index %s ", self.tabWidget.currentIndex())
            self.tableView_3.delegate.commitAndCloseEditor()

    # test2b.py in pyqt
    def test_for_insert(self):  # from my own stackoverflow answer
        """Test insert."""
        logger.debug("tab index %s ", self.tabWidget.currentIndex())
        if self.tabWidget.currentIndex() == 1:  # 2nd tab

            # self.tableView_2.delegate.commitAndCloseEditor()
            index = self.tableView_2.currentIndex()
            # item = self.tableView_2.tablemodel.data(index, Qt.DisplayRole)
            # qDebug("item %s " % item)
            logger.debug(
                " tableView_2.currentIndex: %s %s",
                index.row(),
                index.column(),
            )  # noqa

            # if self.tableView_2.delegate.editor:
            self.tableView_2.delegate.editor.insertPlainText(
                " +2foo+ "
            )  # QTextEdit  # noqa
            self.tableView_2.tablemodel.dataChanged.emit(index, index)

            logger.debug("myarray:%s ", self.tableView_2.myarray[:4])
        elif self.tabWidget.currentIndex() == 2:  # 3rd tab
            logger.debug("tab index %s ", self.tabWidget.currentIndex())
            # self.tableView_3.delegate.commitAndCloseEditor()
            index = self.tableView_3.currentIndex()

            # item = self.tableView_3.tablemodel.data(index, Qt.DisplayRole)
            # delegate = self.tableView_3.delegate
            # qDebug("item %s " % item)
            # if self.tableView_3.delegate.editor:
            self.tableView_3.delegate.editor.insertPlainText(" +3foo+ ")
            self.tableView_3.tablemodel.dataChanged.emit(index, index)

            # delegate.editor.insertPlainText (" +3foo+ ")

            logger.debug("myarray:%s ", self.tableView_3.myarray)
        # index = self.currentIndex()
        # item = self.tablemodel.data(index, Qt.DisplayRole)


def main():
    """main."""
    # from stream_to_logger import StreamToLogger
    # send stderr to log tab

    # stderr_logger = logging.getLogger("STDERR")

    # pipe to log Tab (3)
    # TODO fix stream_to_logger.StreamToLogger crash
    # sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)

    mainapp = QApplication(sys.argv)

    # SPLASH = QSplashScreen(QPixmap("images/blueocean.png"))
    # http://lzxz1234.github.io/python/2015/02/03/pyqt-develop-err-log.html noqa
    # splash_pix = QPixmap("resources/splash.png")
    # splash = QSplashScreen(QPixmap("images/blue-ocean.png"))

    splash_pix = QPixmap("images/blue-ocean.png")

    # splash = QSplashScreen(splash_pix)

    # splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash = QSplashScreen(splash_pix)
    progressBar = QProgressBar(splash)
    progressBar.setAlignment(Qt.AlignCenter)
    progressBar.setFixedWidth(splash_pix.width())
    splash.setMask(splash_pix.mask())

    splash.show()

    splash.showMessage(rf"\n\Ptextpad {__version__} loading, it may take a while...")

    # SPLASH.showMessage("Loaded, coming up...")
    # from detect_lang import detect_lang

    # detect_lang("this is english")
    # from reanchor_selected_rows import reanchor_selected_rows

    t = QElapsedTimer()
    t.start()
    progressBar.setMaximum(1000)
    while t.elapsed() < 1000:
        progressBar.setValue(t.elapsed())

    mainapp.processEvents()

    myapp = MyWindow()
    splash.finish(myapp)
    myapp.show()
    sys.exit(mainapp.exec_())


if __name__ == "__main__":
    main()
