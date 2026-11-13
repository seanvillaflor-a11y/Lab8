"""Lab 8 demonstration: association, aggregation, composition, polymorphism, LSP.

Run with:  python demo.py

This script is separate from the interactive inventorymanager.py. It exists to
demonstrate and test the object relationships and principles from the lab,
without any isinstance() checks and without separate loops per product type.
"""

from supplier import Supplier
from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from inventory import Inventory
from order import Order


def show_product_details(product: Product) -> None:
    """Work with any Product through the common abstraction (LSP + polymorphism).

    This function is typed to accept a Product. It never asks whether the
    object is a PhysicalProduct or a DigitalProduct; each subclass supplies its
    own display_information() and get_fulfilment_info() implementation.
    """
    product.display_information()
    print("  Fulfilment: " + product.get_fulfilment_info())


def section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    # ---- Association: Supplier <-> Product ----
    section("Association: Supplier and Product")
    techworld = Supplier("S001", "TechWorld", "sales@techworld.com")
    softbyte = Supplier("S002", "SoftByte", "support@softbyte.com")

    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, techworld, 2.1)
    mouse = PhysicalProduct("P002", "Mouse", 25.50, 40, techworld, 0.1)
    antivirus = DigitalProduct("P003", "Antivirus License", 45.00, 25, softbyte, 350.0)

    show_product_details(laptop)
    show_product_details(antivirus)
    # The Product holds a reference to the Supplier; both exist independently.
    print("laptop and mouse share the same Supplier object:",
          laptop.supplier is mouse.supplier)

    # ---- Aggregation: Inventory contains Products ----
    section("Aggregation: Inventory and Product")
    inventory = Inventory()
    for product in (laptop, mouse, antivirus):
        inventory.add_product(product)

    # Polymorphism: display_all() loops once over Product references; each
    # object runs its own display_information(). No isinstance checks anywhere.
    print("All products via the common Product abstraction:")
    inventory.display_all()

    # Remove from this inventory; the Product survives (aggregation).
    inventory.remove_product("P002")
    print("After removing P002 from inventory, the Product still works:")
    show_product_details(mouse)

    # ---- Composition: Order owns OrderLine objects ----
    section("Composition: Order and OrderLine")
    order = Order("O-1001")
    order.add_order_line(laptop, 2)
    order.add_order_line(antivirus, 3)
    order.display_information()

    # Same Product in a second Order -> its own OrderLine (shared Product).
    order2 = Order("O-1002")
    order2.add_order_line(laptop, 1)
    print("Same laptop referenced by both orders:",
          order.order_lines[0].product is order2.order_lines[0].product)
    print("But each order has its own OrderLine object:",
          order.order_lines[0] is not order2.order_lines[0])

    # ---- Polymorphism via Product references (Section 7.2) ----
    section("Polymorphism: one loop, many product types")
    mixed = Inventory()
    mixed.add_product(laptop)      # physical
    mixed.add_product(antivirus)   # digital
    # show_product_details works for both types without modification (LSP).
    mixed.display_all()
    print("Calling the same function on different Product subclasses:")
    show_product_details(laptop)
    show_product_details(antivirus)


if __name__ == "__main__":
    main()
