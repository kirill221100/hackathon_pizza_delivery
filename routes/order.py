from fastapi import APIRouter, Depends
from security.oauth import get_current_user
from validation.order import Order as OrderValidation
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.order import create_order, get_order_by_id

order_router = APIRouter()


@order_router.post('/new-order')
async def new_order_path(order_data: OrderValidation, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await create_order(order_data, user['id'], session)


@order_router.get('/get-order-by-id')
async def get_order_by_id_path(order_id: int, user=Depends(get_current_user),
                               session: AsyncSession = Depends(get_session)):
    return await get_order_by_id(order_id, user['id'], session)
