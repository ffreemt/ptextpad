r"""Convert list to csv (writer = csv.writer(filehandle.

delimiter='\t',  doublequote=False, escapechar='\\')).

file1 = r'D:\dl\Dropbox\shuangyu_ku\txt-books\newsen.txt'
file2 = r'D:\dl\Dropbox\shuangyu_ku\txt-books\newszh.txt'

text1 = load_text(file1)
text2 = load_text(file2)

paras = texts_to_anchored_paras(text1, text2)

list_to_csv(paras)
"""
import csv
import logging
import os

from logzero import logger


def list_to_csv(paras, filepath="tmpcsv.txt"):
    """List to csv (writer = csv.writer(filehandle,
    delimiter='\t',  doublequote=False, escapechar='\\')).
    """
    if filepath != "tmpcsv.txt":
        if os.path.exists(filepath):
            logger.warning(" File %s exists, exiting...", filepath)

    with open(filepath, "wt", encoding="utf-8") as filehandle:
        # writer = csv.writer(filehandle)
        writer = csv.writer(
            filehandle, delimiter="\t",
            doublequote=False,
            escapechar="\\"
        )
        # writer = csv.writer(filehandle, delimiter='\t')
        # writer = csv.writer(filehandle, dialect='excel-tab')

        for elm in paras:
            writer.writerow(elm)
    logger.debug(" file %s written", filepath)
