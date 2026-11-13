from product import Product
from product_factory import product_from_dict


class Inventory:
    """Manages a collection of Product objects (aggregation).

    An Inventory groups Product objects, but it does NOT own their lifecycle:
    a Product can exist before being added, and removing it from the inventory
    does not destroy the Product. This is the whole-part "has-a" relationship
    of aggregation (weaker than composition).

    The collection is typed as list[Product] (the base class), so the same
    inventory can hold any Product subclass -- PhysicalProduct, DigitalProduct
    or any future type.
    """

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def is_empty(self) -> bool:
        return len(self.__products) == 0

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product matching product_id (case-insensitive), or None."""
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def add_product(self, product: Product) -> bool:
        """Add an existing Product object. Returns False if the ID already exists."""
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        """Remove the matching Product reference from the inventory.

        Returns True if a product was removed, False if it was not found.
        This removes the reference only; the Product object itself continues
        to exist and can be added to another inventory (aggregation).
        """
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        """Find a product and ask it to update its own stock."""
        product = self.find_product(product_id)
        if product is None:
            print("Product not found.")
            return False
        if product.update_stock(new_stock):
            print("Stock updated successfully!")
            return True
        return False

    def search_product(self, product_id: str) -> Product | None:
        """Display one product's details, or a not-found message."""
        product = self.find_product(product_id)
        if product is None:
            print("Product not found.")
            return None
        print("Product Found")
        print("-" * 48)
        product.display_information()
        print("  Fulfilment: " + product.get_fulfilment_info())
        print("-" * 48)
        return product

    def display_all(self) -> None:
        print("Current Inventory")
        print("-" * 48)
        if self.is_empty():
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def to_list(self) -> list[dict]:
        """Return the products as a list of dictionaries (for saving)."""
        return [product.to_dict() for product in self.__products]

    def load_from_list(self, data: list[dict]) -> None:
        """Rebuild the inventory from a list of saved dictionaries."""
        if not isinstance(data, list):
            raise ValueError("inventory data must be a list")
        for item in data:
            self.add_product(product_from_dict(item))
