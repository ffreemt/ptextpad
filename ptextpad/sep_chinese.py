# coding: utf-8
"""Separate chinese and nonchinese."""
import logging

from .chardet_file import chardet_file
from .detect_lang import detect_lang
from .en_zh_separation import en_zh_separation
from .fetch_xpath import fetch_xpath
from .text_to_paras import text_to_paras
from .zip_longest_middle import zip_longest_middle

# from tqdm import tqdm

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def sep_chinese(text, startlen=30):
    """
    in: text, paras
    out: list of two tuples, srclang, tgtlang
    align starts: when len() >= starlen)

    sep_chinese_logger = logging.getLogger('sep_chinese')
    sep_chinese_logger.setLevel(logging.INFO)
    """
    paras = text_to_paras(text)
    # sep_list = zip(en_zh_separation, paras)
    sep_list = [en_zh_separation(elm) for elm in paras]

    # find the starting anchor
    # for ith, elm in tqdm(enumerate(paras)):
    for ith, elm in enumerate(paras):
        sep = en_zh_separation(elm)
        len0 = len(elm) - sep

        # if min(sep, len0)==0, sep0 = max(sep, len0)
        # else sep0 = min(sep, len0)
        min0 = min(sep, len0)
        sep0 = max(sep, len0) if min0 == 0 else min0
        if sep0 >= startlen:
            # determin chinese is srclang (left) or tgtlang (right)
            if min0 == 0:  # single language in one para
                if sep == 0:
                    tgtlang = (
                        "chinese" if detect_lang(elm) == "chinese" else "nonchinese"
                    )  # noqa
                    srclang = (
                        "nonchinese" if tgtlang == "chinese" else "chinese"
                    )  # noqa
                else:  # sep = len(elm)
                    srclang = (
                        "chinese" if detect_lang(elm) == "chinese" else "nonchinese"
                    )  # noqa
                    tgtlang = (
                        "nonchinese" if srclang == "chinese" else "chinese"
                    )  # noqa
            else:  # two languages in one para
                if detect_lang(elm[:sep]) == "chinese":
                    srclang = "chinese"
                    tgtlang = "nonchinese"
                else:
                    srclang = "nonchinese"
                    tgtlang = "chinese"
            break

    # LOGGER.info(" !!! srclang, tgtlang: %s, %s", srclang, tgtlang)

    list0 = []
    starti = ith
    # LOGGER.debug(">>>Preample...")
    for idxi in range(starti):  # trival preamble, just put in right palce
        sep0 = sep_list[idxi]
        front_part = paras[idxi][:sep0]
        back_part = paras[idxi][sep0:]
        if detect_lang(front_part) == "chinese":
            if srclang == "chinese":
                list0.append([front_part, back_part])
            else:
                list0.append([back_part, front_part])
        else:
            if srclang == "chinese":
                list0.append([back_part, front_part])  # noqa
            else:
                list0.append([front_part, back_part])

    # LOGGER.debug(" list0 %s", list0)

    # LOGGER.debug(">>>Start at %s...", starti)
    # real sep and clapse
    auxflag = (
        -1
    )  # left 0, right 1, if cur - prv==0, colelct,  cur - prv==1, switch to right, cur - prv==-1, switch to left and align  # noqa
    # itembuff = []
    lbuffer = []
    rbuffer = []
    # 0:1, left index:right index
    indexprev = 1

    # for ith, elm in enumerate(tqdm(paras[starti:])):
    for ith, elm in enumerate(paras[starti:]):
        # LOGGER.debug("******** ith %s, pos %s, elm %s", ith, ith + starti, elm)  # noqa
        sep0 = sep_list[ith + starti]
        front_part = elm[:sep0]
        back_part = elm[sep0:]

        # use the langer part to detect chinese
        if sep0 > len(elm) - sep0:
            front_part_lang = (
                "chinese" if detect_lang(front_part) == "chinese" else "nonchinese"
            )  # noqa
            back_part_lang = (
                "nonchinese" if front_part_lang == "chinese" else "chinese"
            )  # noqa
        else:
            back_part_lang = (
                "chinese" if detect_lang(back_part) == "chinese" else "nonchinese"
            )  # noqa
            front_part_lang = (
                "nonchinese" if back_part_lang == "chinese" else "chinese"
            )  # noqa

        # LOGGER.debug(" +++!!! front_part_lang  %s ", front_part_lang)

        # front_part: proc_fbpart(front_part, front_part_lang)
        def proc_fbpart(front_part, front_part_lang):
            """
            process front, back part
            """
            nonlocal srclang, tgtlang, indexprev, auxflag, lbuffer, rbuffer

            # LOGGER.debug("  (in proc_fbpart) f/b part: %s ", front_part)
            if front_part_lang == srclang:
                indexcurr = 0
            else:
                indexcurr = 1
            # LOGGER.debug(" indexcurr: %s", indexcurr)

            auxflag = indexcurr - indexprev
            # LOGGER.debug("auxflag: %s", auxflag)

            if (
                auxflag == -1
            ):  # -1, 0, 1 -- -1: collet, 0 collect left or right, 1, swtich to right  # noqa
                # LOGGER.debug(" collect and align ")

                for zipelm in zip_longest_middle(
                    lbuffer, rbuffer, fillvalue=""
                ):  # noqa
                    list0.append(list(zipelm))
                lbuffer = [front_part]
                rbuffer = []

            elif auxflag == 0:
                # LOGGER.debug(" append lbuffer or rbuffer ")
                if indexcurr == 0:
                    lbuffer += [front_part]
                else:
                    rbuffer += [front_part]
            else:  # auxflag = 1
                rbuffer += [front_part]
            indexprev = indexcurr  # prepare for the next round

        if front_part.strip():  #
            proc_fbpart(front_part, front_part_lang)
            # LOGGER.debug("<<<<< 1111111 front_part <<<<< 1111111")
        if back_part.strip():  #
            proc_fbpart(back_part, back_part_lang)
            # LOGGER.debug("<<<<< 2222222 back_part <<<<< 2222222")

        # LOGGER.debug(" lbuffer, rbuffer, list0: \n>%s, \n>%s, \n>%s ", lbuffer, rbuffer, list0)  # noqa

    # process postamble, equivalent to auxflag = -1
    # LOGGER.debug(" process postamble ")
    # LOGGER.debug("zipped lbuffer, rbuffer: %s ", list(zip_longest_middle(lbuffer, rbuffer, fillvalue='')))  # noqa
    for zipelm in zip_longest_middle(lbuffer, rbuffer, fillvalue=""):
        list0.append(list(zipelm))

    return list0


# pep8/flake8/pylint filename
# nosetests -v --nologcapture
def test_minitext():
    """Test minitext, text =."""
    text = """

中国时间: 09:23 2017年01月22日星期日
双语新闻
双语新闻(2017年1月19日)
2017.01.19 22:49

    美国之音


    奥巴马说 美国一切都会好的

奥巴马总统星期三在他最后一次白宫记者会上，努力让对政府换届感到担忧的美国民众放心。他说：“我相信这个国家。我相信美国人民。我相信人们身上的善多于恶。”

白宫记者们的提问涉及到奥巴马给陆军情报分析员切尔西·曼宁减刑等议题。 奥巴马简单地回答了这些问题，最后他还很具体地回答了他是如何向两个女儿解释美国大选结果的。

奥巴马总统说，玛利亚和萨沙对于共和党候选人川普击败他支持的民主党候选人希拉里·克林顿感到失望，不过令他自豪的是，她们表现得很坚强、爱国，而不是愤世嫉俗。

奥巴马总统承认，他在公开场合表现出的冷静和随和跟他私下的表现并不一样，私下他也会骂人，也像其他人一样会愤怒和沮丧。他说：“不过我深信，（作为一个国家） 一切都会好的，但我们必须奋斗，必须努力，不能觉得理所当然，我相信你们会帮我们做到。”

Obama Says US 'Is Going to Be OK'

At his final news conference as president Wednesday, Barack Obama sought to reassure those Americans anxious about the change of administrations: “I believe in this country. I believe in the American people. I believe that people are more good than bad.”

White House reporters questioned Obama about his decision to shorten the prison term of former Army intelligence analyst Chelsea Manning, and other topics. The president fielded those easily, but took his time answering the final query, about how he discussed the results of the U.S. election with his two teenaged daughters, Sasha and Malia.

Obama said Malia and Sasha were disappointed by Republican Donald Trump's defeat of his preferred candidate, Democrat Hillary Clinton, just as he and first lady Michelle were, but that he is proud of them because they are resilient, patriotic and not cynical.

The president admitted his public persona - calm and cheerful - is not quite the way he feels when behind closed doors.

“I curse more than I do in public, and sometimes I get mad and frustrated, like everybody else does," he said. "But at my core, I think we’re going to be okay [as a country]. We just have to fight for it, we have to work for it, and not take it for granted, and I know that you will help us do that.”

韩国法庭裁定没有足够证据逮捕三星副总裁

韩国一家法庭星期四决定不批准对三星集团负责人的逮捕令，这个案件与朴槿惠总统弹劾案有关。
"""  # NOQA
    exp1 = 14
    exp1 = 18
    list0 = sep_chinese(text)
    LOGGER.debug("text: %s", text)
    LOGGER.debug(" sep_chinese output: %s", list0)
    assert exp1 == len(list0)

    exp2 = "韩国法庭裁定没有足够证据逮捕三星副总裁"
    # assert exp2 == list0[12][0]
    assert exp2 == list0[-2][0]

    exp3 = "Obama Says US 'Is Going to Be OK'"
    # assert exp3 == list0[6][1]
    assert exp3 == list0[10][0]

    # return list0


def xxtest_file1():
    r"""test_file1.

    D:\dl\Dropbox\shuangyu_ku\txt-books\德伯家的苔丝(中英文对照).txt'
    """
    file = r"D:\dl\Dropbox\shuangyu_ku\txt-books\德伯家的苔丝(中英文对照).txt"
    text = open(
        file, "r", encoding=chardet_file(file, 20000), errors="ignore"
    ).read()  # NOQA

    exp1 = []
    list0 = sep_chinese(text)

    # LOGGER.debug("text: %s", pagevoa)
    LOGGER.debug(" sep_chinese output: %s", list0)
    assert exp1 == list0


def xxxtest_voaxpath_content():
    """
    test_voaxpath_content, pagevoa1 = fetch_xpath(urlvoa, "//*[@id='content']")
    """
    urlvoa = r"http://www.voachinese.com/a/bilingual-news-20170119/3682842.html"  # NOQA
    # voaurl = urlvoa
    pagevoa = fetch_xpath(urlvoa, "//*[@id='content']")
    # parasvoa = text_to_paras(pagevoa)

    exp1 = [
        ["双语新闻", ""],
        ["双语新闻(2017年1月19日)", ""],
        ["2017年1月19日 22:49", ""],
        ["美国之音", ""],
        ["分享", ""],
        ["分享到脸书", ""],
        ["分享到推特", ""],
        ["分享到谷歌+", ""],
        ["电邮本文", ""],
        ["打印", ""],
        ["奥巴马说  美国一切都会好的", ""],
        [
            "奥巴马总统星期三在他最后一次白宫记者会上，努力让对政府换届感到担忧的美国民众放心。他说：“我相信这个国家。我相信美国人民。我相信人们身上的善多于恶。”",
            "Obama Says US 'Is Going to Be OK'",
        ],
        [
            "白宫记者们的提问涉及到奥巴马给陆军情报分析员切尔西·曼宁减刑等议题。 奥巴马简单地回答了这些问题，最后他还很具体地回答了他是如何向两个女儿解释美国大选结果的。",
            "At his final news conference as president Wednesday, Barack Obama sought to reassure those Americans anxious about the change of administrations: “I believe in this country. I believe in the American people. I believe that people are more good than bad.”",
        ],
        [
            "",
            "White House reporters questioned Obama about his decision to shorten the prison term of former Army intelligence analyst Chelsea Manning, and other topics. The president fielded those easily, but took his time answering the final query, about how he discussed the results of the U.S. election with his two teenaged daughters, Sasha and Malia.",
        ],
        [
            "",
            "Obama said Malia and Sasha were disappointed by Republican Donald Trump's defeat of his preferred candidate, Democrat Hillary Clinton, just as he and first lady Michelle were, but that he is proud of them because they are resilient, patriotic and not cynical.",
        ],
        [
            "奥巴马总统说，玛利亚和萨沙对于共和党候选人川普击败他支持的民主党候选人希拉里·克林顿感到失望，不过令他自豪的是，她们表现得很坚强、爱国，而不是愤世嫉俗。",
            "The president admitted his public persona - calm and cheerful - is not quite the way he feels when behind closed doors.",
        ],
        [
            "奥巴马总统承认，他在公开场合表现出的冷静和随和跟他私下的表现并不一样，私下他也会骂人，也像其他人一样会愤怒和沮丧。他说：“不过我深信，（作为一个国家） 一切都会好的，但我们必须奋斗，必须努力，不能觉得理所当然，我相信你们会帮我们做到。”",
            '“I curse more than I do in public, and sometimes I get mad and frustrated, like everybody else does," he said. "But at my core, I think we’re going to be okay [as a country]. We just have to fight for it, we have to work for it, and not take it for granted, and I know that you will help us do that.”',
        ],
        [
            "韩国法庭裁定没有足够证据逮捕三星副总裁",
            "Samsung Indictment Reversal Setbacks South Korean Impeachment Trial",
        ],
        [
            "韩国一家法庭星期四决定不批准对三星集团负责人的逮捕令，这个案件与朴槿惠总统弹劾案有关。",
            "A South Korean court Thursday dismissed an arrest warrant request for the head of the Samsung Group, in a case that could affect the impeachment trial of President Park Geun-hye.",
        ],
        [
            "三星集团副总裁李在镕在拘留所被关押了14个小时后，首尔中区法院裁定，目前没有足够证据为检察官提出的行贿、挪用款项和作伪证的指控提供法律依据。",
            "Jay Y. Lee, the vice chairman of Samsung Electronics Co. was held for 14 hours in a detention facility before the Seoul Central District Court ruled there was not enough evidence at this time to justify prosecutors’ charges of bribery, embezzlement and perjury.",
        ],
        [
            "",
            "“The court's decision to reject arrest warrant is very regrettable, but we will steadily continue the investigation by taking necessary measures,\" said a spokesman of the prosecutor's office.",
        ],
        [
            "检察官办公室发言人说，“法庭驳回逮捕令的决定令我们深感遗憾，但是我们会采取必要措施，继续进行调查。”",
            "Lee is suspected of paying President Park's influential friend Choi Soon-sil $36 million in return for the president’s help to secure the approval of a state-run pension fund for a 2015 merger of two Samsung affiliates.",
        ],
        [
            "李在镕涉嫌向朴槿惠总统的密友崔顺实支付了3600万美元，换取总统的帮助，让国营退休基金批准2015年三星两个附属机构的合并案。",
            "The court’s decision on the Samsung case could be a setback for prosecutors in the presidential impeachment trial also underway.",
        ],
        ["法庭这一裁决对于负责朴槿惠弹劾案的检察官一方是一个挫败。", "OMG!"],
        ["美语", "美语怎么说（52）："],
        ["OMG!美语 Homesick!", ""],
        ["OMG!美语 Oil Painting!", ""],
        ["OMG!美语 Catch Up!", ""],
        ["OMG!美语 Knit Scarf!", ""],
        ["OMG!美语 Wear The Basics!", ""],
        ["美语怎么说", ""],
        ["Man-day 男人空间", "神秘的圣诞老人"],
        ["美语怎么说（51）：Secret Santa ", ""],
        ["美语怎么说（50）：The Witches ", "巫师搞怪"],
        ["美语怎么说（49）: Government Shutdown ", "政府关门"],
        ["", "美语怎么说（48）: "],
        ["New Name 命名风波", "YOLO"],
        ["美语", "YOLO"],
        ["美语 第三十八课", "YOLO"],
        ["美语 第三十七课", "YOLO"],
        ["美语 第三十六课", "YOLO"],
        ["美语 第三十五课", "YOLO"],
        ["美语 第三十四课", ""],
    ]  # noqa
    list0 = sep_chinese(pagevoa)
    LOGGER.debug("text: %s", pagevoa)
    LOGGER.debug(" sep_chinese output: %s", list0)
    assert exp1 == list0


def xxtest_voaxpath_body():
    """
    test_voaxpath_body, pagevoa1 = fetch_xpath(urlvoa, "//body")
    """
    urlvoa = r"http://www.voachinese.com/a/bilingual-news-20170119/3682842.html"  # NOQA
    pagevoa1 = fetch_xpath(urlvoa, "//body")
    # parasvoa1 = text_to_paras(pagevoa1)

    exp1 = [
        [
            "if (top.location === self.location) { //if not inside of an IFrame",
            'var utag_data={entity:"VOA",language:"Mandarin",language_service:"VOA Mandarin",short_language_service:"MAN",property_id:"521",platform:"Responsive",platform_short:"R",runs_js:"Yes",page_title:"双语新闻(2017年1月19日)",page_type:"3682842",page_name:"双语新闻(2017年1月19日)",short_headline:"双语新闻(2017年1月19日)",long_headline:"双语新闻(2017年1月19日)",headline:"双语新闻(2017年1月19日)",content_type:"Article",pub_year:"2017",pub_month:"01",pub_day:"19",pub_hour:"14",pub_minute:"49",pub_weekday:"Thursday",byline:"美国之音, ",categories:"bilingual-news",slug:"bilingual-news-20170119",section:"双语新闻",english_section:"bilingual-news",search_results:"No",article_uid:"3682842"};',
        ],
        ['var renderGtm = "true";', ""],
        ['if (renderGtm === "true") {', ""],
        [
            "(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-N8MP7P');",
            "",
        ],
        ["}", ""],
        ["}", ""],
        [
            "if(typeof(TealiumTagFrom)==='function' && typeof(TealiumTagSearchKeyword)==='function') {",
            "无障碍链接",
        ],
        [
            "var utag_from=TealiumTagFrom();var utag_searchKeyword=TealiumTagSearchKeyword();",
            "跳转到内容",
        ],
        ["", "跳转到导航"],
        ["", "跳转到检索"],
        ["", "检索"],
        ["", "检索"],
        ["", "其他语言网站"],
        ["", "检索"],
        ["", "检索"],
        ["", "广播音频"],
        ["", "电视节目"],
        ["", "主页"],
        ["", "美国"],
        ["", "中国"],
        ["", "分类新闻"],
        ["", "美国"],
        ["", "中国"],
        ["", "台湾"],
        ["", "港澳"],
        ["", "国际"],
        ["", "经贸"],
        ["", "法律"],
        ["", "人权"],
        ["", "军事"],
        [
            'if(utag_searchKeyword!=null && utag_searchKeyword!==\'\' && utag_data["search_keyword"]==null) utag_data["search_keyword"]=utag_searchKeyword;if(utag_from!=null && utag_from!==\'\') utag_data["from"]=TealiumTagFrom();}',
            "文化",
        ],
        [
            '(function(a,b,c,d){ a="https://tags.tiqcdn.com/utag/bbg/voa-pangea/prod/utag.js"; b=document;c="script";d=b.createElement(c);d.src=a;d.type="text/java"+c;d.async=true; a=b.getElementsByTagName(c)[0];a.parentNode.insertBefore(d,a); })();',
            "教育",
        ],
        ["宗教", "科技"],
        ["", "劳工"],
        ["", "环境"],
        ["", "健康"],
        ["", "体育"],
        ["", "娱乐"],
        ["", "热点专题"],
        ["", "互动图解：南中国海七十年风云录"],
        ["", "美中关系"],
        ["", "美国总统大选和权力交接"],
        ["", "台海两岸关系"],
        ["", "年终报道"],
        ["", "美国之音专访"],
        ["", "国会报道"],
        ["", "南中国海争端"],
        ["", "美中关系书评"],
        ["", "朝鲜核问题"],
        ["", "法律窗口"],
        ["", "纪念六四"],
        ["", "评述中国文革"],
        ["", "中国“肃贪”政治"],
        ["VOA", "卫视"],
        ["VOA", "卫视最新视频"],
        ["", "美国观察"],
        ["", "时事大家谈"],
        ["", "焦点对话"],
        ["", "海峡论谈"],
        ["VOA", "卫视完整版"],
        ["", "解密时刻"],
        ["", "国际新闻"],
        ["VOA", "连线"],
        ["", "媒体观察"],
        ["", "小夏看美国"],
        ["", "时事看台"],
        ["", "科技101"],
        ["", "走进美国"],
        ["", "美国万花筒"],
        ["", "您的孩子在美国"],
        ["", "美国专讯"],
        ["OMG", "！美语"],
        ["", "视频"],
        ["", "音频"],
        ["", "上午6-7点广播节目"],
        ["", "上午8-9点广播节目"],
        ["", "下午5-6点广播节目"],
        ["", "晚上6-7点广播节目"],
        ["", "晚上7-8点广播节目"],
        ["", "晚上8-9点广播节目"],
        ["", "晚上9-10点广播节目"],
        ["", "晚上10-11点广播节目"],
        ["VOA", "卫视节目音频"],
        ["", "新闻报道音频"],
        ["", "英语教学音频"],
        ["", "英语教学"],
        ["", "最新内容"],
        ["YOLO", "美语"],
        ["", "双语新闻"],
        ["", "学个词"],
        ["", "美国习惯用语"],
        ["", "礼节美语"],
        ["", "流行美语"],
        ["", "美语咖啡屋"],
        ["", "体育美语"],
        ["", "美语三级跳"],
        ["", "美语训练班"],
        ["", "美语怎么说"],
        ["", "OMG！美语(视频)"],
        ["", "美语怎么说(视频)"],
        ["", "上网办法"],
        ["", "播客"],
        ["", "图片集"],
        ["", "订阅邮件"],
        ["", "美国之音丛书"],
        ["", "登录/注册"],
        ["", "更多"],
        ["VOA", "卫视"],
        ["", "最新节目"],
        ["", "VOA卫视 焦点对话(重播)"],
        ["", "即将开播"],
        ["20:00 - 20:59", "卫视 解密时刻"],
        ["VOA", ""],
        ["21:00 - 22:00", "卫视 海峡论谈"],
        ["VOA", ""],
        ["6:00 - 07:00", "VOA卫视 解密时刻(重播)"],
        ["", "卫视节目"],
        ["《VOA", "卫视》节目介绍"],
        ["", "电视广播节目表"],
        ["", "美国之音"],
        ["YouTube", "美国观察"],
        ["", "时事大家谈"],
        ["", "焦点对话"],
        ["", "媒体观察"],
        ["VOA", "连线"],
        ["更多《VOA卫视》节目... ...", "现场广播"],
        ["", "最新节目"],
        ["", "解密时刻(重播)"],
        ["", "即将开播"],
        ["17:00 - 18:00", "英语教学 时事大家谈(重播)"],
        ["18:00 - 19:00", "国际新闻 焦点对话(重播)"],
        ["19:00 - 20:00", "时事经纬 社论"],
        ["", "其他音频"],
        ["", "24-7中文广播"],
        ["", "新闻报道音频"],
        ["", "英语教学音频"],
        ["VOA", "卫视音频"],
        ["SoundCloud", "频道"],
        ["", "广播节目表"],
        ["", "上一页"],
        ["", "下一页"],
        ["0", "快讯"],
        ["", "上一页"],
        ["VOA", "下一页"],
        ["0", "直播"],
        ["", "中国时间 16:45 2017年3月12日 星期日"],
        ["", "双语新闻"],
        ["", "双语新闻(2017年1月19日)"],
        ["", "2017年1月19日 22:49"],
        ["", "美国之音"],
        ["", "分享"],
        ["", "分享到脸书"],
        ["", "分享到推特"],
        ["", "分享到谷歌+"],
        ["", "电邮本文"],
        ["", "打印"],
        ["", "奥巴马说  美国一切都会好的"],
        [
            "",
            "奥巴马总统星期三在他最后一次白宫记者会上，努力让对政府换届感到担忧的美国民众放心。他说：“我相信这个国家。我相信美国人民。我相信人们身上的善多于恶。”",
        ],
        [
            "",
            "白宫记者们的提问涉及到奥巴马给陆军情报分析员切尔西·曼宁减刑等议题。 奥巴马简单地回答了这些问题，最后他还很具体地回答了他是如何向两个女儿解释美国大选结果的。",
        ],
        [
            "",
            "奥巴马总统说，玛利亚和萨沙对于共和党候选人川普击败他支持的民主党候选人希拉里·克林顿感到失望，不过令他自豪的是，她们表现得很坚强、爱国，而不是愤世嫉俗。",
        ],
        [
            "",
            "奥巴马总统承认，他在公开场合表现出的冷静和随和跟他私下的表现并不一样，私下他也会骂人，也像其他人一样会愤怒和沮丧。他说：“不过我深信，（作为一个国家） 一切都会好的，但我们必须奋斗，必须努力，不能觉得理所当然，我相信你们会帮我们做到。”",
        ],
        ["Obama Says US 'Is Going to Be OK'", "韩国法庭裁定没有足够证据逮捕三星副总裁"],
        [
            "At his final news conference as president Wednesday, Barack Obama sought to reassure those Americans anxious about the change of administrations: “I believe in this country. I believe in the American people. I believe that people are more good than bad.”",
            "韩国一家法庭星期四决定不批准对三星集团负责人的逮捕令，这个案件与朴槿惠总统弹劾案有关。",
        ],
        [
            "White House reporters questioned Obama about his decision to shorten the prison term of former Army intelligence analyst Chelsea Manning, and other topics. The president fielded those easily, but took his time answering the final query, about how he discussed the results of the U.S. election with his two teenaged daughters, Sasha and Malia.",
            "三星集团副总裁李在镕在拘留所被关押了14个小时后，首尔中区法院裁定，目前没有足够证据为检察官提出的行贿、挪用款项和作伪证的指控提供法律依据。",
        ],
        [
            "Obama said Malia and Sasha were disappointed by Republican Donald Trump's defeat of his preferred candidate, Democrat Hillary Clinton, just as he and first lady Michelle were, but that he is proud of them because they are resilient, patriotic and not cynical.",
            "检察官办公室发言人说，“法庭驳回逮捕令的决定令我们深感遗憾，但是我们会采取必要措施，继续进行调查。”",
        ],
        [
            "The president admitted his public persona - calm and cheerful - is not quite the way he feels when behind closed doors.",
            "李在镕涉嫌向朴槿惠总统的密友崔顺实支付了3600万美元，换取总统的帮助，让国营退休基金批准2015年三星两个附属机构的合并案。",
        ],
        [
            '“I curse more than I do in public, and sometimes I get mad and frustrated, like everybody else does," he said. "But at my core, I think we’re going to be okay [as a country]. We just have to fight for it, we have to work for it, and not take it for granted, and I know that you will help us do that.”',
            "法庭这一裁决对于负责朴槿惠弹劾案的检察官一方是一个挫败。",
        ],
        ["Samsung Indictment Reversal Setbacks South Korean Impeachment Trial", "美语"],
        [
            "A South Korean court Thursday dismissed an arrest warrant request for the head of the Samsung Group, in a case that could affect the impeachment trial of President Park Geun-hye.",
            "OMG!美语 Homesick!",
        ],
        [
            "Jay Y. Lee, the vice chairman of Samsung Electronics Co. was held for 14 hours in a detention facility before the Seoul Central District Court ruled there was not enough evidence at this time to justify prosecutors’ charges of bribery, embezzlement and perjury.",
            "OMG!美语 Oil Painting!",
        ],
        [
            "“The court's decision to reject arrest warrant is very regrettable, but we will steadily continue the investigation by taking necessary measures,\" said a spokesman of the prosecutor's office.",
            "OMG!美语 Catch Up!",
        ],
        [
            "Lee is suspected of paying President Park's influential friend Choi Soon-sil $36 million in return for the president’s help to secure the approval of a state-run pension fund for a 2015 merger of two Samsung affiliates.",
            "OMG!美语 Knit Scarf!",
        ],
        [
            "The court’s decision on the Samsung case could be a setback for prosecutors in the presidential impeachment trial also underway.",
            "OMG!美语 Wear The Basics!",
        ],
        ["OMG!", "美语怎么说"],
        ["美语怎么说（52）：", "Man-day 男人空间"],
        ["", "美语怎么说（51）：Secret Santa "],
        ["神秘的圣诞老人", "美语怎么说（50）：The Witches "],
        ["巫师搞怪", "美语怎么说（49）: Government Shutdown "],
        ["政府关门", "New Name 命名风波"],
        ["美语怎么说（48）: ", ""],
        ["YOLO", "美语"],
        ["YOLO", "美语 第三十八课"],
        ["YOLO", "美语 第三十七课"],
        ["YOLO", "美语 第三十六课"],
        ["YOLO", "美语 第三十五课"],
        ["YOLO", "美语 第三十四课"],
        ["", "回页顶"],
        ["", "关注我们"],
        ["", "网上服务"],
        ["", "翻墙信息"],
        ["", "聚合新闻"],
        ["", "播客"],
        ["", "订阅电邮新闻、英语学习教材"],
        ["", "音频"],
        ["", "广播节目音频存档"],
        ["", "新闻音频存档"],
        ["VOA", "卫视音频"],
        ["", "英语音频存档"],
        ["", "应用程序("],
        ["APP)", "美国之音应用程序简介"],
        ["", "新闻应用程序("],
        ["iOS)", "移动流媒体播放器("],
        ["APK)", "非智能手机新闻应用程序"],
        ["", "其他信息"],
        ["", "关于我们"],
        ["", "联系我们"],
        ["", "美国之音宪章"],
        ["", "条款及私隐政策"],
        ["", "网站留言规则"],
        ["", "互联网翻墙指南"],
        ["", "广播理事会("],
        ["BBG)", "美國之音粵語網"],
        ["VOA English", "自由亚洲网站"],
        ["\u0f56\u0f7c\u0f51\u0f0b\u0f61\u0f72\u0f42", "中国时间"],
        ["Media Relations", "//"],
        ["test ie 6, 7, 8", ""],
        ['var div = document.createElement("div");', ""],
        ['div.innerHTML = "<!--[if lte IE 8]><i></i><![endif]-->";', ""],
        ['var isIe8orLower = !!div.getElementsByTagName("i").length;', ""],
        ["if (!isIe8orLower && !navigator.userAgent.match(/Opera Mini/i)) {", ""],
        ['document.getElementsByTagName("body")[0].className += " can-fontface";', ""],
        ["}", ""],
        ["XS", ""],
        ["SM", ""],
        ["MD", ""],
        ["LG", ""],
        ["var bar_data = {", ""],
        [
            '"apiUrl": "http://voa.pangea-cms.com/publisher/zh-CN/api/frontend/itemdata",',
            "",
        ],
        ['"apiId": "3682842",', ""],
        ['"apiType": "1",', ""],
        ['"isEmbedded": "0",', ""],
        ['"cookieName": "cmsLoggedIn",', ""],
        ['"cookieDomain": "www.voachinese.com"', ""],
        ["};", ""],
    ]  # noqa
    list0 = sep_chinese(pagevoa1)
    LOGGER.debug("text: %s", pagevoa1)
    LOGGER.debug(" sep_chinese output: %s", list0)
    assert exp1 == list0
    # return list0


def xxtest_voadual():
    """
    test_voadual D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\neualignerv002\voa_dual.txt"""  # noqa
    filepath = r"D:\dl\Dropbox\mat-dir\snippets-mat\pyqt\Sandbox\neualignerv002\voa_dual.txt"  # noqa
    text = open(
        filepath, "r", encoding=chardet_file(filepath, 20000), errors="ignore"
    ).read()  # NOQA
    tabdata = sep_chinese(text)

    assert 17 == len(tabdata)

    assert tabdata[0], ["" == "from test"]

    exp = [
        "奥巴马总统星期三在他最后一次白宫记者会上，努力让对政府换届感到担忧的美国民众放心。他说：“我相信这个国家。我相信美国人民。我相信人们身上的善多于恶。”",
        "Obama Says US 'Is Going to Be OK'",
    ]  # NOQA

    assert exp == tabdata[9]


if __name__ == "__main__":
    pass
    # my_setup()
    # test_minitext()
