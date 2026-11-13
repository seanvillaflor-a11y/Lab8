import json
import os
from inventory import Inventory
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from product_factory import product_from_dict

# Global constant: always relative to this script, not to the folder it is run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "data", "inventory.json")


# ---------------------------------------------------------------
# File handling
# ---------------------------------------------------------------
def load_inventory():
    """Return an Inventory loaded from INVENTORY_FILE, or None if that is not possible."""
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)          # a list of dictionaries

        inventory = Inventory()
        inventory.load_from_list(data)

        print(INVENTORY_FILE + " found.")
        print("Inventory loaded successfully.")
        return inventory
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


def save_inventory(inventory):
    """Write the inventory to INVENTORY_FILE as JSON."""
    print("Saving inventory...")
    try:
        os.makedirs(os.path.dirname(INVENTORY_FILE), exist_ok=True)
        with open(INVENTORY_FILE, "w") as file:
            json.dump(inventory.to_list(), file, indent=4)
        print("Inventory saved successfully to " + INVENTORY_FILE + ".")
        return True
    except OSError as error:
        print("Error saving inventory: " + str(error))
        return False


# ---------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------
def get_float(prompt):
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


def get_int(prompt):
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


# ---------------------------------------------------------------
# Menu handlers (input and messages only; the work is done by Inventory)
# ---------------------------------------------------------------
def handle_add(inventory):
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

    print("Product type:")
    print("  1. Physical product (has weight, can be shipped)")
    print("  2. Digital product (has download size)")
    type_choice = input("Choose product type (1-2): ").strip()

    if type_choice == "1":
        weight = get_float("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight)
    elif type_choice == "2":
        download_size = get_float("Download size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, download_size)
    else:
        print("Invalid product type. Product not added.")
        return

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("Product ID already exists.")


def handle_update(inventory):
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


def handle_search(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    inventory.search_product(product_id)


def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def create_starter_inventory():
    """First run only: build an Inventory with starter products of both types."""
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.1))
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, 0.1))
    inventory.add_product(DigitalProduct("P003", "Antivirus License", 45.00, 25, 350.0))
    return inventory


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()
    if inventory is None:
        # No usable data file: start with the starter products and create the file now,
        # so every later run loads from it.
        inventory = create_starter_inventory()
        print("Loaded starter products.")
        save_inventory(inventory)

    print_menu()

    while True:
        try:
            option = input("Enter option: ").strip()
        except EOFError:
            option = "6"

        if option == "1":
            inventory.display_all()
        elif option == "2":
            handle_add(inventory)
        elif option == "3":
            handle_update(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            save_inventory(inventory)
        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
