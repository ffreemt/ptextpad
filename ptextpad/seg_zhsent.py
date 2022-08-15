# -*- coding: utf-8 -*-

# seems written for python3
# A Chinese sentence segment tool
# https://github.com/zsy056/nlp-tools

# senends endfollow
senendsbyte = [
    b"\xe3\x80\x82",
    b"\xef\xbc\x81",
    b"\xef\xbc\x9f",
    b"\xe2\x80\xa6",
    b"~",
    b"\xef\xbd\x9e",
    b"!",
    b"?",
    b".",
    b"\xef\xbc\x8e",
]
senendsbyte = [
    b"\xe3\x80\x82",
    b"\xef\xbc\x81",
    b"\xef\xbc\x9f",
    b"\xe2\x80\xa6",
    b"~",
    b"\xef\xbd\x9e",
    b"!",
    b"?",
]  # ,b'.', b'\xef\xbc\x8e' removed
senendsbyte = [
    b"\xe3\x80\x82",
    b"\xef\xbc\x81",
    b"\xef\xbc\x9f",
    b"\xe2\x80\xa6",
    b"~",
    b"\xef\xbd\x9e",
    b"!",
    b"?",
    b"\xef\xbc\x9b",
]  # ,b'\xef\xbc\x9b' added semi column
# endfollowbyte = [b"'", b'"', b'\xe2\x80\x9d', b'\xe2\x80\x99', b'.']
endfollowbyte = [
    b"'",
    b'"',
    b"\xe2\x80\x9d",
    b"\xe2\x80\x99",
    b".",
    b")",
    b"\xef\xbc\x89",
]
# ): b')', ): b'\xef\xbc\x89' [,b')',b'\xef\xbc\x89']

senends = []
for i in range(len(senendsbyte)):
    senends.append(senendsbyte[i].decode("utf-8"))
endfollow = []
for i in range(len(endfollowbyte)):
    endfollow.append(endfollowbyte[i].decode("utf-8"))


# Segment sentences from text
def seg_zhsent(text):
    sen_lst = []
    buf_str = ""
    in_fo = False
    for char in text:
        if (not in_fo) and (char in senends):
            in_fo = True
            buf_str += char
            continue
        if in_fo:
            if (char in endfollow) or (char in senends):
                buf_str += char
            else:
                in_fo = False
                sen_lst.append(buf_str)
                buf_str = char
            continue
        buf_str += char
    # Collect the rest of text
    sen_lst.append(buf_str)

    return sen_lst


if __name__ == "__main__":
    # main(sys.argv)
    pass
