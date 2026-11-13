from product_factory import product_from_dict


class Inventory:
    """Manages a collection of Product objects.

    Inventory only manages products (add, find, list, update); it calls the
    products' own methods and never implements product behaviour itself.
    """

    def __init__(self):
        self.__products = []

    def is_empty(self):
        return len(self.__products) == 0

    def find_product(self, product_id):
        """Return the Product matching product_id (case-insensitive), or None."""
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def add_product(self, product):
        """Add a Product object. Returns False if the ID already exists."""
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def update_stock(self, product_id, new_stock):
        """Find a product and ask it to update its own stock."""
        product = self.find_product(product_id)
        if product is None:
            print("Product not found.")
            return False
        if product.update_stock(new_stock):
            print("Stock updated successfully!")
            return True
        return False

    def search_product(self, product_id):
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

    def display_all(self):
        print("Current Inventory")
        print("-" * 48)
        if self.is_empty():
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def to_list(self):
        """Return the products as a list of dictionaries (for saving)."""
        return [product.to_dict() for product in self.__products]

    def load_from_list(self, data):
        """Rebuild the inventory from a list of saved dictionaries."""
        if not isinstance(data, list):
            raise ValueError("inventory data must be a list")
        for item in data:
            self.add_product(product_from_dict(item))
