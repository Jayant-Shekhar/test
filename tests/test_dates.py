from datetime import date

import pytest

from app import dates


def test_is_leap_year():
    assert dates.is_leap_year(2024)
    assert dates.is_leap_year(2000)
    assert not dates.is_leap_year(1900)
    assert not dates.is_leap_year(2023)


def test_days_in_month():
    assert dates.days_in_month(2023, 11) == 30
    assert dates.days_in_month(2023, 10) == 31
    assert dates.days_in_month(2024, 2) == 29
    assert dates.days_in_month(2023, 2) == 28


def test_add_business_days():
    friday = date(2024, 5, 3)
    assert dates.add_business_days(friday, 1) == date(2024, 5, 6)
    assert dates.add_business_days(friday, 5) == date(2024, 5, 10)


def test_business_days_between():
    assert dates.business_days_between(date(2024, 5, 6), date(2024, 5, 13)) == 5
    assert dates.business_days_between(date(2024, 5, 6), date(2024, 5, 6)) == 0


def test_age_on():
    birthday = date(1990, 6, 15)
    assert dates.age_on(birthday, date(2024, 6, 14)) == 33
    assert dates.age_on(birthday, date(2024, 6, 15)) == 34


def test_quarter_of():
    assert dates.quarter_of(date(2024, 1, 1)) == 1
    assert dates.quarter_of(date(2024, 3, 31)) == 1
    assert dates.quarter_of(date(2024, 4, 1)) == 2
    assert dates.quarter_of(date(2024, 12, 1)) == 4


def test_format_duration():
    assert dates.format_duration(3723) == "1h 2m 3s"
    assert dates.format_duration(60) == "1m"
    assert dates.format_duration(0) == "0s"


def test_parse_iso_date():
    assert dates.parse_iso_date(" 2024-05-13 ") == date(2024, 5, 13)


def test_start_of_week():
    assert dates.start_of_week(date(2024, 5, 8)) == date(2024, 5, 6)
    assert dates.start_of_week(date(2024, 5, 6)) == date(2024, 5, 6)


def test_days_until():
    assert dates.days_until(date(2024, 1, 10), date(2024, 1, 1)) == 9
    assert dates.days_until(date(2024, 1, 1), date(2024, 1, 10)) == -9


def test_month_name():
    assert dates.month_name(1) == "January"
    assert dates.month_name(12) == "December"
    with pytest.raises(ValueError):
        dates.month_name(13)
