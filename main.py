from fastapi import FastAPI
from contextlib import asynccontextmanager
from security.config import get_config
from routes.auth import auth_router
from routes.order import order_router
from routes.pizza import pizza_router
from db.db_setup import init_db
import uvicorn


@asynccontextmanager
async def on_startup(app: FastAPI):
    await init_db()
    yield

app = FastAPI(debug=get_config().DEBUG, lifespan=on_startup)
app.include_router(auth_router, prefix='/auth')
app.include_router(order_router, prefix='/order')
app.include_router(pizza_router, prefix='/pizza')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
