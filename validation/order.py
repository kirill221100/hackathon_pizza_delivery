from pydantic import BaseModel
from typing import List
from validation.pizza import PizzaOrder
import enum


class Status(enum.Enum):
    PREPARING = 'preparing'
    COOKING = 'cooking'
    DELIVERING = 'delivering'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


class Order(BaseModel):
    pizza_orders: List[PizzaOrder]
    address: str

