from datetime import date

import pytest

from app import inventory as inv


def test_add_stock():
    stock = {"A": 5}
    assert inv.add_stock(stock, "A", 3) == {"A": 8}
    assert inv.add_stock(stock, "B", 2) == {"A": 5, "B": 2}
    assert stock == {"A": 5}
    with pytest.raises(ValueError):
        inv.add_stock(stock, "A", 0)


def test_remove_stock():
    assert inv.remove_stock({"A": 5}, "A", 2) == {"A": 3}
    assert inv.remove_stock({"A": 5, "B": 1}, "A", 5) == {"B": 1}
    with pytest.raises(inv.InsufficientStockError):
        inv.remove_stock({"A": 1}, "A", 2)


def test_low_stock():
    assert inv.low_stock({"B": 2, "A": 5, "C": 10}, 5) == ["A", "B"]


def test_inventory_value():
    assert inv.inventory_value({"A": 2, "B": 3}, {"A": 1.5, "B": 2}) == 9.0
    assert inv.inventory_value({"A": 2, "Z": 7}, {"A": 1.25}) == 2.5


def test_reorder_quantity():
    assert inv.reorder_quantity(3, 5, 20) == 17
    assert inv.reorder_quantity(5, 5, 20) == 15
    assert inv.reorder_quantity(6, 5, 20) == 0


def test_reserve_items():
    stock = {"A": 5, "B": 1}
    assert inv.reserve_items(stock, {"A": 2}) == {"A": 3, "B": 1}
    assert stock == {"A": 5, "B": 1}
    with pytest.raises(inv.InsufficientStockError):
        inv.reserve_items(stock, {"A": 2, "B": 3})
    assert stock == {"A": 5, "B": 1}


def test_fulfillment_rate():
    assert inv.fulfillment_rate(8, 6) == 75.0
    assert inv.fulfillment_rate(10, 12) == 100.0
    assert inv.fulfillment_rate(0, 0) == 100.0


def test_find_by_sku():
    products = [{"sku": "AB-1", "name": "Widget"}, {"sku": "CD-2", "name": "Gadget"}]
    assert inv.find_by_sku(products, " ab-1 ") == {"sku": "AB-1", "name": "Widget"}
    assert inv.find_by_sku(products, "zz") is None


def test_movement_balance():
    moves = [
        {"sku": "A", "type": "in", "qty": 10},
        {"sku": "A", "type": "out", "qty": 3},
        {"sku": "B", "type": "out", "qty": 2},
    ]
    assert inv.movement_balance(moves) == {"A": 7, "B": -2}


def test_expiring_soon():
    today = date(2024, 5, 1)
    batches = [
        {"id": "old", "expires": date(2024, 4, 30)},
        {"id": "today", "expires": date(2024, 5, 1)},
        {"id": "soon", "expires": date(2024, 5, 8)},
        {"id": "later", "expires": date(2024, 6, 1)},
    ]
    assert inv.expiring_soon(batches, today, 7) == ["today", "soon"]


def test_allocate_fifo():
    batches = [
        {"id": "new", "received": date(2024, 3, 1), "qty": 10},
        {"id": "old", "received": date(2024, 1, 1), "qty": 4},
    ]
    assert inv.allocate_fifo(batches, 6) == [{"id": "old", "qty": 4}, {"id": "new", "qty": 2}]
    with pytest.raises(inv.InsufficientStockError):
        inv.allocate_fifo(batches, 20)
