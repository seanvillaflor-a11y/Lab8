from product import Product
from shipping import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A physical product (is-a Product) that can-be-shipped.

    Single inheritance from Product, plus the CanBeShipped interface-style
    contract. Adds a weight attribute and shipping behaviour.
    """

    # A flat rate charged per kilogram of weight.
    SHIPPING_RATE_PER_KG = 2.50

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    @property
    def weight(self):
        return self.__weight

    # ---- Method overriding: reuse the parent part, then add our own ----
    def display_information(self):
        super().display_information()
        print("  Type: Physical | Weight: " + format(self.__weight, ".2f") + " kg")

    # ---- Abstract method from Product ----
    def get_fulfilment_info(self):
        return "This physical product requires shipping and will be delivered by courier."

    # ---- CanBeShipped interface ----
    def calculate_shipping_cost(self):
        """Shipping cost based on the product's weight."""
        return self.__weight * PhysicalProduct.SHIPPING_RATE_PER_KG

    # ---- Persistence ----
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
