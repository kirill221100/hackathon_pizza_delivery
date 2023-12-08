from fastapi import Depends, HTTPException, status
from fastapi.websockets import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from validation.order import Order as OrderValidation, Status
from db.models.order import Order
from db.models.pizza import PizzaOrder
from db.utils.user import get_user_by_id
from db.utils.pizza import get_pizza_by_id, create_pizza_order
from utils.ws import manager


async def create_order(order_data: OrderValidation, user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    order = Order(address=order_data.address, price=0, user=user)
    for pizza_order in order_data.pizzas:
        pizza_order_db = await create_pizza_order(pizza_order.pizza_id, pizza_order.amount, session)
        order.pizzas.append(pizza_order_db)
        session.add(pizza_order_db)
        order.price += pizza_order_db.pizza.price * pizza_order_db.amount
    session.add(order)
    await session.commit()
    return order


async def repeat_order(order_id: int, user_id: int, session: AsyncSession):
    order = await get_order_by_id_selectin_pizzas(order_id, user_id, session)
    order.status = Status.PREPARING
    await session.commit()
    return order


async def get_order_by_id(order_id: int, user_id: int, session: AsyncSession):
    if order := (await session.execute(select(Order).filter_by(id=order_id, user_id=user_id))).scalar_one_or_none():
        return order
    raise HTTPException(status_code=404, detail='There is no your order with such id')


async def get_order_by_id_no_user_id(order_id: int, session: AsyncSession):
    if order := (await session.execute(select(Order).filter_by(id=order_id))).scalar_one_or_none():
        return order
    raise HTTPException(status_code=404, detail='There is no order with such id')


async def get_order_by_id_selectin_pizzas(order_id: int, user_id: int, session: AsyncSession):
    if order := (await session.execute(select(Order).filter_by(id=order_id, user_id=user_id)
                                               .options(selectinload(Order.pizzas)))).scalar_one_or_none():
        return order
    raise HTTPException(status_code=404, detail='There is no your order with such id')


async def get_all_user_orders(user_id: int, session: AsyncSession, page: int, per_page: int):
    limit = per_page * page
    offset = (page - 1) * per_page
    return (await session.execute(select(Order).filter_by(user_id=user_id)
                                  .options(selectinload(Order.pizzas).selectinload(PizzaOrder.pizza))
                                  .limit(limit).offset(offset))).scalars().all()


async def get_all_active_user_orders(user_id: int, session: AsyncSession, page: int, per_page: int):
    limit = per_page * page
    offset = (page - 1) * per_page
    return (await session.execute(select(Order).filter(Order.user_id == user_id,
                                                       Order.status not in (Status.CANCELLED, Status.DELIVERED))
                                  .options(selectinload(Order.pizzas))
                                  .limit(limit).offset(offset))).scalars().all()


async def get_all_delivered_user_orders(user_id: int, session: AsyncSession, page: int, per_page: int):
    limit = per_page * page
    offset = (page - 1) * per_page
    return (await session.execute(select(Order).filter(Order.user_id == user_id,
                                                       Order.status == Status.DELIVERED)
                                  .options(selectinload(Order.pizzas))
                                  .limit(limit).offset(offset))).scalars().all()


async def change_status_ws(ws: WebSocket, order_id: int, status: Status, session: AsyncSession):
    order = await get_order_by_id_no_user_id(order_id, session)
    order.status = status
    await session.commit()
    await manager.connect(order_id, ws)
    await manager.send_text(order_id, status.value)
    await manager.disconnect(order_id, ws)


async def order_status_ws(ws: WebSocket, order_id: int, session: AsyncSession):
    order = await get_order_by_id_no_user_id(order_id, session)
    await manager.connect(order_id, ws)
    try:
        while True:
            text = await ws.receive_text()
            await manager.send_text(order, text)
    except WebSocketDisconnect:
        await manager.disconnect(order_id, ws)
