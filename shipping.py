from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style abstract base class (a 'can-be-shipped' capability).

    This is NOT part of the Product inheritance chain. Any class that can
    be shipped "signs the contract" by implementing calculate_shipping_cost().
    It deliberately holds no product-specific attributes or shipping logic;
    it only specifies the capability a shippable object must provide.
    """

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for the implementing object."""
        raise NotImplementedError
