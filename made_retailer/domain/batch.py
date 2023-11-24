from typing import List
from made_retailer.domain.entity import Entity
from made_retailer.domain.order import OrderLine
from made_retailer.domain.value_objects.sku import SKU


class Batch(Entity):
    sku: SKU
    quantity: int
    order_lines: List[OrderLine]