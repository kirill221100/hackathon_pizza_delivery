from sqlalchemy import Integer, Column, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from validation.pizza import Crust, Sauce, Toppings, Size
from db.db_setup import Base
from db.models.favorite_pizzas_table import favorite_pizzas_table

class Pizza(Base):
    __tablename__ = 'pizzas'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=True)
    crust = Column(Enum(Crust))
    sauce = Column(Enum(Sauce))
    toppings = Column(ARRAY(Enum(Toppings)))
    size = Column(Enum(Size))
    price = Column(Integer)
    picture = Column(String, nullable=True)
    is_custom = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='custom_pizzas')
    users_favorite = relationship('User', secondary=favorite_pizzas_table)
    pizza_orders = relationship('PizzaOrder', back_populates='pizza')


class PizzaOrder(Base):
    __tablename__ = 'pizza_orders'
    id = Column(Integer, primary_key=True)
    pizza_id = Column(Integer, ForeignKey('pizzas.id'))
    pizza = relationship('Pizza', back_populates='pizza_orders')
    amount = Column(Integer)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship('Order', back_populates='pizzas')

