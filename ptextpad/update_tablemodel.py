"""Update a cell or layout of a tablemodel.

update_cell(model, row, col)
update_layout(model, data: list)
"""
import numpy as np


def update_cell(model, row=0, col=0, value=""):
    """Update cell (row, col) of tablemodel model)."""
    model.arraydata[row][col] = value
    index = model.createIndex(row, col)
    model.dataChanged.emit(index, index)


def update_layout(model, data=[["text1", "text2", "metric"], ["", "", ""]]):
    """Update tablemodel model with data: list."""
    model.layoutAboutToBeChanged.emit()
    model.arraydata = np.array(data).tolist()
    model.layoutChanged.emit()
