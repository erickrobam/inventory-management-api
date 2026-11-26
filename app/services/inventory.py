from dataclasses import dataclass

class InsufficientStock(Exception):
    """Raised when an outbound movement exceeds available stock."""

@dataclass(frozen=True)
class Movement:
    product_id: int
    quantity: int
    direction: str
    reference: str

class InventoryService:
    """Starter domain service; persistence can be replaced by a repository adapter."""
    def __init__(self) -> None:
        self._products: dict[int, dict[str, object]] = {}
        self._sku_index: dict[str, int] = {}
        self._balances: dict[int, int] = {}
        self.movements: list[Movement] = []
        self._next_id = 1

    def create_product(self, sku: str, name: str) -> dict[str, object]:
        normalized = sku.strip().upper()
        if normalized in self._sku_index:
            raise ValueError(f"SKU '{normalized}' already exists")
        product_id = self._next_id
        self._next_id += 1
        product = {"id": product_id, "sku": normalized, "name": name.strip()}
        self._products[product_id] = product
        self._sku_index[normalized] = product_id
        self._balances[product_id] = 0
        return product

    def list_products(self) -> list[dict[str, object]]:
        return list(self._products.values())

    def move_stock(self, product_id: int, quantity: int, direction: str, reference: str) -> int:
        if product_id not in self._products:
            raise KeyError(product_id)
        delta = quantity if direction == "in" else -quantity
        new_balance = self._balances[product_id] + delta
        if new_balance < 0:
            raise InsufficientStock("Movement would make inventory negative")
        self._balances[product_id] = new_balance
        self.movements.append(Movement(product_id, quantity, direction, reference))
        return new_balance
