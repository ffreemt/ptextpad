"""Realign selected rows."""
import logging

from .list_to_selected_rows import list_to_selected_rows
from .realign_sent_list import realign_sent_list

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def realign_selected_rows(self, srclang="english", tgtlang="chinese"):
    """
    Realign selected rows.

    Calling seq: realign_selected_rows(self.tableView_3)

    self.tabWidget.currentIndex() == 2:  # senttab
        (self.tableView_3)
    """

    indices = self.tableview.selectionModel().selectedRows()

    rows = []
    for elm in indices:
        rows += [elm.row()]
    LOGGER.info("Seleced rows: %s ", rows)

    currindex = self.tableview.currentIndex()
    currentrow = currindex.row()

    # select last continuous bacth of rows
    rows = list(list_to_selected_rows(rows, currentrow))
    if rows is None:
        LOGGER.warning(" list_to_selected_rows is None, exiting...")
        return None

    # save before removal
    srclist = []
    tgtlist = []

    for elm in rows:
        srclist += [self.tablemodel.arraydata[elm][0]]
        tgtlist += [self.tablemodel.arraydata[elm][1]]

    srclist0, tgtlist0 = realign_sent_list(
        srclist, tgtlist, srclang=srclang, tgtlang=tgtlang
    )  # noqa

    reversed_rows = list(reversed(rows))  # list(reversed(range(x,y)))
    LOGGER.info("Seleced rows reversed_rows: %s ", reversed_rows)

    if reversed_rows:
        # LOGGER.debug("arradata: %s", self.tablemodel.arraydata)  # to be removed  # noqa
        # remove reversed_rows in the tablemodel
        self.tablemodel.layoutAboutToBeChanged.emit()
        for elm in reversed_rows:
            self.tablemodel.arraydata = (
                self.tablemodel.arraydata[:elm] + self.tablemodel.arraydata[elm + 1:]
            )  # noqa okok

        self.tablemodel.layoutChanged.emit()
        LOGGER.info("Removed.")

        # update with realigned sents with srclist0, tgtlist0
        # insert at rows[0]+1 in reverse order

        LOGGER.debug("srclist0: %s, tgtlist0: %s", srclist0, tgtlist0)

        if len(srclist0) != len(tgtlist0):
            LOGGER.warning(
                "len(srclist0) != len(tgtlist0): Something has gone wrong..."
            )
        len0 = len(srclist0)

        self.tablemodel.layoutAboutToBeChanged.emit()
        pos = rows[0]  # insert at rows[0] in reverse order
        for elm in reversed(range(len0)):
            # temp = [srclist0[elm], tgtlist[elm], '']
            # self.tablemodel.arraydata.insert(pos, temp)
            self.tablemodel.arraydata.insert(pos, [srclist0[elm], tgtlist0[elm], ""])
        self.tablemodel.layoutChanged.emit()
        LOGGER.debug(" %s, %s inserted after %s ", srclist0, tgtlist0, pos)
