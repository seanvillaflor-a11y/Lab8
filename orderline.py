from product import Product


class OrderLine:
    """One line of an order: a product and the quantity requested.

    Composition note: an OrderLine is a part of an Order. The Order creates
    and owns its OrderLine objects, and an OrderLine is not intended to exist
    independently of its owning Order.

    Association note: the OrderLine *refers to* a Product but does NOT own it.
    The same Product can exist in an Inventory and be referenced by other
    OrderLines; it is not destroyed when the OrderLine (or its Order) goes away.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        self.__product = product
        self.__quantity = quantity

    # ---- Read-only access (properties) ----
    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    # ---- Behaviour ----
    def calculate_subtotal(self) -> float:
        """Return the product price multiplied by the quantity."""
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print("  " + str(self.__quantity) + " x " + self.__product.name
              + " @ $" + format(self.__product.price, ".2f")
              + " = $" + format(self.calculate_subtotal(), ".2f"))
