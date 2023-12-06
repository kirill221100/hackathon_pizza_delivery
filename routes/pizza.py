from fastapi import APIRouter, Depends
from typing import List
from security.oauth import get_current_user
from validation.pizza import CustomPizza as CustomPizzaValidation, CustomPizzaResponse, GetPizzasResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.pizza import create_custom_pizza, get_pizzas

pizza_router = APIRouter()


@pizza_router.post('/custom-pizza', response_model=CustomPizzaResponse)
async def custom_pizza_path(pizza_data: CustomPizzaValidation, user=Depends(get_current_user),
                            session: AsyncSession = Depends(get_session)):
    return await create_custom_pizza(pizza_data, user['id'], session)


@pizza_router.get('/get_pizzas', response_model=List[CustomPizzaResponse])
async def get_pizzas_path(session: AsyncSession = Depends(get_session), page: int = 1, per_page: int = 10):
    return await get_pizzas(session, page, per_page)
