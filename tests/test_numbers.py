import pytest

from app import numbers


def test_clamp():
    assert numbers.clamp(5, 0, 10) == 5
    assert numbers.clamp(-1, 0, 10) == 0
    assert numbers.clamp(11, 0, 10) == 10


def test_percentage():
    assert numbers.percentage(1, 3) == 33.33
    assert numbers.percentage(50, 200) == 25.0
    assert numbers.percentage(5, 0) == 0.0


def test_round_half_up():
    assert numbers.round_half_up(2.5) == 3.0
    assert numbers.round_half_up(0.125, 2) == 0.13
    assert numbers.round_half_up(-2.5) == -3.0
    assert numbers.round_half_up(2.4) == 2.0


def test_mean():
    assert numbers.mean([1, 2]) == 1.5
    assert numbers.mean([2, 4, 9]) == 5
    with pytest.raises(ValueError):
        numbers.mean([])


def test_median():
    assert numbers.median([3, 1, 2]) == 2
    assert numbers.median([4, 1, 3, 2]) == 2.5
    with pytest.raises(ValueError):
        numbers.median([])


def test_mode():
    assert numbers.mode([1, 2, 2, 3, 3]) == [2, 3]
    assert numbers.mode(["a"]) == ["a"]
    assert numbers.mode([]) == []


def test_is_prime():
    assert numbers.is_prime(2)
    assert numbers.is_prime(97)
    assert not numbers.is_prime(1)
    assert not numbers.is_prime(4)
    assert not numbers.is_prime(9)
    assert not numbers.is_prime(25)


def test_gcd():
    assert numbers.gcd(48, 36) == 12
    assert numbers.gcd(12, -18) == 6
    assert numbers.gcd(0, 5) == 5


def test_lcm():
    assert numbers.lcm(4, 6) == 12
    assert numbers.lcm(-4, 6) == 12
    assert numbers.lcm(0, 0) == 0


def test_factorial():
    assert numbers.factorial(0) == 1
    assert numbers.factorial(5) == 120
    with pytest.raises(ValueError):
        numbers.factorial(-1)


def test_fibonacci():
    assert numbers.fibonacci(6) == [0, 1, 1, 2, 3, 5]
    assert numbers.fibonacci(1) == [0]
    assert numbers.fibonacci(0) == []
