"""
Reanchor selected rows.

"""
import logging

from .list_to_selected_rows import list_to_selected_rows

# from realign_sent_list import realign_sent_list
from .texts_to_anchored_paras import texts_to_anchored_paras

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


# def realign_selected_rows(self, srclang='english', tgtlang='chinese'):
def reanchor_selected_rows(self, srclang="english", tgtlang="chinese"):
    """Re-anachor selected rows.

    Calling seq: reanchor_selected_rows(self.tableView_2)

    self.tabWidget.currentIndex() == 1:  # anchortab
        (self.tableView_2)

    Refer to realign_selected_rows
    """
    # indices = self.tableview.selectionModel().selectedRows()
    # self is already a tableview
    indices = self.selectionModel().selectedRows()

    rows = []
    for elm in indices:
        rows += [elm.row()]
    LOGGER.info("Seleced rows: %s ", rows)

    # currindex = self.tableview.currentIndex()
    currindex = self.currentIndex()
    currentrow = currindex.row()

    # select last continuous bacth of rows
    rows = list(list_to_selected_rows(rows, currentrow))
    if rows is None:
        LOGGER.warning(" list_to_selected_rows is None, exiting...")
        return None

    # save before removal
    srclist = []
    tgtlist = []
    # collect non empty rows (paras)
    for elm in rows:
        if self.tablemodel.arraydata[elm][0].strip():
            srclist += [self.tablemodel.arraydata[elm][0]]
        if self.tablemodel.arraydata[elm][1].strip():
            tgtlist += [self.tablemodel.arraydata[elm][1]]
    text1 = "\n".join(srclist)
    text2 = "\n".join(tgtlist)

    LOGGER.debug("text1: %s", text1)
    LOGGER.debug("text2: %s", text2)

    # anchor texts_to_anchored_paras
    listnew = texts_to_anchored_paras(text1, text2, tgtlang=tgtlang)
    # an nx3 list
    LOGGER.debug("realigned listnew %s", listnew)

    reversed_rows = list(reversed(rows))  # list(reversed(range(x,y)))
    LOGGER.info("Seleced rows reversed_rows: %s ", reversed_rows)

    # remove reversed_rows in the tablemodel
    if reversed_rows:
        # LOGGER.debug("arradata: %s", self.tablemodel.arraydata)  # to be removed  # noqa
        self.tablemodel.layoutAboutToBeChanged.emit()
        for elm in reversed_rows:
            self.tablemodel.arraydata = (
                self.tablemodel.arraydata[:elm] + self.tablemodel.arraydata[elm + 1:]
            )  # noqa okok

        self.tablemodel.layoutChanged.emit()
        LOGGER.info("Removed.")

        # update with listnew
        # insert at rows[0]+1 in reverse order

        if len(listnew) <= 0:
            LOGGER.warning("len(listnew) <= 0: Something has gone wrong...")
        len0 = len(listnew)

        self.tablemodel.layoutAboutToBeChanged.emit()
        pos = rows[0]  # insert at rows[0] in reverse order
        for elm in reversed(range(len0)):
            LOGGER.debug("*** %s, %s", elm, listnew[elm])
            # temp = [srclist0[elm], tgtlist[elm], '']
            # self.tablemodel.arraydata.insert(pos, temp)
            self.tablemodel.arraydata.insert(pos, listnew[elm])
        self.tablemodel.layoutChanged.emit()
        LOGGER.debug(" %s inserted after %s ", listnew, pos)
