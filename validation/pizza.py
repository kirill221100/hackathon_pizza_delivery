from pydantic import BaseModel
import enum
from typing import List, Optional


class Crust(str, enum.Enum):
    SOURDOUGH = 'sourdough'
    GLUTEN_FREE = 'gluten_free'
    CANOTTO = 'canotto'
    NYC_STYLE = 'nyc_style'
    DETROIT_STYLE = 'detroit_style'
    ITALIAN = 'italian'


class Sauce(str, enum.Enum):
    MARINARA = 'marinara'
    SPICY_RED = 'spicey_red'
    BBQ = 'bbq'
    BUFFALO = 'buffalo'
    ALFREDO = 'alfredo'
    PESTO = 'pesto'


class Toppings(str, enum.Enum):
    CHEESE = 'cheese'
    OLIVES = 'olives'
    TOMATOES = 'tomatoes'
    MUSHROOMS = 'mushrooms'
    PEPPERONI = 'pepperoni'


class Size(str, enum.Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'


class Prices(enum.Enum):
    CRUST = 150
    SAUCE = 50
    TOPPINGS = 25
    SMALL_SIZE = 1.15
    MEDIUM_SIZE = 1.35
    LARGE_SIZE = 1.6


class Pizza(BaseModel):
    title: str
    crust: Crust
    sauce: Sauce
    toppings: List[Toppings]
    size: Size
    picture: str


class CustomPizza(Pizza):
    picture: Optional[str]


class CustomPizzaResponse(CustomPizza):
    id: int
    user_id: int
    price: float
    is_custom: bool


class PizzaResponse(Pizza):
    id: int
    price: float
    is_custom: bool


class GetPizzasResponse(BaseModel):
    pizzas: List[PizzaResponse]


class PizzaOrder(BaseModel):
    pizza: PizzaResponse
    # pizza_id: int
    amount: int

