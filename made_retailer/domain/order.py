from dataclasses import dataclass
from typing import List
from uuid import UUID
from made_retailer.domain.entity import Entity
from made_retailer.domain.value_objects.sku import SKU


@dataclass
class OrderLine:
    sku: SKU
    quantity: int


class Order(Entity):
    client_id: UUID
    order_lines: List[OrderLine]