from pydantic import BaseModel
from typing import List
from validation.pizza import PizzaOrder, PizzaOrderResponse
import enum
from datetime import datetime


class Status(enum.Enum):
    PREPARING = 'preparing'
    COOKING = 'cooking'
    DELIVERING = 'delivering'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


class Order(BaseModel):
    pizzas: List[PizzaOrder]
    address: str


class OrderResponse(Order):
    id: int
    user_id: int
    pizzas: List[PizzaOrderResponse]
    price: int
    date: datetime
    status: Status
