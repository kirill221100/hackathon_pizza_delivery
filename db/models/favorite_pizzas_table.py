from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from db.db_setup import Base

favorite_pizzas_table = Table(
    "favorite_pizzas_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("pizza_id", ForeignKey("pizzas.id")),
)
