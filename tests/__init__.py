"""Init.

need to test

ls ptextpad/c*.py | xargs -I {} pytest {}
    ptextpad\clapse_text.py
     ptextpad.csv_to_list:csv_to_list.py:38

ls ptextpad/d*.py | xargs -I {} pytest {}

    pytest ptextpad/data_for_updating.py
        8 failed, fixed eq_

pytest ptextpad/docx_to_txt.py::test_
pytest ptextpad/docx_to_txt.py::test_doc

ptextpad/element_to_string.py  #  no tests
ptextpad/epub_to_txt.py

pytest ptextpad/fetch_url.py  ptextpad/fetch_xpath.py  # no tests

pytest ^
ptextpad/gen_aligned_sentlist.py ^
ptextpad/get_anchor_set.py ^
ptextpad/get_para.py

pytest ^
ptextpad/help_manual.py ^
ptextpad/html2txt.py ^
ptextpad/insert_itag.py ^
ptextpad/lists_to_tmx4n.py ^
ptextpad/list_to_csv.py # no tests ^
ptextpad/loadtext.py ^
ptextpad/load_file_as_text.py ^
ptextpad/load_text.py # no tests ^
ptextpad/load_zipped.py # FIXME ^
ptextpad/logging_progress.py  # no tests

dir /b ptextpad|grep "^[m-o].*\.py$"
minifuncwrapper.py  #  no tests
msg_popup.py  # no tests
myqprogressbar.py  # "
mytable.py  # "
ofiles_2files.py  # "

dir /b ptextpad|grep "^[p-q].*\.py$"
para_cosine_rev.py  # no tests
para_gc.py  #
pdf_to_text.py  # FIXME
pdf_to_text_h.py  # FIXME
popup_anchortab_dirty.py  # no tests
post_process.py  #  no tests
ptextpad.py  #  no tests
pyqtlogging.py  # no tests
qthread_func_with_progressbar.py  #  1 passed

dir /b ptextpad|grep "^[rs].*\.py$"
realign_list.py
realign_selected_rows.py
remove_selected_rows.py
resource_rc.py
seg_chinese.py
seg_sent.py
seg_xysent.py
seg_zhsent.py
send_to_table.py
sep_chinese.py
srtass_to_txt.py
srt_to_txt.py
stream_to_logger.py

dir /b ptextpad|grep "^[rs].*\.py$" | xargs -I {} pytest ptextpad/{}

fd "^r.*\.py" -d2
ptextpad\realign_list.py
ptextpad\realign_selected_rows.py
ptextpad\remove_selected_rows.py
ptextpad\resource_rc.py

fd "^r.*\.py" -d2 |sed "s/\\\\/\\\\\\\/" | xargs -I {} pytest {}

fd "^r.*\.py" -d2 -x pytest

fd -tf ".*\.py$" -d1 ptextpad -x pytest

pytest.ini
[pytest]
python_files = *.py

sep_chinese.py OK
ptextpad\seg_sent.py: FIXME
ptextpad\seg_xysent.py: FIXME

pytest ptextpad\seg_zhsent.py  no tests
pytest ptextpad\send_to_table.py  FIXME
pytest ptextpad\sep_chinese.py  1 passed in 7.61s
pytest ptextpad\srtass_to_txt.py  FIXME
pytest ptextpad\srt_to_txt.py  # 3 failed, 1 passed, 1 warning in 8.95s
pytest ptextpad\stream_to_logger.py  no tests

"""
