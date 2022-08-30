"""Fetch content from url."""
import logging

# ~ from PyQt4.QtGui import QMainWindow, QIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

# import urlxpathtestmainwindow_ui  # okok
import ptextpad.fetch_url_ui

from .fetch_xpath import fetch_xpath
from .text_to_paras import text_to_paras

# import requests
# import requests_cache

# from PyQt4.QtCore import QAbstractTableModel, Qt
# from PyQt4.QtGui import *
# from PyQt4.QtGui import QMainWindow, QTableView, QVBoxLayout, QLabel, QPushButton, QApplication, QIcon


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# requests_cache.configure()


# class MyWindow(QtGui.QMainWindow, Ui_MainWindow):
# class MyWindow(QMainWindow, Ui_MainWindow):  # from  urlxpathtestmainwindow_ui import Ui_MainWindow  okok
# class MyWindow(QMainWindow, urlxpathtestmainwindow_ui.Ui_MainWindow):  # import  urlxpathtestmainwindow_ui okok
class FetchURL(
    QMainWindow, ptextpad.fetch_url_ui.Ui_MainWindow
):  # import  urlxpathtestmainwindow_ui okok
    """Test."""

    def __init__(self, parent=None):
        # QtGui.QWidget.__init__(self, parent)
        # super(MyWindow, self).__init__(parent)
        super(FetchURL, self).__init__(parent)

        self.page = ""

        self.setupUi(self)
        self.setWindowTitle("Pagefetcher")
        # self.setWindowIcon(QtGui.QIcon('images/Anchor-48.png'))
        # self.setWindowIcon(QtGui.QIcon('Info-48.png'))
        self.setWindowIcon(QIcon("images/Info-48.png"))
        # self.pushButton.clicked.connect(self.fetch_page)
        self.goButton.clicked.connect(self.fetch_page)

    def fetch_page(self):
        """Fetch a url page."""
        url = "http://www.voachinese.com/a/bilingual-news-20170119/3682842.html"
        xpath = "//*[@id='content']"

        url = self.lineEdit.text()
        xpath = self.lineEdit_2.text()

        LOGGER.debug("url type: %s, xpath type %s", type(url), type(xpath))

        url = str(url)
        xpath = str(xpath)

        if url is not None:
            url = url.strip()
        if xpath is not None:
            xpath = xpath.strip()

        if not url:
            return None

        LOGGER.debug("url: %s, xpath: %s", url, xpath)

        # LOGGER.debug(" true or false %s", not (url[:7] == 'http://' or url[:7] == 'https://'))

        # http:// https://
        if not (url[:7] == "http://" or url[:7] == "https://"):
            url = "http://" + url
            LOGGER.debug("url missting prefix http:// or https://")

        self.lineEdit.setText(url)
        self.lineEdit_2.setText(xpath)

        if xpath:
            xpath = str(xpath).strip()
            xpath = xpath.replace('"', "'")

        if not xpath:
            xpath = "//body"

        LOGGER.debug("url: %s, xpath: %s", url, xpath)

        page = fetch_xpath(url, xpath)

        # resp = requests.get(url)
        # resp.encoding = 'utf-8'
        # page = resp.text

        # LOGGER.debug("Page fetched: %s", page)

        # textStatus.setText(
        # self.textBrowser.textStatus.setText(page)

        page0 = "\n\n".join(text_to_paras(page))
        self.textBrowser.append(page0)
        self.page = page0
