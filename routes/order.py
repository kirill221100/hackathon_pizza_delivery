from fastapi import APIRouter, Depends, status, Header
from fastapi.websockets import WebSocket
from typing import List
from security.oauth import get_current_user, get_current_user_ws
from validation.order import Order as OrderValidation, Status, OrderResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.order import create_order, get_order_by_id_selectin_pizzas, repeat_order, change_order_status_ws, \
    get_all_user_orders, get_all_active_user_orders, get_all_delivered_user_orders, users_orders_ws

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


@order_router.post('/change-status/{user_id}/{order_id}', status_code=status.HTTP_200_OK)
async def change_order_status_ws_path(user_id: int, order_id: int, status: Status, session: AsyncSession = Depends(get_session)):
    return await change_order_status_ws(user_id, order_id, status, session)


@order_router.websocket('/users-orders-ws')
async def users_orders_ws_path(ws: WebSocket, user_token: str):
    user = await get_current_user_ws(user_token)
    await users_orders_ws(ws, user['id'])
