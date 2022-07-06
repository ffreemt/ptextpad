"""Remove slected rows.

New: use in neualigner as
from remove_selected_rows import delete_rows
from remove_selected_rows import remove_selected_rows

class MyWindow in neualigner.py
self.actionRemoverow.connect(self.remove_rows)

    def remove.rows(self):
        '''Remove selected rows.'''
        if self.tabWidget.currentIndex() == 1:  # anchortab
            remove_selected_rows(self.tableView_2)
            logger.debug("Delete rows on anchortab")
        elif self.tabWidget.currentIndex() == 2:  # sent tab
            remove_selected_rows(self.tableView_3)
            logger.debug("Delete rows on senttab")

Does it work? It works.

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
"""
from logzero import logger


def remove_selected_rows(self):
    r"""Remove selected rows.

    if self.tabWidget.currentIndex() == 1:  # anchortab
        remove_selected_rows(self.tableView_2)
        logger.debug("Delete rows on anchortab")
    elif self.tabWidget.currentIndex() == 2:  # senttab
        remove_selected_rows(self.tableView_3)
        logger.debug("Delete rows on senttab")

    Refer to D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\my_test_delete_selected-rows.py
    """

    indices = self.selectionModel().selectedRows()

    rows = []
    for elm in indices:
        rows += [elm.row()]

    reversed_rows = list(reversed(sorted(rows)))
    logger.info("Seleced rows reversed_rows: %s ", reversed_rows)

    # if selected rows
    if reversed_rows:
        # logger.debug("arradata: %s", self.tablemodel.arraydata)  # to be removed  # noqa
        self.tablemodel.layoutAboutToBeChanged.emit()
        for elm in reversed_rows:
            self.tablemodel.arraydata = self.tablemodel.arraydata[:elm] + self.tablemodel.arraydata[elm + 1:]  # noqa okok

            # self.tablemodel.arraydata = [['0', '0', '0']]  # okok
            # self.tablemodel.arraydata = [[]]  # okok

        self.tablemodel.layoutChanged.emit()
        logger.info("Removed.")
        # logger.debug("**after** arradata: %s", self.tablemodel.arraydata)  # to be removed
        return None
    # logger.debug(" **after** self.tablemodel.arraydata %s", self.tablemodel.arraydata)

    # if none selected, delete the currentIndex row
    index1 = self.selectedIndexes()
    if index1:
        idxi = index1[-1].row()
        # logger.debug("==>arraydata: %s", self.tablemodel.arraydata)  # to be removed
        self.tablemodel.layoutAboutToBeChanged.emit()
        self.tablemodel.arraydata = self.tablemodel.arraydata[:idxi] + self.tablemodel.arraydata[idxi + 1:]  # noqa okok
        self.tablemodel.layoutChanged.emit()
        logger.info("%s-th row removed.", idxi + 1)
        # logger.debug("==>**after** arradata: %s", self.tablemodel.arraydata)  # to be removed

def delete_rows(self):
    """
    Remove selected rows.

    This does not seem to work, need to setup in neualigner.py.
    """

    if self.tabWidget.currentIndex() == 1:  # anchortab
        remove_selected_rows(self.tableView_2)
        logger.debug("Delete rows on anchortab")
    elif self.tabWidget.currentIndex() == 2:  # senttab
        remove_selected_rows(self.tableView_3)
        logger.debug("Delete rows on senttab")
