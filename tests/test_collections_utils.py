import pytest

from app import collections_utils as cu


def test_chunk():
    assert cu.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert cu.chunk([], 3) == []
    with pytest.raises(ValueError):
        cu.chunk([1], 0)


def test_flatten():
    assert cu.flatten([1, [2, [3, [4]]], (5,)]) == [1, 2, 3, 4, 5]
    assert cu.flatten(["ab", ["cd"]]) == ["ab", "cd"]


def test_unique():
    assert cu.unique([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert cu.unique([]) == []


def test_group_by():
    result = cu.group_by(["apple", "avocado", "banana"], lambda s: s[0])
    assert result == {"a": ["apple", "avocado"], "b": ["banana"]}


def test_partition():
    assert cu.partition([1, 2, 3, 4], lambda x: x % 2 == 0) == ([2, 4], [1, 3])


def test_rotate():
    assert cu.rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
    assert cu.rotate([1, 2, 3], 4) == [3, 1, 2]
    assert cu.rotate([1, 2, 3], -1) == [2, 3, 1]
    assert cu.rotate([], 3) == []


def test_sliding_window():
    assert cu.sliding_window([1, 2, 3, 4], 2) == [[1, 2], [2, 3], [3, 4]]
    assert cu.sliding_window([1, 2], 3) == []


def test_dedupe_by_key():
    records = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}, {"id": 1, "v": "c"}]
    assert cu.dedupe_by_key(records, "id") == [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}]


def test_deep_merge():
    base = {"a": {"x": 1}, "b": 1}
    override = {"a": {"y": 2}, "c": 3}
    assert cu.deep_merge(base, override) == {"a": {"x": 1, "y": 2}, "b": 1, "c": 3}
    assert base == {"a": {"x": 1}, "b": 1}


def test_invert_dict():
    assert cu.invert_dict({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}


def test_most_common():
    assert cu.most_common("abracadabra", 2) == [("a", 5), ("b", 2)]
