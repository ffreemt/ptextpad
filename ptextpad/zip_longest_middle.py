# coding: utf-8
"""Modify zip_longest: fillvalue in the middle.

zip_longest(iter1 [,iter2 [...]], [fillvalue=None]) --> zip_longest object
"""

# from nose.tools import eq_


def zip_longest_middle(list1, list2, fillvalue=None):
    """Do zip_longest with fillvalue in middle."""
    len1 = len(list1)
    len2 = len(list2)

    if len1 == len2:
        out1 = zip(list1, list2)
    elif len2 > len1:
        tmp = [fillvalue] * (len2 - len1)
        out1 = list1[: (len1 + 1) // 2] + tmp + list1[(len1 + 1) // 2:]
        out1 = zip(out1, list2)
    else:
        tmp = [fillvalue] * (len1 - len2)
        out1 = list2[: (len2 + 1) // 2] + tmp + list2[(len2 + 1) // 2:]
        out1 = zip(list1, out1)

    out = []
    for elm in out1:
        # out += list(elm)
        # out += elm  # list of numbers
        out.append(elm)  # list of tuples

    return out


def test1():
    """Test 1."""
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    out = list(zip_longest_middle(list1, list2))
    assert out == [(1, 4), (2, 5), (3, 6)]


def test2():
    """Test 2."""
    list1 = [1, 2, 3]
    list2 = [4, 5, 6, 7, 8]

    out = list(zip_longest_middle(list1, list2, ""))
    assert out == [(1, 4), (2, 5), ("", 6), ("", 7), (3, 8)]


def test3():
    """Test 3."""
    list1 = [1, 2, 3, 4]
    list2 = [4, 5, 6, 7, 8]
    out = zip_longest_middle(list1, list2)
    assert out == [(1, 4), (2, 5), (None, 6), (3, 7), (4, 8)]

    out = zip_longest_middle(list1, list2, "")
    assert out == [(1, 4), (2, 5), ("", 6), (3, 7), (4, 8)]


def test4():
    """Test 4."""
    list1 = []
    list2 = [4, 5, 6, 7, 8]
    out = zip_longest_middle(list1, list2)
    assert out == [(None, 4), (None, 5), (None, 6), (None, 7), (None, 8)]

    out = zip_longest_middle(list1, list2, "")
    assert out == [("", 4), ("", 5), ("", 6), ("", 7), ("", 8)]


def test5():
    """Test 5."""
    list1 = [1, 2, 3]
    list2 = []
    out = zip_longest_middle(list1, list2)
    assert out == [(1, None), (2, None), (3, None)]

    out = zip_longest_middle(list1, list2, "")
    assert out == [(1, ""), (2, ""), (3, "")]
