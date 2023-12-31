from pydantic import BaseModel
from typing import List, Optional
from validation.pizza import Crust, Sauce, Toppings


class FavoriteIngredients(BaseModel):
    crusts: Optional[List[Crust]]
    sauces: Optional[List[Sauce]]
    toppings: Optional[List[Toppings]]


class FavoriteIngredientsResponse(FavoriteIngredients):
    pass


class UserResponse(BaseModel):
    id: int
    username: str
    address: Optional[str]

