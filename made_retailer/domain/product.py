from made_retailer.domain.entity import Entity
from made_retailer.domain.value_objects.sku import SKU


class Product(Entity):
    sku: SKU
    description: str