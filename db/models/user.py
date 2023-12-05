from sqlalchemy import Integer, Column, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from db.db_setup import Base
from validation.user import Crust, Sauce, Toppings
from db.models.favorite_pizzas_table import favorite_pizzas_table


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    address = Column(String)
    orders = relationship('Order', back_populates='user')
    custom_pizzas = relationship('Pizza', back_populates='user')
    favorite_pizzas = relationship('Pizza', secondary=favorite_pizzas_table)
    favorite_crusts = Column(ARRAY(Enum(Crust)))
    favorite_sauces = Column(ARRAY(Enum(Sauce)))
    favorite_toppings = Column(ARRAY(Enum(Toppings)))

