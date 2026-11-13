from product import Product
from orderline import OrderLine


class Order:
    """A customer order, composed of OrderLine objects (composition).

    Composition: the Order CREATES and OWNS its OrderLine objects. Order lines
    are not created elsewhere and passed in; instead add_order_line() builds
    them internally. An OrderLine belongs to exactly one Order, is never
    transferred to another Order, and is removed when the Order is cancelled
    or removed. This is the strongest ("terminal") relationship.
    """

    def __init__(self, order_id: str) -> None:
        self.__order_id = order_id
        self.__order_lines: list[OrderLine] = []

    # ---- Read-only access (properties) ----
    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return self.__order_lines

    # ---- Behaviour ----
    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create an OrderLine internally for the given product and quantity,
        and add it to this order. The Order owns the OrderLine it creates.
        """
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove (and discard) the line for the given product id.

        The OrderLine is part of this Order, so removing it means it ceases to
        exist as part of the order. Returns True if a line was removed.
        """
        for order_line in self.__order_lines:
            if order_line.product.product_id.lower() == product_id.lower():
                self.__order_lines.remove(order_line)
                return True
        return False

    def calculate_total(self) -> float:
        """Total value of the order: ask each OrderLine for its subtotal."""
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print("Order: " + self.__order_id)
        print("-" * 48)
        if len(self.__order_lines) == 0:
            print("  (no order lines)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("  Order Total: $" + format(self.calculate_total(), ".2f"))
        print("-" * 48)
