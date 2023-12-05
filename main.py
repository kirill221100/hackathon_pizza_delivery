from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from security.config import get_config
from routes.auth import auth_router
from routes.order import order_router
from routes.pizza import pizza_router
from routes.user import user_router
from db.db_setup import init_db
import uvicorn


@asynccontextmanager
async def on_startup(app: FastAPI):
    await init_db()
    yield

app = FastAPI(debug=get_config().DEBUG, lifespan=on_startup, title='LeoSlice API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(order_router, prefix='/order', tags=['order'])
app.include_router(pizza_router, prefix='/pizza', tags=['pizza'])
app.include_router(user_router, prefix='/user', tags=['user'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
