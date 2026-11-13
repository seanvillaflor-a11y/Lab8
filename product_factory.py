from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct


def product_from_dict(data):
    """Build the correct Product subclass from a saved dictionary.

    Uses the "type" identifier stored in the JSON to decide which subclass
    to create. Older records without a "type" default to physical.
    """
    product_type = data.get("type", "physical")

    if product_type == "digital":
        return DigitalProduct(
            data["id"],
            data["name"],
            data["price"],
            data["stock"],
            data.get("download_size", 0.0),
        )

    if product_type == "physical":
        return PhysicalProduct(
            data["id"],
            data["name"],
            data["price"],
            data["stock"],
            data.get("weight", 0.0),
        )

    raise ValueError("Unknown product type: " + str(product_type))
