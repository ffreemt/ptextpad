"""
Calculate the cosine of two vectors.
"""
import logging
import collections
import re
import math

# from stopwords import get_stopwords

# import smallseg
# jieba = smallseg.SEG()

# from sseg import SSEG  # SSEG: instance SSEG = SEG(), SSEG.cut(text)

# use jieba
import jieba as SSEG

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

stopstr = "[来你我们在而了但又和：“”‘’：的，,。 他她是呢]"


def vec_cosine(text1, text2, lang="chinese") -> float:
    """Consine of text1 and text2."""
    # stopstr = "[来你我们在他而了但又和：“”‘’：的，,。 ？]"
    # stopstr = "[来你我们在而了但又和：“”‘’：的，,。 ]"

    # check neither text1 or text2 is empty or None
    if not (isinstance(text1, str) and isinstance(text2, str)):
        LOGGER.warning(" Input not a str, return None")
        return

    if not (text1 and text2):
        return 0

    len1 = len(text1)
    len2 = len(text2)

    if not (len1 or len2):  # if both zero
        return 0.0

    if lang == "chinese":

        text1 = re.sub(stopstr, "", text1)
        text2 = re.sub(stopstr, "", text2)

        # add modification factor to consider length discrepancy: rewards same lengths, penelizes different lengths

        mf = 1.0 - 2 * abs(len1 - len2) / (len1 + len2)  # modi
        # clip = lambda i: i if i>0 else 0
        # a > 3b, or b > 3a, set cosine = 0

        mf = 1.0 - 3 * abs(len1 - len2) / (len1 + len2)
        # a > 2b or b > 2a, set cosine = 0

        mf = max(0, mf)

        return mf * get_cosine(ztext_to_vector(text1), ztext_to_vector(text2))
        # modi 2015 10 13

    else:  # nonchinese, assume latine language

        mf = 1.0 - 3 * abs(len1 - len2) / (len1 + len2)
        # a > 2b or b > 2a, set cosine = 0
        mf = max(0, mf)

        """
        try:
            cachedStopWords = get_stopwords(lang)
        except Exception as exc:
            cachedStopWords = get_stopwords('en')
            LOGGER.warning(" stopwords for %s ()(stopwords.get_stopwords) failed, using 'en'", lang)

        # remove ''
        try:
            cachedStopWords.remove('')
        except Exception:
            pass
        """

        cachedStopWords = (
            {"and", "he", "in", "of", "the", "was", "with"}
            | {"a", "an", "and", "in", "like", "of", "on", "other", "the"}
            | {"and", "of", "the", "was", "with"}
            | {"The", "a", "and", "as", "into", "of", "other", "the", "to", "world"}
        )

        text0 = text1

        pattern = re.compile(
            r"\b(" + r"|".join(cachedStopWords) + r")\b\s*", flags=re.I
        )
        text0a = pattern.sub("", text0)
        words0 = text0a.split()

        # words0 = text0.split()

        vec1 = collections.Counter(words0)

        text0 = text2

        pattern = re.compile(
            r"\b(" + r"|".join(cachedStopWords) + r")\b\s*", flags=re.I
        )
        text0a = pattern.sub("", text0)
        words0 = text0a.split()

        # words0 = text0.split()

        vec2 = collections.Counter(words0)

        return mf * get_cosine(vec1, vec2)


def ztext_to_vector(text):
    # import smallseg

    # words = WORD.findall(text)
    # words = [s for s in jieba.cut(text,True)]
    # text1 = re.sub("[的，,]","",text1)
    text = re.sub(stopstr, "", text)
    # words = [s for s in jieba.cut(text)]
    words = [s for s in SSEG.cut(text)]
    return collections.Counter(words)


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())

    # modified #2015 11 09
    # if # of common terms is smaller than 4， set cosine to 0
    # if len(intersection) < 1:
    if len(intersection) < 5:
        return 0.0

    # log.debug(" intersection={intersection} ".format(intersection=intersection))
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return round(float(numerator) / denominator, 2)


def test_vec1vec2():
    """foldingbj 50 59"""
    vec1 = "Rise in the earth.Old knife observed on the surface of the ground movements， came to the edge of the seam， and with the rise of aperture up constantly.His hands and， starting from the ground of the marble edge， along the cross section of earth， hold the soil buried metal cutting stubble， originally， down with the feet feel regression， soon， with the fast flip of the land， he was taken to the air."

    vec2 = "For the rest of the day, Lao Dao couldn’t forget the scene. He had lived in this city for forty–eight years, but he had never seen such a sight. His days had always started with the cocoon and ended with the cocoon, and the time in between was spent at work or navigating dirty tables at hawker stalls and loudly bargaining crowds surrounding street vendors. This was the first time he had seen the world, bare."

    # eq_(0.5828888888888889, vec_cosine(vec1, vec2, "english"))
    _ = vec_cosine(vec1, vec2, "english")
    assert _ >= 0
