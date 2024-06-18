import datetime
from sqlalchemy import MetaData, text, ForeignKey
from typing import Annotated
from sqlalchemy.sql.sqltypes import DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


metadata = Base.metadata
intpk = Annotated[int, mapped_column(primary_key=True)]


# Декларативный таблицы
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(unique=True, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    products = relationship('Product', back_populates='user')
    user_products = relationship('UserProduct', back_populates='user')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)

    user = relationship('User', back_populates='products')
    user_products = relationship('UserProduct', back_populates='product')


class UserProduct(Base):
    __tablename__ = 'user_products'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    start_tracking_date: Mapped[Date] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    user = relationship('User', back_populates='user_products')
    product = relationship('Product', back_populates='user_products')
    product_updates = relationship('ProductUpdate', back_populates='user_product')


class ProductUpdate(Base):
    __tablename__ = 'product_updates'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_product_id: Mapped[int] = mapped_column(ForeignKey('user_products.id'), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=True)
    grades: Mapped[int] = mapped_column(nullable=True)
    orders: Mapped[int] = mapped_column(nullable=True)
    values: Mapped[int] = mapped_column(nullable=True)
    updated_date: Mapped[Date] = mapped_column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    user_product = relationship('UserProduct', back_populates='product_updates')
