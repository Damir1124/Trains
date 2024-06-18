from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Table, Date, Float
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    created_date = Column(Date, nullable=False)

    products = relationship('Product', back_populates='user')
    user_products = relationship('UserProduct', back_populates='user')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    url = Column(String, nullable=False)

    user = relationship('User', back_populates='products')
    user_products = relationship('UserProduct', back_populates='product')


class UserProduct(Base):
    __tablename__ = 'user_products'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    start_tracking_date = Column(Date, nullable=False)

    user = relationship('User', back_populates='user_products')
    product = relationship('Product', back_populates='user_products')
    product_updates = relationship('ProductUpdate', back_populates='user_product')


class ProductUpdate(Base):
    __tablename__ = 'product_updates'

    id = Column(Integer, primary_key=True)
    user_product_id = Column(Integer, ForeignKey('user_products.id'), nullable=False)
    rating = Column(Float, nullable=True)
    grades = Column(Integer, nullable=True)
    orders = Column(Integer, nullable=True)
    values = Column(Integer, nullable=True)
    updated_date = Column(Date, nullable=False)

    user_product = relationship('UserProduct', back_populates='product_updates')

