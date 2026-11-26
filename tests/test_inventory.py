import pytest
from app.services.inventory import InventoryService, InsufficientStock

def test_stock_receipt_and_issue() -> None:
    service = InventoryService()
    product = service.create_product("abc-1", "Keyboard")
    assert service.move_stock(int(product["id"]), 10, "in", "PO-1") == 10
    assert service.move_stock(int(product["id"]), 3, "out", "SO-1") == 7

def test_prevents_negative_stock() -> None:
    service = InventoryService()
    product = service.create_product("abc-1", "Keyboard")
    with pytest.raises(InsufficientStock):
        service.move_stock(int(product["id"]), 1, "out", "SO-1")

def test_sku_is_unique_case_insensitively() -> None:
    service = InventoryService()
    service.create_product("abc-1", "Keyboard")
    with pytest.raises(ValueError):
        service.create_product("ABC-1", "Other")
