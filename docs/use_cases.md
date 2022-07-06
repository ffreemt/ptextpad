使用案例及操作示范
==============================

英中双语单文件
--------------------------

以双语《呼啸山庄》第一章为例。（Wuthering_Heights_ch1_zh-en.txt 文件可以在程序目录里的 test_files\files_for_testing_load目录里找到。）

    呼啸山庄

    艾米莉·勃朗特


    第一章


    一八○一年。我刚刚拜访……
    ……比起来是多么擅长交际啊，这可真是惊人。

    Wuthering Heights

    Emily Bront


    Chapter 1

    1801—I have just returned...
    ...astonishing how sociable I feel myself compared with him.

此例模拟章章对照的双语资料。段段对照的双语资料以此类推。

首先启动Neualigner。

* 载入文件

.. |setanchorbut| image:: _static/setanchorbut.png
    :width: 20pt

.. |alignbut| image:: _static/alignbut.png
    :width: 20pt

.. |setmerits| image:: _static/setmerits.png
    :width: 20pt

点击载入文件1（快捷键Ctrl+1），文件2留空，点击自动打钉操作（|setanchorbut|），Neualigner会对双语文件做分离处理。

.. image:: _static/usecase1loading.png
    :width: 500px
    :align: center
    :alt: 载入文件

* 自动打钉

自动打钉的结果并不理想。（自动打钉键在单文件双语载入时是做分离键使用的。）

.. image:: _static/usecase1autoanchor.png
    :width: 500px
    :align: center
    :alt: 自动打钉

我们用手动打钉。

* 手工打钉（微调）

    * 下猛药大幅调节，按空格将行数上屏

先点击选定第3行左列。再按空格键。“3”被置入LRow处。

.. image:: _static/usecase1LRow3.png
    :width: 500px
    :align: center
    :alt: 第3行左列

滚动到英文处的Chapter 1处。点击选定第27行右列。再按空格键。“27”被置入RRow处。

.. image:: _static/usecase1RRow27.png
    :width: 500px
    :align: center
    :alt: 第27行右列

Merit置为1。

.. image:: _static/usecase1Merit1.png
    :width: 500px
    :align: center
    :alt: 第27行右列

按回车键对3-27进行打钉后：

.. image:: _static/usecase13-27.png
    :width: 500px
    :align: center
    :alt: 进行3-27打钉

往下滚动到27行处。选定左右表单元（先点击28行左列，再按住Ctrl键点击27行右列），再按空格键。27、28上屏：

.. image:: _static/usecase28-27.png
    :width: 500px
    :align: center
    :alt: 进行28-27打钉

* 回车打钉

按回车键打钉：


.. image:: _static/usecase28anchor.png
    :width: 500px
    :align: center
    :alt: 进行28-28打钉


* 固定已经对好的段落

可以看到，第29行已经对好，可以顺便点击指标开关键（|setmerits|）打钉。

.. image:: _static/usecase29anchor.png
    :width: 500px
    :align: center
    :alt: 进行29-29打钉

* 句句对齐

点击对齐键（|alignbut|)句句对齐。完成后会自动跳至句卡（Sents Tab）。滚动目测一下可以发现92行处的脚注导致从第84行开始的位移。

.. image:: _static/usecase1footnote.png
    :width: 500px
    :align: center
    :alt: 脚注导致位移

先合并（Mergeup）左列的83、84行、再删除84行：

.. image:: _static/usecase1row83-84merge.png
    :width: 500px
    :align: center
    :alt: 合并83、84行

将【You might as well leave a stranger with a brood of tigers!'】一句上移至行号小于含脚注的行号。并删掉一些重复的句子。

.. image:: _static/usecase1rowfoornoteadj.png
    :width: 500px
    :align: center
    :alt: 含脚注的行号

先点击行号85，在按住Ctrl后点击行号89，选定85-89行

.. image:: _static/usecase1rowfoornote85-89.png
    :width: 500px
    :align: center
    :alt: 选定85-89行

点击对齐键（|alignbut|）选择性对齐85-89行



* 导出tmx记忆库


直接剪贴源语言文本及目标语言文本
-----------------------------------

以《呼啸山庄》双语第一章为例。（当然也可以在下面的第一步和第二步直接从两个独立的文件载入源语言文本及目标语言文本。）

启动Neualigner。

* 在文件卡（File tab）左列贴入源语言文本

* 在文件卡（File tab）右列贴入目标语言文本

* 自动打钉

* 微调及手动打钉

* 句句对齐

* 选择数行后重新句句对齐

