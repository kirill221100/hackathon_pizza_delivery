from datetime import datetime
from fastapi import Depends, HTTPException, status as status_response
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from validation.order import Order as OrderValidation, Status, OrderResponse
from validation.pizza import PizzaOrderResponse
from db.models.order import Order
from db.models.pizza import PizzaOrder
from db.utils.user import get_user_by_id
from db.utils.pizza import get_pizza_by_id, create_pizza_order
from utils.ws import users_orders_manager


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
    await session.flush()
    pizzas_json = [PizzaOrderResponse.model_validate(i, from_attributes=True) for i in order.pizzas]
    order_json = {'id': order.id,
                  'user_id': user_id,
                  'pizzas': pizzas_json,
                  'price': order.price,
                  'date': order.date,
                  'status': order.status,
                  'address': order.address}
    await users_orders_manager.send_data(user_id, {'type': 'new_order',
                                                   'order': jsonable_encoder(OrderResponse.model_validate(order_json))})
    return order


async def repeat_order(order_id: int, user_id: int, session: AsyncSession):
    order = await get_order_by_id_selectin_pizzas(order_id, user_id, session)
    order.status = Status.PREPARING
    order.date = datetime.now()
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
                                               .options(selectinload(Order.pizzas).selectinload(PizzaOrder.pizza)))).scalar_one_or_none():
        return order
    raise HTTPException(status_code=404, detail='There is no your order with such id')


async def get_all_user_orders(user_id: int, session: AsyncSession, page: int, per_page: int):
    limit = per_page * page
    offset = (page - 1) * per_page
    return (await session.execute(select(Order).filter_by(user_id=user_id)
                                  .options(selectinload(Order.pizzas).selectinload(PizzaOrder.pizza)).order_by(Order.date.desc())
                                  .limit(limit).offset(offset))).scalars().all()


async def get_all_active_user_orders(user_id: int, session: AsyncSession, page: int, per_page: int):
    limit = per_page * page
    offset = (page - 1) * per_page
    return (await session.execute(select(Order).filter(Order.user_id == user_id,
                                                       Order.status not in (Status.CANCELLED, Status.DELIVERED))
                                  .options(selectinload(Order.pizzas).selectinload(PizzaOrder.pizza)).order_by(Order.date.desc())
                                  .limit(limit).offset(offset))).scalars().all()


async def get_all_delivered_user_orders(user_id: int, session: AsyncSession, page: int, per_page: int):
    limit = per_page * page
    offset = (page - 1) * per_page
    return (await session.execute(select(Order).filter(Order.user_id == user_id,
                                                       Order.status == Status.DELIVERED)
                                  .options(selectinload(Order.pizzas).selectinload(PizzaOrder.pizza)).order_by(Order.date.desc())
                                  .limit(limit).offset(offset))).scalars().all()


async def change_order_status_ws(user_id: int, order_id: int, status: Status, session: AsyncSession):
    order = await get_order_by_id_no_user_id(order_id, session)
    order.status = status
    await session.commit()
    await users_orders_manager.send_data(user_id, {'type': 'change_status', 'status': status.value, 'order_id': order_id})
    return status_response.HTTP_200_OK


async def users_orders_ws(ws: WebSocket, user_id: int):
    await users_orders_manager.connect(user_id, ws)
    try:
        while True:
            data = await ws.receive_text()
            await users_orders_manager.send_data(user_id, data)
    except WebSocketDisconnect:
        await users_orders_manager.disconnect(user_id, ws)
