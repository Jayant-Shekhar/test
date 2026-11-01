import pytest

from app import search

PEOPLE = [
    {"name": "Ada Lovelace", "city": "London", "active": True, "score": 90},
    {"name": "Alan Turing", "city": "London", "active": False, "score": 95},
    {"name": "Marie Curie", "city": "Paris", "active": True, "score": 99},
    {"name": "Pierre Curie", "city": "Paris", "active": False},
]


def test_total_pages():
    assert search.total_pages(25, 10) == 3
    assert search.total_pages(20, 10) == 2
    assert search.total_pages(0, 10) == 1
    with pytest.raises(ValueError):
        search.total_pages(5, 0)


def test_paginate():
    items = list(range(1, 26))
    assert search.paginate(items, 1, 10) == list(range(1, 11))
    assert search.paginate(items, 3, 10) == [21, 22, 23, 24, 25]


def test_page_window():
    assert search.page_window(1, 10) == [1, 2, 3, 4, 5]
    assert search.page_window(5, 10) == [3, 4, 5, 6, 7]
    assert search.page_window(10, 10) == [6, 7, 8, 9, 10]
    assert search.page_window(2, 3) == [1, 2, 3]


def test_sort_records():
    names = [r["name"] for r in search.sort_records(PEOPLE, "score", descending=True)]
    assert names == ["Marie Curie", "Alan Turing", "Ada Lovelace", "Pierre Curie"]


def test_filter_records():
    result = search.filter_records(PEOPLE, city="Paris", active=True)
    assert [r["name"] for r in result] == ["Marie Curie"]


def test_search_records():
    result = search.search_records(PEOPLE, "ada", ["name"])
    assert [r["name"] for r in result] == ["Ada Lovelace"]
    assert len(search.search_records(PEOPLE, "CURIE", ["name"])) == 2


def test_top_n():
    scored = [p for p in PEOPLE if "score" in p]
    assert [r["name"] for r in search.top_n(scored, "score", 2)] == ["Marie Curie", "Alan Turing"]


def test_binary_search():
    assert search.binary_search([1, 3, 5, 7, 9], 9) == 4
    assert search.binary_search([1, 3, 5, 7, 9], 1) == 0
    assert search.binary_search([5], 5) == 0
    assert search.binary_search([1, 3], 2) == -1


def test_merge_sorted():
    assert search.merge_sorted([1, 4], [2, 3, 5, 6]) == [1, 2, 3, 4, 5, 6]
    assert search.merge_sorted([], [1]) == [1]


def test_offset_for_cursor():
    assert search.offset_for_cursor("offset:20") == 20
    assert search.offset_for_cursor(None) == 0
    assert search.offset_for_cursor("offset:abc") == 0
    assert search.offset_for_cursor("offset:-5") == 0


def test_highlight():
    assert search.highlight("Python and python", "PYTHON") == "<mark>Python</mark> and <mark>python</mark>"
    assert search.highlight("abc", "") == "abc"
