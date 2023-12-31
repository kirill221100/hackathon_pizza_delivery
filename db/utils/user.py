from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from security.password import verify_pass, hash_password
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from validation.auth import UserAuth
from validation.user import FavoriteIngredients
from db.models.user import User


async def create_user(user_data: UserAuth, session: AsyncSession):
    user = User(username=user_data.username, hashed_password=hash_password(user_data.password))
    session.add(user)
    await session.commit()
    await session.flush()
    return {'username': user_data.username, 'id': user.id}


async def login_user(user_data: OAuth2PasswordRequestForm, session: AsyncSession):
    if user := await get_user_by_username(user_data.username, session):
        if verify_pass(user_data.password, user.hashed_password):
            return {'username': user_data.username, 'id': user.id}
    raise HTTPException(status_code=401, detail='incorrect password or username',
                        headers={"WWW-Authenticate": "Bearer"})


async def edit_user_address(new_address: str, user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    user.address = new_address
    await session.commit()
    return status.HTTP_200_OK


async def edit_favorite_ingredients(favourite_ingredients: FavoriteIngredients, user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    if favourite_ingredients.crusts:
        user.favorite_crusts = favourite_ingredients.crusts
    if favourite_ingredients.sauces:
        user.favorite_sauces = favourite_ingredients.sauces
    if favourite_ingredients.toppings:
        user.favorite_toppings = favourite_ingredients.toppings
    await session.commit()
    return status.HTTP_200_OK


async def get_user_by_username(username: str, session: AsyncSession):
    return (await session.execute(select(User).filter_by(username=username))).scalar_one_or_none()


async def get_user_by_id(user_id: int, session: AsyncSession):
    return (await session.execute(select(User).filter_by(id=user_id))).scalar_one_or_none()


async def get_user_by_id_selectin_favorite_pizzas(user_id: int, session: AsyncSession):
    return (await session.execute(select(User).filter_by(id=user_id).options(selectinload(User.favorite_pizzas))))\
        .scalar_one_or_none()


async def get_user_by_id_selectin_custom_pizzas(user_id: int, session: AsyncSession):
    # limit = per_page * page
    # offset = (page - 1) * per_page
    return (await session.execute(select(User).filter_by(id=user_id).options(selectinload(User.custom_pizzas))))\
        .scalar_one_or_none()


async def get_favorite_pizzas(user_id: int, session: AsyncSession):
    # limit = per_page * page
    # offset = (page - 1) * per_page
    user = await get_user_by_id_selectin_favorite_pizzas(user_id, session)
    return user.favorite_pizzas


async def get_custom_pizzas(user_id: int, session: AsyncSession):
    # limit = per_page * page
    # offset = (page - 1) * per_page
    user = await get_user_by_id_selectin_custom_pizzas(user_id, session)
    return user.custom_pizzas


async def get_favorite_ingredients(user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    return {'crusts': user.favorite_crusts, 'sauces': user.favorite_sauces, 'toppings': user.favorite_toppings}

