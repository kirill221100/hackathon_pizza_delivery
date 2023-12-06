from fastapi import APIRouter, Depends
from typing import List
from security.oauth import get_current_user
from validation.pizza import CustomPizza as CustomPizzaValidation, CustomPizzaResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.pizza import create_custom_pizza, get_pizzas, get_pizza_by_id

pizza_router = APIRouter()


@pizza_router.post('/custom-pizza', response_model=CustomPizzaResponse)
async def custom_pizza_path(pizza_data: CustomPizzaValidation, user=Depends(get_current_user),
                            session: AsyncSession = Depends(get_session)):
    return await create_custom_pizza(pizza_data, user['id'], session)


@pizza_router.get('/get-pizza-by-id/{pizza_id}', response_model=CustomPizzaResponse)
async def get_pizza_by_id_path(pizza_id: int, session: AsyncSession = Depends(get_session)):
    return await get_pizza_by_id(pizza_id, session)


@pizza_router.get('/get_pizzas', response_model=List[CustomPizzaResponse])
async def get_pizzas_path(session: AsyncSession = Depends(get_session), page: int = 1, per_page: int = 10):
    return await get_pizzas(session, page, per_page)


# @pizza_router.get('/get-favorite-pizzas', response_model=List[CustomPizzaResponse])
# async def get_favorite_pizzas_path(user=Depends(get_current_user), session: AsyncSession = Depends(get_session),
#                                    page: int = 1, per_page: int = 10):
#     return await get_favorite_pizzas(user['id'], session, page, per_page)
#
#
# @pizza_router.get('/get-custom-pizzas', response_model=List[CustomPizzaResponse])
# async def get_custom_pizzas_path(user=Depends(get_current_user), session: AsyncSession = Depends(get_session),
#                                  page: int = 1, per_page: int = 10):
#     return await get_custom_pizzas(user['id'], session, page, per_page)


