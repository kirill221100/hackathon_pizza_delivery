from fastapi import APIRouter, Depends
from fastapi.websockets import WebSocket
from typing import List
from security.oauth import get_current_user
from validation.order import Order as OrderValidation, Status, OrderResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.order import create_order, get_order_by_id_selectin_pizzas, repeat_order, change_status_ws, \
    get_all_user_orders, get_all_active_user_orders, get_all_delivered_user_orders, order_status_ws

order_router = APIRouter()


@order_router.post('/new-order', response_model=OrderResponse)
async def new_order_path(order_data: OrderValidation, user=Depends(get_current_user),
                         session: AsyncSession = Depends(get_session)):
    return await create_order(order_data, user['id'], session)


@order_router.post('/repeat-order/{order_id}', response_model=OrderResponse)
async def repeat_order_path(order_id: int, user=Depends(get_current_user),
                            session: AsyncSession = Depends(get_session)):
    return await repeat_order(order_id, user['id'], session)


@order_router.get('/get-order-by-id/{order_id}', response_model=OrderResponse)
async def get_order_by_id_path(order_id: int, user=Depends(get_current_user),
                               session: AsyncSession = Depends(get_session)):
    return await get_order_by_id_selectin_pizzas(order_id, user['id'], session)


@order_router.get('/get-all-user-orders', response_model=List[OrderResponse])
async def get_all_user_orders_path(user=Depends(get_current_user),
                                   session: AsyncSession = Depends(get_session), page: int = 1, per_page: int = 3):
    return await get_all_user_orders(user['id'], session, page, per_page)


@order_router.get('/get-all-active-user-orders', response_model=List[OrderResponse])
async def get_all_active_user_orders_path(user=Depends(get_current_user),
                                          session: AsyncSession = Depends(get_session), page: int = 1,
                                          per_page: int = 3):
    return await get_all_active_user_orders(user['id'], session, page, per_page)


@order_router.get('/get-all-delivered-user-orders', response_model=List[OrderResponse])
async def get_all_delivered_user_orders_path(user=Depends(get_current_user),
                                             session: AsyncSession = Depends(get_session), page: int = 1,
                                             per_page: int = 3):
    return await get_all_delivered_user_orders(user['id'], session, page, per_page)


@order_router.websocket('/change-status/{order_id}/{status}')
async def change_status_ws_path(ws: WebSocket, order_id: int, status: Status,
                                session: AsyncSession = Depends(get_session)):
    await change_status_ws(ws, order_id, status, session)


@order_router.websocket('/order-status-ws/{order_id}')
async def order_status_ws_path(ws: WebSocket, order_id: int, session: AsyncSession = Depends(get_session)):
    await order_status_ws(ws, order_id, session)
