from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from validation.order import Status
from db.db_setup import Base


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now())
    address = Column(String)
    pizzas = relationship('PizzaOrder', back_populates='order')
    status = Column(Enum(Status), default=Status.PREPARING)
    price = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')
