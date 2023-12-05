from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from validation.pizza import CustomPizza as CustomPizzaValidation, Prices
from db.models.pizza import Pizza, PizzaOrder
from db.utils.user import get_user_by_id, get_user_by_id_selectin_favorite_pizzas


async def create_pizza_order(pizza_id: int, amount: int, session: AsyncSession):
    if pizza := await get_pizza_by_id(pizza_id, session):
        pizza_order = PizzaOrder(pizza=pizza, amount=amount)
        return pizza_order
    raise HTTPException(status_code=404, detail='No pizza with such id')


async def create_custom_pizza(pizza_data: CustomPizzaValidation, user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    pizza = Pizza(title=pizza_data.title, crust=pizza_data.crust, sauce=pizza_data.sauce, toppings=pizza_data.toppings,
                  size=pizza_data.size, picture=pizza_data.picture, is_custom=True, user=user)
    if pizza_data.picture:
        pizza.picture = pizza_data.picture
    price = Prices.CRUST.value + Prices.SAUCE.value + Prices.TOPPINGS.value * len(pizza_data.toppings)
    if pizza_data.size == 'small':
        price *= Prices.SMALL_SIZE.value
    elif pizza_data.size == 'medium':
        price *= Prices.MEDIUM_SIZE.value
    else:
        price *= Prices.LARGE_SIZE.value
    pizza.price = price
    session.add(pizza)
    await session.commit()
    return pizza


async def add_favorite_pizza(pizza_id: int, user_id: int, session: AsyncSession):
    pizza = await get_pizza_by_id(pizza_id, session)
    user = await get_user_by_id_selectin_favorite_pizzas(user_id, session)
    user.favorite_pizzas.append(pizza)
    await session.commit()
    return status.HTTP_200_OK


async def delete_from_favorite_pizza(pizza_id: int, user_id: int, session: AsyncSession):
    pizza = await get_pizza_by_id(pizza_id, session)
    user = await get_user_by_id_selectin_favorite_pizzas(user_id, session)
    user.favorite_pizzas.remove(pizza)
    await session.commit()
    return status.HTTP_200_OK


async def get_pizza_by_id(pizza_id: int, session: AsyncSession):
    return (await session.execute(select(Pizza).filter_by(id=pizza_id))).scalar_one_or_none()
