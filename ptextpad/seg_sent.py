# coding: utf-8
'''
Segments text to sents.

Uss seg_zhsent and seg_xysent ang detect_lang.
'''

import logging

# from nose.tools import (eq_, with_setup)

from .detect_lang import detect_lang
# from seg_zhsent import seg_zhsent
from .seg_chinese import seg_chinese as seg_zhsent
from .seg_xysent import seg_xysent
from .text_to_paras import text_to_paras

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def seg_para(para, lang='english'):
    if lang == 'chinese':
        sents = seg_zhsent(para)
    else:
        sents = seg_xysent(para, language=lang)
    return sents


def seg_sent(text, lang='english'):
    '''Segment text, lang='en').

    output: []
    '''
    # lang = detect_lang(text)

    # remove para indent
    # if lang == 'chinese':
    text = text.replace('\u3000', '')

    paras = text_to_paras(text)
    sents = []
    if lang == 'chinese':
        for para in paras:
            sents += seg_zhsent(para)
    else:
        for para in paras:
            sents0 = seg_xysent(para, language=lang)
            if sents0 is None:
                return None
            sents += sents0
    return sents


def my_setup():
    logging.basicConfig(level=logging.DEBUG)


# @with_setup(my_setup)
def test_zh():
    '''
    ===test_zh===
    '''
    text = '''总局批准吉非替尼片等3个国产仿制药品上市

　　2017年01月12日 发布

　　近日，国家食品药品监督管理总局批准抗癌药吉非替尼片、抗艾滋病药依非韦伦片以及富马酸替诺福韦二吡呋酯片的国产仿制药品上市。

　　吉非替尼是表皮生长因子受体（EGFR）酪氨酸激酶抑制剂，通过选择性阻断表皮生长因子受体信号传导路径，从而抑制肿瘤生长、转移和血管生成。依非韦伦是人类免疫缺陷病毒1型（HIV-1）选择性非核苷类逆转录酶抑制剂，口服生物利用度高，半衰期长，临床用于HIV-1感染的成人、青少年和3岁以上儿童的抗病毒联合治疗，临床疗效较为确切。富马酸替诺福韦二吡呋酯是一种核苷酸逆转录酶抑制剂(NtRTI)，可与其他抗逆转录病毒药物联用治疗HIV 1感染。上述产品在相关治疗领域均为一线常用治疗药物。'''  # noqa

    expected = 7
    sents = seg_sent(text)
    LOGGER.debug(" sents: %s ", sents)
    out = len(sents)

    assert expected == out


# @with_setup(my_setup)
def test_en():
    '''
    === test_en ===
    '''
    text = ''' Posted by Daniel Jordon on Jan 13th, 2017 // No Comments

Baidu logoInvestment analysts at Sanford C. Bernstein initiated coverage on shares of Baidu, Inc. (NASDAQ:BIDU) in a research note issued on Wednesday. The firm set an “underperform” rating and a $150.00 price target on the stock. Sanford C. Bernstein’s price objective points to a potential downside of 15.53% from the company’s current price.'''  # noqa

    expected = 4
    sents = seg_sent(text)
    out = len(sents)

    LOGGER.debug(" sents: %s", sents)

    assert expected == out


# @with_setup(my_setup)
def test_russian():
    '''
    === test_russian ===
    '''
    text = ''' My name is Masha - Меня зовут Маша
Play Здравствуйте! Меня зовут Маша. Мне восемнадцать лет. Я живу в России. Я из города Липецк. Липецк находится в четырехстах километрах к югу от Москвы. Но по Российским меркам это не очень большое расстояние. Я окончила школу, когда мне было 16 лет, хотя в России большинство учеников выпускаются из школы в семнадцать. Это потому, что мой день рождения приходится на первую часть учебного года. Он в декабре. Но мне всегда нравилось быть младшей ученицей в классе. Не знаю почему. В школе я начала учить английский. На сегодняшний день я изучаю английский уже более десяти лет.'''

    expected = 4
    sents = seg_sent(text)
    if sents is None:
        LOGGER.warning("\n\n")
        LOGGER.warning("Segmentation not successful, probably because the necessary file is not available.")
        lang = detect_lang(text)
        LOGGER.warning(" Try to copy **%s.pickle** to the lib dir or the current dir...\n\n", lang)
        return None

    out = len(sents)

    LOGGER.debug(" sents: %s", sents)

    assert expected == out


# @with_setup(my_setup)
def test_fr():
    '''
    === test_fr ===
    '''
    text = ''' Quand Emmanuel Macron chasse sur les terres du Front national
21h42, le 13 janvier 2017, modifié à 22h34, le 13 janvier 2017

Quand Emmanuel Macron chasse sur les terres du Front national
Emmanuel Macron donnera un meeting à Lille, samedi.@ DENIS CHARLET / AFP
Partagez sur :

Le candidat à la présidentielle écume le terrain et n'hésite pas à aller chercher les électeurs FN dans les fiefs frontistes. Avec une stratégie de prédilection : provoquer la discussion.

En politique, personne ne vient plus à Hénin-Beaumont par hasard. Depuis les législatives de 2012 et la guerre qui a opposé Jean-Luc Mélenchon à Marine Le Pen dans cette commune du Nord-Pas-de-Calais-Picardie, la ville est devenue un symbole de l'ancrage du Front national dans certains territoires. La victoire de Steeve Briois aux municipales de 2014 a achevé de la classer dans la catégorie des "fiefs" frontistes. Alors forcément, lorsqu'Emmanuel Macron choisit de s'y rendre, cela n'a rien d'une coïncidence et tout d'un calcul.

Le candidat à la présidentielle s'y est rendu vendredi en fin de journée pour remettre des médailles du Travail à des salariés de Metro. Plus tôt dans l'après-midi, il était à Lens, où le Front national signe aussi de jolis scores (20% des suffrages au premier tour de l'élection municipale il y a trois ans). Le 4 février, c'est Marine Le Pen qu'il ira défier directement à Lyon. La présidente du Front national avait déjà prévu de faire sa rentrée politique dans la capitale des Gaules lorsque le fondateur d'En Marche! a annoncé qu'il allait y tenir un meeting. Le Palais des sports de Gerland, réservé pour l'occasion, peut accueillir 7.000 personnes.'''

    expected = 18
    sents = seg_sent(text)
    if sents is None:
        LOGGER.warning("\n\n")
        LOGGER.warning("Segmentation not successful, probably because the necessary file is not available.")
        lang = detect_lang(text)
        LOGGER.warning(" Try to copy **%s.pickle** to the lib dir or the current dir...\n\n", lang)
        return None

    out = len(sents)

    LOGGER.debug(" sents: %s", sents)

    assert expected == out
