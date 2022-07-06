"""Test insert_itag."""
# pylint: disable=invalid-name
from ptextpad.insert_itag import insert_itag

itag = "|||"

def test_insert_itag_special_cases():
    """Test insert_itag for some special casse."""
    text = "a\nbc"

    # '|||a\nbc'
    insert_itag(text, (0, -3)).startswith(itag)

    # 'a\n|||bc'
    insert_itag(text, (2, -3)).splitlines()[1].startswith(itag)

    # 'a\nb|||c'
    insert_itag(text, (1, 1)).splitlines()[1].startswith("b" + itag)

    # 'a\nbc|||'
    insert_itag(text, (1, 2)).endswith(itag)
