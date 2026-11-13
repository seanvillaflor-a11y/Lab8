from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A digital product (is-a Product). Adds a download_size attribute."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size = download_size

    @property
    def download_size(self) -> float:
        return self.__download_size

    # Method overriding: reuse the parent part, then add our own.
    def display_information(self) -> None:
        super().display_information()
        print("  Type: Digital | Download Size: "
              + format(self.__download_size, ".2f") + " MB")

    # Abstract method from Product.
    def get_fulfilment_info(self) -> str:
        return "This digital product is delivered instantly via a download link."

    # Persistence.
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
