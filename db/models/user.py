from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship
from db.db_setup import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    address = Column(String)
    orders = relationship('Order', back_populates='user')
    custom_pizzas = relationship('Pizza', back_populates='user')


