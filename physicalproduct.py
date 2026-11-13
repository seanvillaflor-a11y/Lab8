from product import Product
from shipping import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A physical product (is-a Product) that can-be-shipped.

    Single inheritance from Product, plus the CanBeShipped interface-style
    contract. Adds a weight attribute and shipping behaviour.
    """

    # A flat rate charged per kilogram of weight.
    SHIPPING_RATE_PER_KG: float = 2.50

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight = weight

    @property
    def weight(self) -> float:
        return self.__weight

    # ---- Method overriding: reuse the parent part, then add our own ----
    def display_information(self) -> None:
        super().display_information()
        print("  Type: Physical | Weight: " + format(self.__weight, ".2f") + " kg")

    # ---- Abstract method from Product ----
    def get_fulfilment_info(self) -> str:
        return "This physical product requires shipping and will be delivered by courier."

    # ---- CanBeShipped interface ----
    def calculate_shipping_cost(self) -> float:
        """Shipping cost based on the product's weight."""
        return self.__weight * PhysicalProduct.SHIPPING_RATE_PER_KG

    # ---- Persistence ----
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
