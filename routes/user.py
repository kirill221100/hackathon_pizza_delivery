from fastapi import APIRouter, Depends
from security.oauth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from typing import List
from validation.user import FavoriteIngredients
from db.utils.pizza import add_favorite_pizza, delete_from_favorite_pizza
from db.utils.user import edit_user_address, edit_favorite_ingredients, get_user_by_id

user_router = APIRouter()


@user_router.patch('/edit-user-address')
async def edit_user_address_path(new_address: str, user=Depends(get_current_user),
                                 session: AsyncSession = Depends(get_session)):
    return await edit_user_address(new_address, user['id'], session)


@user_router.put('/edit-favorite-ingredients')
async def edit_favorite_ingredients_path(ingredients: FavoriteIngredients, user=Depends(get_current_user),
                                         session: AsyncSession = Depends(get_session)):
    return await edit_favorite_ingredients(ingredients, user['id'], session)


@user_router.patch('/add-favorite-pizza')
async def add_favorite_pizza_path(pizza_id: int, user=Depends(get_current_user),
                                  session: AsyncSession = Depends(get_session)):
    return await add_favorite_pizza(pizza_id, user['id'], session)


@user_router.delete('/delete-from-favorite-pizza')
async def delete_from_favorite_pizza_path(pizza_id: int, user=Depends(get_current_user),
                                          session: AsyncSession = Depends(get_session)):
    return await delete_from_favorite_pizza(pizza_id, user['id'], session)


@user_router.get('/get-user-by-id/{user_id}')
async def get_user_by_id_path(user_id: int, session: AsyncSession = Depends(get_session)):
    return await get_user_by_id(user_id, session)
