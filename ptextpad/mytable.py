# coding: utf-8
r"""Define mytable.

test_bigfile3a_1.py
pyqt\test2cQPlainTextEdit.py
"""
import sys

import logzero

# from update_list import update_mytable
# from update_list import update_list
from logzero import logger
from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, qDebug  # NOQA
from PyQt5.QtGui import QColor, QFont  # noqa QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHeaderView,
    QLineEdit,
    QPlainTextEdit,
    QShortcut,
    QStyledItemDelegate,
    QTableView,
    QTextEdit,
)
from .data_for_updating import data_for_split0

# logzero.loglevel(10)

ITAG = "|||"

# from plaintextedit import LNTextEdit as QPlainTextEdit  # QPlainTextEdit with line numbers  # NOQA

# from load_paras3a import load_paras
# from load_paras import load_paras

MY_ARRAY = [["", "", ""]]

# defaultdir = r'D:\dl\Dropbox\shuangyu_ku\txt-books'
# defaultfile = r'Folding_Beijing-en.txt'

# defaultdir = r'D:\dl\Dropbox\mat-dir\snippets-mat\pyqt'
# defaultfile = r'notes pyqt tkinter tktable.txt'

# filepath = os.path.join(defaultdir, defaultfile)
# paralist, lenlist = load_paras(filepath)

# MY_ARRAY = [list(elm) for elm in zip(paralist, lenlist)]
# data_list = [

# class MyTable(QFrame):
# ok, will need to instantiate QTableView
# e.g. self.tableview = QTableView(self)


class MyTable(QTableView):  # ok
    """Define Class Mytable."""

    # class MyTable(QTableView):  # ok
    # def __init__(self, *args):
    # def __init__(self, parent=None, myarray=MY_ARRAY, *args):
    # def __init__(self, parent=None, myarray=[['a', 'aa', 0.5]], vh=56, *args):
    # def __init__(self, parent=None, myarray=MY_ARRAY, vh=56, *args):
    # 12*7 = 84,  12 * 8 = 96
    def __init__(self, *args, myarray=MY_ARRAY, vh=84, **kwargs):
        """Init."""
        # def __init__(self, parent=None, myarray=[['', '']], *args):
        # super(MyWindow, self).__init__()
        # super(MyTableView, self).__init__(parent, *args)

        # super(MyTable, self).__init__(parent, *args)
        super().__init__(*args, **kwargs)

        logger.debug("myarray: %s", myarray)

        # self.tablemodel = MyTableModel(MY_ARRAY)
        self.myarray = myarray

        logger.debug("self.myarray: %s", self.myarray)

        self.tablemodel = MyTableModel(self.myarray)

        # wrong wrong!! self.tableview = QTableView(parent)
        # self is already tableView

        # self.tableview.setModel(self.tablemodel)
        self.setModel(self.tablemodel)

        self.delegate = MyDelegate(self)
        self.setItemDelegate(self.delegate)

        # table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        # self.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        # self.horizontalHeader().setResizeMode(QHeaderView.Interactive)  # noqa

        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )  # Interactive=0

        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch=1

        # self.horizontalHeader().setStretchLastSection(True)

        # QHeaderView.Interactive

        self.setWordWrap(True)

        # self.setVisible(False)
        # self.setVisible(True)

        font = QFont("Courier New", 14)
        self.setFont(font)

        self.resizeColumnsToContents()

        # https://stackoverflow.com/questions/40019022/how-do-i-resize-rows-with-setrowheight-and-resizerowtocontents-in-pyqt4
        # self.table.setRowHeight(row, 100)
        # self.resizeRowsToContents()

        # self.resizeColumnsToContents()
        # self.setColumnWidth(0, 450)  #
        # self.setColumnWidth(1, 450)

        # self.setColumnWidth(0, 420)  #

        # table.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)
        # self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        # self.setColumnWidth(1, 400)
        self.setColumnWidth(1, 600)
        self.setColumnWidth(2, 55)

        # verticalHeader->setDefaultSectionSize(24);
        self.verticalHeader().setDefaultSectionSize(vh)
        # self.verticalHeader().setDefaultSectionSize(200)

        # self.horizontalHeader().setDefaultSectionSize(560)
        # self.horizontalHeader().setDefaultSectionSize(560)

        # self.layout = QVBoxLayout(self)
        # self.layout.addWidget(self)

        # self.button1 = QPushButton("Test")

        # self.button1.released.connect(self.test)

        # self.layout.addWidget(self.button1)
        # self.setLayout(self.layout)


class MyTableModel(QAbstractTableModel):
    """Define a model."""

    def __init__(self, datain, parent=None, *args):
        """Init."""
        # super(MyTableModel, self).__init__(parent, *args)
        super().__init__(parent, *args)

        self.header = ["text1", "text2", "metric"]
        self.arraydata = datain

    def rowCount(self, parent):  # NOQA
        """Row."""
        return len(self.arraydata)

    def columnCount(self, parent):  # NOQA
        """columnCount"""
        # return len(self.arraydata[0])
        return 3

    def data(self, index, role):
        """Data."""
        # logger.debug(" self.arraydata: %s", self.arraydata)
        # carefull with logger in this method, lots of traffic
        if not index.isValid():
            return None

        elif not (  # needed, or QFont::fromString: Invalid description '(empty)'
            role == Qt.DisplayRole or role == Qt.EditRole or role == Qt.BackgroundRole or role == Qt.TextAlignmentRole
        ):
            return None

        if role == Qt.TextAlignmentRole:
            return Qt.AlignTop  # works

        # http://stackoverflow.com/questions/13121025/tableview-cell-delegates-qt-backgroundrole
        if role == Qt.BackgroundRole:
            # sgi salmon 	#C67171 198, 113, 113
            # mistyrose 1 (mistyrose) #FFE4E1 255, 228, 225
            # set rows with empty cell in col0 and col1 to salmon QColor(198, 113, 113)

            # col 0 and col 1: set to QColor(255, 228, 225) if one cell or both is empty
            if (
                not (self.arraydata[index.row()][0] and self.arraydata[index.row()][1])
                and index.column() < 2
            ):
                return QColor(255, 228, 225)

            # check col 2's value (merit)
            datafloat = 0.0
            try:
                datafloat = float(self.arraydata[index.row()][2])
            except Exception:  # as exc:
                pass

            if datafloat > 0.0 and index.column() < 2:
                return QColor(Qt.lightGray)  # column=0, 1, 2
            if index.column() == 2:
                if datafloat > 0.0 and datafloat <= 0.33:
                    return QColor(218, 112, 214)  # magenta 255, 0, 255
                    # http://cloford.com/resources/colours/500col.htm
                if datafloat > 0.33 and datafloat < 0.5:
                    return QColor(155, 100, 255)  # orchid 218, 112, 214
                if datafloat >= 0.5 and datafloat < 0.70:
                    return QColor(125, 175, 255)
                if datafloat >= 0.70:  # 1.
                    return QColor(75, 251, 152)  # palegreen 152, 251, 152

            # if index.column() == 2:  # 3rd column merit
            # return QColor(63, 127, 0)
            # return QColor(Qt.lightGray)

            # col 1 cell the same as the cell above, set salmon HERE
            if index.column() == 1 and index.row() > 0:  # starting row1
                rowno = index.row()
                if self.arraydata[rowno][1] == self.arraydata[rowno - 1][1]:
                    return QColor(255, 236, 139)  # sgi salmon (198, 113, 113)
                    # lightgoldenrod 1 	#FFEC8B 	(255, 236, 139)

            return None

        # logger.debug("self.arraydata: %s", self.arraydata)

        # return self.arraydata[index.row()][index.column()]
        if len(self.arraydata) == 0:  # modi 2017 02 24
            return None
        else:
            return self.arraydata[index.row()][index.column()]

    def setData(self, index, value, role=Qt.EditRole):  # noqa
        """Set data."""
        self.arraydata[index.row()][index.column()] = value
        return True

    def flags(self, index):
        """Flag."""
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    # refer to D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\my_test_QCompleter.py
    #
    def headerData(self, col, orientation, role):  # noqa
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]  # col header
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(col + 1)  # row header
        return None


class MyDelegate(QStyledItemDelegate):
    """Mydelegate."""

    # contextMenuRequested = pyqtSignal(object, QPoint)

    def __init__(self, parent=None):  # noqa
        super(MyDelegate, self).__init__(parent)

        # self.cursorpos = -1  # unset flag
        # self.cursormy = None
        self.textcursor = None  # QTextEdit or QPlainTextEdit editor
        self.s_pressed = False
        # self.editor = self.createEditor(parent)  # for split_cell in neualigner.py
        # self.editor = QTextEdit(parent)  # for split_cell in neualigner.py

    def createEditor(self, parent, option, index):  # noqa

        # self.cursormy = None  # unset flag

        # editor = QLineEdit(parent)  # can use editor.cursorPosition()

        # editor = QPlainTextEdit(parent)
        # editor = QTextEdit(parent)

        # for split_cell in neualigner.py/ptextpad

        # self.editor = QTextEdit(parent)
        self.editor = QPlainTextEdit(parent)

        shcut1 = QShortcut("CTRL+S", self.editor, self.commitAndCloseEditor)  # noqa
        # shcut2 = QShortcut("CTRL+Q", self.editor, self.commitAndCloseEditor1)  # noqa

        # self.shortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+S'), parent)
        # self.shortcut.activated.connect(self.commitAndCloseEditor)

        # shcut1.setKey("CTRL+E")
        # shcut1.setKey("CTRL+S")

        # textChanged
        # self.connect(self.editor, SIGNAL("textChanged()"), self.commitAndCloseEditor)

        # self.connect(self.editor, SIGNAL("editingFinished()"), self.commitAndCloseEditor)  # editingFinished() available only in QLineEdit
        # self.cursorpos = editor.cursorPosition()  # cursorPosition for QLineEdit only

        # self.cursormy = QCursor.pos()

        """
        # editor.setContextMenuPolicy(Qt.CustomContextMenu)
        # editor.customContextMenuRequested.connect(
            # self.commitAndCloseEditor)  # !!! right-click  # noqa
        """

        # self.connect(shcut1, SIGNAL("activated()"), self.commitAndCloseEditor)  # ctrl-E

        # not needed?
        # self.connect(self.editor, SIGNAL("activated()"), self.commitAndCloseEditor)  # ctrl-S
        # self.connect(self.editor, SIGNAL("activated()"), self.commitAndCloseEditor1)  # ctrl-Q

        # qDebug(" <createEditor><MyDelegate> self.cursormy: %s " % self.cursormy)
        # qDebug(" <createEditor><MyDelegate> self.textcursor: %s " % self.cursorpos)

        # self.editor.paste()

        # self.editor = editor
        self.index = index
        self.model = index.model()  # MyTableModel

        # qDebug(" run createEditor ")
        logger.debug(" run createEditor ")
        return self.editor

    def commitAndCloseEditor(self):  # noqa
        """Reimplement."""
        # editor = self.sender()
        # qDebug(" <commitAndCloseEditor> editor: %s " % editor)

        # self.cursorpos = editor.cursorPosition()
        # self.textcursor = editor
        # self.cursormy = QCursor.pos()

        # qDebug(" run commitAndCloseEditor ")
        logger.debug(" run commitAndCloseEditor ")

        if isinstance(self.editor, (QTextEdit, QLineEdit, QPlainTextEdit)):
            self.editor.insertPlainText(ITAG)
            # self.emit(SIGNAL("commitData(QWidget*)"), self.editor)
            # self.emit(SIGNAL("closeEditor(QWidget*)"), self.editor)
            self.commitData.emit(self.editor)
            self.closeEditor.emit(self.editor)
            return

        idxi = self.index.row()
        idxj = self.index.column()
        # xxx # tmpdata = data_for_split0(list0, idxi, idxj)

        logger.debug(" == idxi idxj ==  %s, %s", idxi, idxj)
        logger.debug(" ** model.arraydata ** %s ", self.model.arraydata)

        tmpdata = data_for_split0(self.model.arraydata, idxi, idxj)

        logger.debug(" tmpdata [irow, row_numbers, rows to add] %s ", tmpdata)

        # updating
        self.model.layoutAboutToBeChanged.emit()
        # update_mytable(self.model, tmpdata[0], tmpdata[1], tmpdata[2])

        # update_list(self.model.arraydata, tmpdata[0], tmpdata[1], tmpdata[2])  # idxi, row_numbers, rows_to_add

        # logger.debug("\n!!!before pop!!! %s\n", self.model.arraydata)

        self.model.arraydata[tmpdata[0]] = tmpdata[2][0][
            :
        ]  # update instead of pop and insert
        self.model.dataChanged.emit(self.index, self.index)

        # self.model.arraydata.pop(tmpdata[0])  # idxi row
        # logger.debug("\n!!!after pop!!! %s\n", self.model.arraydata)

        # self.model.layoutChanged.emit()
        # self.model.layoutAboutToBeChanged.emit()

        # self.model.arraydata.insert(tmpdata[0], tmpdata[2][0])
        # logger.debug("\n!!!after 1st insert!!! %s\n", self.model.arraydata)

        # self.model.dataChanged.emit(self.index, self.index)  # somehow this is needed for pop and insert at the same row, 1pop+1insert equiv to data change? use update the row instead  # noqa

        self.model.layoutAboutToBeChanged.emit()
        self.model.arraydata.insert(tmpdata[0] + 1, tmpdata[2][1])
        self.model.layoutChanged.emit()

        # logger.debug("\n!!!after 2nd insert!!! %s\n", self.model.arraydata)

        # self.model.layoutChanged.emit()

        logger.debug("\n!!!after layoutCanged!!! %s\n", self.model.arraydata)

        # if isinstance(editor, (QTextEdit, QLineEdit)):
        if isinstance(self.editor, (QTextEdit, QLineEdit, QPlainTextEdit)):
            # self.emit(SIGNAL("commitData(QWidget*)"), self.editor)
            # self.emit(SIGNAL("closeEditor(QWidget*)"), self.editor)

            self.commitData.emit(self.editor)
            self.closeEditor.emit(self.editor)

        # manipulate model data
        # self.index.model.setData(self.index, " 0000 ")  # does not work: 'builtin_function_or_method' object has no attribute 'setData'

        # self.s_pressed = True  # ? needed in inserting "==="
        # manipulate model

        # tmpstr = self.editor.toPlainText()
        tmpstr = str(self.model.data(self.index, Qt.DisplayRole))
        # qDebug("tmpstr %s" % tmpstr)

        # print("tmpstr %s" % tmpstr)
        logger.debug("tmpstr %s", tmpstr)

        # tmpstr = tmpstr.replace(ITAG, CTAG)
        # qDebug("1 tmpstr %s" % tmpstr)

        tmpstr = tmpstr.split(ITAG)

        # print("1 tmpstr %s" % tmpstr)
        logger.debug("1 tmpstr %s", tmpstr)

        # ==== manual updating =======
        # self.model.setData(self.index, tmpstr[0])
        # self.model.dataChanged.emit(self.index, self.index)

        # self.model.layoutAboutToBeChanged.emit()
        # self.model.arraydata.insert(self.index.row()+1, [tmpstr[1], 0, 0])
        # self.model.layoutChanged.emit()

        # prev row
        """
        # if self.index.row() > 0:
            # index0 = self.model.createIndex(self.index.row() - 1, self.index.column())
            # data0 = self.model.data(index0, Qt.DisplayRole)
            # self.model.setData(self.index, self.editor.toPlainText() + '===')
            # self.model.setData(self.index, self.editor.toHtml() + '<div style="width:0px;height:0px;padding:0px;border:10px ridge yellowgreen;"></div>')
            # self.model.setData(index0, str(data0) + ' ===')
            # self.model.dataChanged.emit(index0, self.index)  # noqa
        # else:
            # self.model.setData(self.index, self.editor.toPlainText() + '===')
            # self.model.setData(index0, str(data0) + ' ===')
            # self.model.dataChanged.emit(self.index, self.index)
        """
        # s_pressed = False

    def setEditorData(self, editor, index):  # noqa
        text = str(index.model().data(index, Qt.DisplayRole))

        # editor.setText(text)  # for QLineEdit
        editor.setPlainText(text)  # for QTextEdit and QPlainTextEdit

    def setModelData(self, editor, model, index):  # noqa
        # model.setData(index, editor.text())
        model.setData(index, editor.toPlainText())

        # manipulate model
        # model.setData(index, editor.toPlainText()+'===' )

        # model = index.model()  #

        # cache the cursor for splitdouble in __main__
        cursor = editor.textCursor()
        self.cursorpos = cursor.blockNumber(), cursor.columnNumber()


def main():
    """main."""
    app = QApplication(sys.argv)

    # w = MyWindow()
    # w = MyTable()
    w = MyTable(myarray=[["x", "y", "z"]])

    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
