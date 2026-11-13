from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base for all products. Manages common product state.

    Product is abstract (inherits ABC) and declares the abstract method
    get_fulfilment_info(), so it can never be instantiated directly.
    Every concrete product must be either a PhysicalProduct or a
    DigitalProduct.

    A Product is associated with a Supplier (association, not aggregation):
    the Supplier is created independently and passed in. The Product keeps a
    reference so it can ask the Supplier for its information, but it does not
    own the Supplier -- both can exist independently. 

    product asks info from supplier but supplier is independent of product. 
    An association is also so that both classes are loose coupled/no dependence 
    on each other
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier = supplier

    # ---- Read-only access (properties) ----
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    # ---- Behaviour (concrete, shared by all products) ----
    def update_stock(self, quantity: int) -> bool:
        """Set the stock to quantity. Rejects negative values."""
        if quantity < 0:
            print("Stock cannot be negative.")
            return False
        self.__stock = quantity
        return True

    def display_information(self) -> None:
        """Display the information common to every product.

        Subclasses override this, call super().display_information() to
        reuse this common part, then add their own specific details.
        """
        print("ID: " + self.__product_id
              + " | Name: " + self.__name
              + " | Price: $" + format(self.__price, ".2f")
              + " | Stock: " + str(self.__stock)
              + " | Supplier: " + self.__supplier.name)

    # ---- Abstract behaviour (each subclass MUST implement) ----
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message describing how this product is fulfilled."""
        raise NotImplementedError

    # ---- Conversion helpers ----
    def to_dict(self) -> dict:
        """Common fields shared by every product type.

        Subclasses extend this with a "type" identifier and their own
        extra attributes. The associated supplier is stored by reference
        (its id) so the association can be rebuilt on load.
        """
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.supplier_id,
        }
