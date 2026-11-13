import json
import os
from inventory import Inventory
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from supplier import Supplier

# Global constant: always relative to this script, not to the folder it is run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "data", "inventory.json")


# ---------------------------------------------------------------
# File handling
#
# The data file now stores both suppliers and products:
#   { "suppliers": [ {supplier_id, name, contact_email}, ... ],
#     "products":  [ {id, name, price, stock, supplier_id, type, ...}, ... ] }
# Products reference their supplier by supplier_id (association).
# ---------------------------------------------------------------
def build_supplier_registry(supplier_dicts: list[dict]) -> dict[str, Supplier]:
    """Turn a list of saved supplier dicts into a {supplier_id: Supplier} map."""
    registry: dict[str, Supplier] = {}
    for item in supplier_dicts:
        supplier = Supplier(item["supplier_id"], item["name"], item["contact_email"])
        registry[supplier.supplier_id] = supplier
    return registry


def load_data() -> "tuple[Inventory, dict[str, Supplier]] | None":
    """Load suppliers and inventory from INVENTORY_FILE.

    Returns (inventory, suppliers) or None if the file cannot be used.
    """
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        suppliers = build_supplier_registry(data.get("suppliers", []))
        inventory = Inventory()
        inventory.load_from_list(data.get("products", []), suppliers)

        print(INVENTORY_FILE + " found.")
        print("Inventory loaded successfully.")
        return inventory, suppliers
    except FileNotFoundError:
        print(INVENTORY_FILE + " not found.")
        return None
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as error:
        print("Could not read " + INVENTORY_FILE + " (" + str(error) + ").")
        backup = INVENTORY_FILE + ".bak"
        try:
            os.replace(INVENTORY_FILE, backup)
            print("The unreadable file was kept as " + backup + ".")
        except OSError:
            pass
        return None


def save_data(inventory: Inventory, suppliers: dict[str, Supplier]) -> bool:
    """Write suppliers and inventory to INVENTORY_FILE as JSON."""
    print("Saving inventory...")
    try:
        os.makedirs(os.path.dirname(INVENTORY_FILE), exist_ok=True)
        payload = {
            "suppliers": [s.to_dict() for s in suppliers.values()],
            "products": inventory.to_list(),
        }
        with open(INVENTORY_FILE, "w") as file:
            json.dump(payload, file, indent=4)
        print("Inventory saved successfully to " + INVENTORY_FILE + ".")
        return True
    except OSError as error:
        print("Error saving inventory: " + str(error))
        return False


# ---------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------
def get_float(prompt: str) -> float:
    """Keep asking until the user enters a non-negative number."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Invalid input. Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_int(prompt: str) -> int:
    """Keep asking until the user enters a non-negative whole number."""
    while True:
        try:
            value = int(float(input(prompt)))  # decimals are truncated
            if value < 0:
                print("Invalid input. Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_supplier(suppliers: dict[str, Supplier]) -> "Supplier | None":
    """Let the user pick an existing supplier by id, or register a new one."""
    print("Available suppliers:")
    if len(suppliers) == 0:
        print("  (none yet)")
    for supplier in suppliers.values():
        print("  - " + supplier.supplier_id + ": " + supplier.name)
    print("Enter a supplier ID to use, or 'new' to add one.")
    choice = input("Supplier: ").strip()

    if choice.lower() == "new":
        return register_supplier(suppliers)

    supplier = suppliers.get(choice)
    if supplier is None:
        print("No supplier with that ID.")
        return None
    return supplier


def register_supplier(suppliers: dict[str, Supplier]) -> "Supplier | None":
    """Create a new Supplier and add it to the registry."""
    supplier_id = input("New Supplier ID: ").strip()
    if supplier_id == "":
        print("Supplier ID cannot be empty.")
        return None
    if supplier_id in suppliers:
        print("Supplier ID already exists.")
        return None
    name = input("Supplier Name: ").strip()
    if name == "":
        print("Supplier name cannot be empty.")
        return None
    contact_email = input("Supplier Contact Email: ").strip()
    supplier = Supplier(supplier_id, name, contact_email)
    suppliers[supplier_id] = supplier
    print("Supplier added.")
    return supplier


# ---------------------------------------------------------------
# Menu handlers (input and messages only; the work is done by the classes)
# ---------------------------------------------------------------
def handle_add(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("Add New Product")
    product_id = input("Product ID: ").strip()
    if product_id == "":
        print("Product ID cannot be empty.")
        return
    name = input("Product Name: ").strip()
    if name == "":
        print("Product name cannot be empty.")
        return
    price = get_float("Price: ")
    stock = get_int("Stock Quantity: ")

    supplier = choose_supplier(suppliers)
    if supplier is None:
        print("A valid supplier is required. Product not added.")
        return

    print("Product type:")
    print("  1. Physical product (has weight, can be shipped)")
    print("  2. Digital product (has download size)")
    type_choice = input("Choose product type (1-2): ").strip()

    if type_choice == "1":
        weight = get_float("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    elif type_choice == "2":
        download_size = get_float("Download size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
    else:
        print("Invalid product type. Product not added.")
        return

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("Product ID already exists.")


def handle_update(inventory: Inventory) -> None:
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print("Name: " + product.name)
    print("Current Stock: " + str(product.stock))
    new_stock = get_int("New Stock Quantity: ")
    inventory.update_stock(product_id, new_stock)


def handle_search(inventory: Inventory) -> None:
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    inventory.search_product(product_id)


def print_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def create_starter_data() -> "tuple[Inventory, dict[str, Supplier]]":
    """First run only: build suppliers and an Inventory with starter products."""
    suppliers: dict[str, Supplier] = {
        "S001": Supplier("S001", "TechWorld", "sales@techworld.com"),
        "S002": Supplier("S002", "SoftByte", "support@softbyte.com"),
    }
    inventory = Inventory()
    inventory.add_product(
        PhysicalProduct("P001", "Laptop", 1200.00, 15, suppliers["S001"], 2.1))
    inventory.add_product(
        PhysicalProduct("P002", "Mouse", 25.50, 40, suppliers["S001"], 0.1))
    inventory.add_product(
        DigitalProduct("P003", "Antivirus License", 45.00, 25, suppliers["S002"], 350.0))
    return inventory, suppliers


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    loaded = load_data()
    if loaded is None:
        inventory, suppliers = create_starter_data()
        print("Loaded starter suppliers and products.")
        save_data(inventory, suppliers)
    else:
        inventory, suppliers = loaded

    print_menu()

    while True:
        try:
            option = input("Enter option: ").strip()
        except EOFError:
            option = "6"

        if option == "1":
            inventory.display_all()
        elif option == "2":
            handle_add(inventory, suppliers)
        elif option == "3":
            handle_update(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            save_data(inventory, suppliers)
        elif option == "6":
            print("Saving inventory before exit...")
            save_data(inventory, suppliers)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
