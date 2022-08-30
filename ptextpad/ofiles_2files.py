"""Open files."""
import logging
import os
from typing import Optional, Tuple

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def ofiles_2files(file1, file2=None, check=True) -> Optional[Tuple[str, str, str]]:
    """Open files.

    out12,out1,out2 = ofiles_2files(file1,file2=None,check=True)

    out12,out1,out2 = ofiles_2files(eninfile,zhinfile)
    out12,out1,out2 = ofiles_2files( 'file1', check=False)

    if check=True: check the existence of file1 and file2

    file1, file2, full path filename or relative path filename
    ofile: commonprefix of fntrunks of file1 and file2 (trunk of file2 if commonprefix is empty)
        outdirname = file2's dir
    """
    # logger.setLevel(logging.DEBUG)
    # imp.reload(logging) # needed in ipython

    if not file2:
        file2 = file1

    if check:
        if not os.path.exists(file1):
            logger.info(" file {} does not exists...".format(file1))
            return None

        if not os.path.exists(file2):
            logger.info(" file {} does not exists...".format(file2))
            return None

    file1basename = os.path.basename(file1)
    file2basename = os.path.basename(file2)
    if os.path.commonprefix([file1basename, file2basename]):
        if (
            file1basename == file2basename
        ):  # file1 and file2 are the same, or only one file is provided
            ofile = os.path.splitext(file2basename)[0]
        else:
            ofile = os.path.commonprefix([file1basename, file2basename])
    else:
        ofile = os.path.splitext(file2basename)[0]

    #
    indirname = os.path.dirname(os.path.abspath(file2))

    # outdirname, make a dir aligned if not already existed
    outdirname = indirname + "\\aligned\\"
    os.makedirs(outdirname, exist_ok=True)

    out12 = os.path.join(outdirname, ofile + "_12.txt")
    out1 = os.path.join(outdirname, ofile + "_1.txt")
    out2 = os.path.join(outdirname, ofile + "_2.txt")
    return out12, out1, out2
