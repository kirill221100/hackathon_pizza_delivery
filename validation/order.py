from pydantic import BaseModel
from typing import List
from validation.pizza import PizzaOrder


class Order(BaseModel):
    pizza_orders: List[PizzaOrder]
    address: str

