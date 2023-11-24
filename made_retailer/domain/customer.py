from made_retailer.domain.entity import Entity
from made_retailer.domain.value_objects.address import Address


class Customer(Entity):
    name: str
    address: Address
