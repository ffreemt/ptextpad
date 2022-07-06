# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fetch_url.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

# ~ from PyQt4 import QtCore, QtGui
from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)

except AttributeError:

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(914, 645)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit.setDragEnabled(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.goButton = QtGui.QPushButton(self.centralwidget)
        self.goButton.setMinimumSize(QtCore.QSize(28, 28))
        self.goButton.setMaximumSize(QtCore.QSize(28, 28))
        self.goButton.setAutoFillBackground(True)
        self.goButton.setObjectName(_fromUtf8("goButton"))
        self.horizontalLayout_2.addWidget(self.goButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.textBrowser = QtGui.QTextEdit(self.centralwidget)
        self.textBrowser.setAutoFillBackground(True)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout_3.addWidget(self.textBrowser)
        self.sendButton = QtGui.QPushButton(self.centralwidget)
        self.sendButton.setObjectName(_fromUtf8("sendButton"))
        self.verticalLayout_3.addWidget(self.sendButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 914, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", " Url ", None))
        self.label_2.setText(_translate("MainWindow", " Xpath ", None))
        self.lineEdit.setWhatsThis(
            _translate(
                "MainWindow",
                "The url for the bilingual page you wish to extract. For example, http://www.voachinese.com/a/bilingual-news-20170119/3682842.html",
                None,
            )
        )
        self.lineEdit.setText(
            _translate(
                "MainWindow",
                "http://www.voachinese.com/a/bilingual-news-20170119/3682842.html",
                None,
            )
        )
        self.lineEdit_2.setWhatsThis(
            _translate(
                "MainWindow",
                "Xpath is a way to specify part of a webpage and can be easily obtained, for example, by the Firebug extension in Firefox. Typical xpath are: //body or //*[@id='content'. If you have no idea, just leave it blank in which case //body will be use. It will like produce some undesired stuff. But we can remove them later on.",
                None,
            )
        )
        self.lineEdit_2.setText(_translate("MainWindow", "//body", None))
        self.goButton.setText(_translate("MainWindow", "Go", None))
        self.sendButton.setText(
            _translate("MainWindow", "Send to Anchor Tab and close this page", None)
        )
