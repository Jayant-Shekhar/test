from decimal import Decimal

import pytest

from app import pricing


def test_apply_discount():
    assert pricing.apply_discount(200, 15) == Decimal("170.00")
    assert pricing.apply_discount(10, 0) == Decimal("10.00")
    with pytest.raises(ValueError):
        pricing.apply_discount(10, 120)


def test_add_tax():
    assert pricing.add_tax(100, 0.0825) == Decimal("108.25")
    assert pricing.add_tax("19.99", 0.07) == Decimal("21.39")


def test_cart_total():
    items = [{"unit_price": "2.50", "quantity": 4}, {"unit_price": 1.25, "quantity": 2}]
    assert pricing.cart_total(items) == Decimal("12.50")
    assert pricing.cart_total([]) == Decimal("0.00")


def test_bulk_discount_rate():
    assert pricing.bulk_discount_rate(9) == Decimal("0")
    assert pricing.bulk_discount_rate(10) == Decimal("0.05")
    assert pricing.bulk_discount_rate(50) == Decimal("0.10")
    assert pricing.bulk_discount_rate(100) == Decimal("0.15")


def test_shipping_cost():
    assert pricing.shipping_cost(50, 2) == Decimal("0.00")
    assert pricing.shipping_cost("49.99", 2.1) == Decimal("9.50")
    assert pricing.shipping_cost(10, 0) == Decimal("5.00")


def test_split_bill():
    shares = pricing.split_bill(10, 3)
    assert shares == [Decimal("3.34"), Decimal("3.33"), Decimal("3.33")]
    assert sum(shares) == Decimal("10")
    with pytest.raises(ValueError):
        pricing.split_bill(10, 0)


def test_convert_currency():
    assert pricing.convert_currency(100, 0.92) == Decimal("92.00")
    assert pricing.convert_currency(10, 1.5) == Decimal("15.00")


def test_compound_interest():
    assert pricing.compound_interest(1000, 0.05, 10, 1) == Decimal("1628.89")
    assert pricing.compound_interest(1000, 0.12, 1, 12) == Decimal("1126.83")


def test_monthly_loan_payment():
    assert pricing.monthly_loan_payment(1200, 0, 12) == Decimal("100.00")
    assert pricing.monthly_loan_payment(10000, 0.06, 36) == Decimal("304.22")


def test_apply_coupon():
    assert pricing.apply_coupon(15, {"type": "fixed", "value": 20}) == Decimal("0.00")
    assert pricing.apply_coupon(80, {"type": "percent", "value": 10}) == Decimal("72.00")
    assert pricing.apply_coupon(80, {"type": "fixed", "value": 5, "min_spend": 100}) == Decimal("80.00")


def test_format_price():
    assert pricing.format_price(1234.5) == "$1,234.50"
    assert pricing.format_price(-5) == "-$5.00"
    assert pricing.format_price(0.1, "€") == "€0.10"
