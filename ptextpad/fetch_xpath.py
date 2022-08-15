'''Fetch content from url in xpath.'''
# based on etymonline

import logging
from io import StringIO
import requests

# import lxml
# import re
# import requests_cache

import chardet

from lxml import etree
# import codecs

from .element_to_string import element_to_string

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17'

# requests_cache.configure()


def fetch_xpath(url='url', xpath='xpath', file_=None):
    '''Obtain the content of url with xpath.

    write to file if specified.

    >>> url = 'http://www.wordthink.com/analogous/'
    >>> url = 'https://www.wordnik.com/words/analogous'
    >>> xpath = "//h1[contains(.,'analogous')]"
    >>> fetch_xpath(url, xpath).strip()
    'analogous'
    '''
    LOGGER.debug(" url: %s  xpath: %s ", url, xpath)

    if not (isinstance(url, str) or isinstance(xpath, str)):
        LOGGER.warning(' Input not string, exiting...')
        return None

    parser = etree.HTMLParser()

    # resp = requests.get(url)
    resp = requests.get(url, headers={'User-Agent': UA})
    # LOGGER.debug(" resp.text: {} ".format(resp.text))

    # LOGGER.debug(" resp.from_cache: %s ", resp.from_cache)

    encoding = chardet.detect(resp.content[:1000])
    resp.encoding = encoding

    try:
        if file_:
            #  noqa if isinstance(file_, basestring): try:   basestring except NameError: basestring = str
            if isinstance(file_, str):
                with open(file_, 'w') as fileh:
                    fileh.write(resp.text)
    except Exception as exc:
        LOGGER.warning("Writing to file failed...: %s", exc)

    with StringIO(resp.text) as fileh:
        tree = etree.parse(fileh, parser)

    # print( element_to_string( tree.getroot() ))
    # LOGGER.debug(element_to_string( tree.getroot() ))

    # write to tmpfile
    # tmpfile = 'etymtmp.html'
    # with codecs.open(tmpfile,"w", encoding="utf8") as f:
        # f.write(resp.text)

    # doc = tree.getroot()
    # el = doc.xpath(xpath)

    # el = tree.xpath(xpath)
    elm = tree.xpath(xpath)

    # LOGGER.debug(" len(elm): %s ", len(elm))
    if len(elm) > 0:
        output = element_to_string(elm[0])
        return output
    else:
        output = None
    # output = output.replace('"', "'")


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()
# file = r'D:\dl\Dropbox\mat-dir\snippets-mat\selenium\fetch_xpath.py'
# exec(open(file).read())
