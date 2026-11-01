import pytest

from app import parsing


def test_parse_csv_line():
    assert parsing.parse_csv_line('a,"b,c",d') == ["a", "b,c", "d"]
    assert parsing.parse_csv_line('x,"say ""hi""",y') == ["x", 'say "hi"', "y"]
    assert parsing.parse_csv_line("a,,b") == ["a", "", "b"]


def test_parse_query_string():
    assert parsing.parse_query_string("?tag=a&tag=b&q=hello+world%21") == {
        "tag": ["a", "b"],
        "q": ["hello world!"],
    }
    assert parsing.parse_query_string("") == {}


def test_parse_bool():
    assert parsing.parse_bool(" Yes ") is True
    assert parsing.parse_bool("off") is False
    with pytest.raises(ValueError):
        parsing.parse_bool("maybe")


def test_parse_size():
    assert parsing.parse_size("10KB") == 10240
    assert parsing.parse_size("1.5 MB") == 1572864
    assert parsing.parse_size("512") == 512
    with pytest.raises(ValueError):
        parsing.parse_size("abc")


def test_parse_duration():
    assert parsing.parse_duration("1h30m") == 5400
    assert parsing.parse_duration("45s") == 45
    assert parsing.parse_duration("2h 5s") == 7205


def test_compare_versions():
    assert parsing.compare_versions("1.10", "1.9") == 1
    assert parsing.compare_versions("1.0", "1") == 0
    assert parsing.compare_versions("2.0.1", "2.1") == -1


def test_roman_to_int():
    assert parsing.roman_to_int("MCMXCIV") == 1994
    assert parsing.roman_to_int("iv") == 4
    assert parsing.roman_to_int("LVIII") == 58


def test_int_to_roman():
    assert parsing.int_to_roman(1994) == "MCMXCIV"
    assert parsing.int_to_roman(3) == "III"
    assert parsing.int_to_roman(58) == "LVIII"
    with pytest.raises(ValueError):
        parsing.int_to_roman(0)


def test_parse_range_list():
    assert parsing.parse_range_list("1-3,5,7-8") == [1, 2, 3, 5, 7, 8]
    assert parsing.parse_range_list(" 2, 2-3 ") == [2, 3]


def test_parse_key_value():
    text = '# database\nURL=postgres://u:p@h/db?sslmode=require\n\nNAME = "demo"\n'
    assert parsing.parse_key_value(text) == {
        "URL": "postgres://u:p@h/db?sslmode=require",
        "NAME": "demo",
    }


def test_parse_content_type():
    assert parsing.parse_content_type('Text/HTML; Charset="UTF-8"') == ("text/html", {"charset": "UTF-8"})
    assert parsing.parse_content_type("application/json") == ("application/json", {})
