from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from validation.order import Order as OrderValidation
from db.models.order import Order
from db.utils.user import get_user_by_id
from db.utils.pizza import get_pizza_by_id, create_pizza_order


async def create_order(order_data: OrderValidation, user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    order = Order(address=order_data.address, price=0, user=user)
    for pizza_order in order_data.pizza_orders:
        pizza_order_db = await create_pizza_order(pizza_order.pizza_id, pizza_order.amount, session)
        order.pizzas.append(pizza_order_db)
        session.add(pizza_order_db)
        order.price += pizza_order_db.pizza.price * pizza_order_db.amount
    session.add(order)
    await session.commit()
    return {'order_id': order.id}


async def get_order_by_id(order_id: int, user_id: int, session: AsyncSession):
    if order := (await session.execute(select(Order).filter_by(id=order_id, user_id=user_id))).scalar_one_or_none():
        return order
    raise HTTPException(status_code=404, detail='There is no your order with such id')


