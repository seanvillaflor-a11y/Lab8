class Supplier:
    """Represents who supplies a product.

    A Supplier is NOT part of a Product and a Product is NOT part of a
    Supplier -- they collaborate through a reference (association). Both can
    exist independently; deleting one does not destroy the other.
    """

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id = supplier_id
        self.__name = name
        self.__contact_email = contact_email

    # ---- Read-only access (properties) ----
    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    # ---- Behaviour ----
    def display_information(self) -> None:
        print("Supplier: " + self.__name
              + " | ID: " + self.__supplier_id
              + " | Contact: " + self.__contact_email)

    # ---- Conversion helper (so persistence code never touches privates) ----
    def to_dict(self) -> dict:
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }
