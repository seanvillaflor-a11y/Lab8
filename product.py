from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base for all products. Manages common product state.

    Product is abstract (inherits ABC) and declares the abstract method
    get_fulfilment_info(), so it can never be instantiated directly.
    Every concrete product must be either a PhysicalProduct or a
    DigitalProduct.
    """

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ---- Read-only access (properties) ----
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    # ---- Behaviour (concrete, shared by all products) ----
    def update_stock(self, quantity):
        """Set the stock to quantity. Rejects negative values."""
        if quantity < 0:
            print("Stock cannot be negative.")
            return False
        self.__stock = quantity
        return True

    def display_information(self):
        """Display the information common to every product.

        Subclasses override this, call super().display_information() to
        reuse this common part, then add their own specific details.
        """
        print("ID: " + self.__product_id
              + " | Name: " + self.__name
              + " | Price: $" + format(self.__price, ".2f")
              + " | Stock: " + str(self.__stock))

    # ---- Abstract behaviour (each subclass MUST implement) ----
    @abstractmethod
    def get_fulfilment_info(self):
        """Return a message describing how this product is fulfilled."""
        raise NotImplementedError

    # ---- Conversion helpers ----
    def to_dict(self):
        """Common fields shared by every product type.

        Subclasses extend this with a "type" identifier and their own
        extra attributes.
        """
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }
