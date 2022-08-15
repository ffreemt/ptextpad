"""help_manual"""
# pylint: disable=line-too-long

import logging
import os
from pathlib import Path

from PyQt5.QtGui import QIcon

# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def help_manual():
    """Ptextpad Manual pop up."""
    # import os
    msg = QMessageBox()
    msg.setWindowTitle("Ptextpad/Neualigner Docs")
    msg.setWindowIcon(QIcon("images/Anchor-48.png"))
    msg.setIcon(QMessageBox.Information)
    msg.setText(
        """<html><head/><body><p><span style=" font-size:10pt; font-weight:600; font-style:italic; color:#0000ff;">Ptextpad </span><span style=" font-size:10pt; color:#0000ff;"/><span style=" font-size:10pt; font-weight:600; color:#0000ff;">Howto</span></p><p><span style=" color:#0000ff;">In short, load files, click SetAnchor, click Align, export files (csv, tmx) as needed.</span></p><p><span style=" color:#0000ff;">Detailed instructions will be furnished, soon.</span></p>

        <p><span style=" color:#0000ff;">导出的文件在同目录下的 aligned 目录里。表格的单元可双击编辑或单击再按F2编辑。一般的Ctrl+C、Ctrl+V、Ctrl+Z、Ctrl+X等剪贴快捷键都可用。</span></p>

        <p><span style=" color:#0000ff;">表格单元的大小可用鼠标调节。</span></p>

        <p><span style=" color:#0000ff;">表格的拆分：
          <ul> <li>可在编辑模式（双击或单击再按F2）下将光标置于希望拆分的位置，再按Ctrl+S。
          <li>或在编辑模式下在同一行的左右两个单元里希望拆分的多处键入|||，再点击拆分按钮（工具栏里上下两个箭头的按钮，右数第二个）；可多次点击。每一次点击拆分一对|||或一个|||。

          <li> File的右列为空时，Ptextpad会将左列视为双语混合文件，点击自动打钉钮后， Ptextpad会将其分离成源语言及目标语言并送至打钉卡（Anchor tab）。

          </ul></span></p>
        </body></html>"""
    )  # noqa

    msg.setInformativeText(
        """<html><head/><body><p>

        <p><span style=" color:#0000ff;">阅读 ｒｅａｄｍｅ.html?</span></p>

        </body></html>"""
    )  # noqa
    msg.setDetailedText(
        "Click Yes to browser the readme.html file in your default browser, or click No to do nothing."
    )  # NOQA

    # Add the standard buttons "Ok" and "Cancel"
    # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # noqa  # noqa

    # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)  # noqa
    msg.setDefaultButton(QMessageBox.No)

    ret_val = msg.exec_()
    if ret_val == QMessageBox.Yes:
        # os.startfile("readme.html")

        readmefile = "readme.html"
        file = __file__
        # readmefile in the parent directory of this file
        currdir = os.path.split(os.path.abspath(file))[0]
        paredir = os.path.split(currdir)[0]

        LOGGER.debug("curr dir, par dir: %s, %s", currdir, paredir)

        # filepath = os.path.join(paredir, readmefile)  # noqa

        # filepath = os.path.join(currdir, readmefile)  # noqa
        # filepath = os.path.abspath(filepath)
        # LOGGER.debug(" readme.html: %s", filepath)

        readmefile = "index.html"
        pp_dir = Path(__file__).parent.parent
        pp_dir = Path(__file__).parent
        filepath = Path(pp_dir, "singlehtml/index.html")

        try:
            os.startfile(filepath)  # noqa
        except Exception as exc:
            LOGGER.warning("os.startfile(filepath) error: %s", exc)
            try:
                os.startfile(paredir)
            except Exception as exc:
                LOGGER.debug("os.startfile(paredir) error: %s", exc)
                LOGGER.debug(" Cant open the file nor the dir...something is wrong.")

    # return ret_val
