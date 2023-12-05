from fastapi import APIRouter, Depends
from security.oauth import get_current_user
from validation.pizza import CustomPizza as CusrtomPizzaValidation
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.pizza import create_custom_pizza

pizza_router = APIRouter()


@pizza_router.post('/custom-pizza')
async def custom_pizza_path(pizza_data: CusrtomPizzaValidation, user=Depends(get_current_user),
                            session: AsyncSession = Depends(get_session)):
    return await create_custom_pizza(pizza_data, user['id'], session)


# @pizza_router.get('/get_pizzas')
# async def get_pizzas_path
