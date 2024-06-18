from app.models import Base
from app.database import engine
from sqlalchemy import select
from app.database import get_session
from app.models import User, Product, ProductUpdate, UserProduct
from app.database import session

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_user(session: session, telegram_id: int, username: str) -> User:
    new_user = User(telegram_id=telegram_id, username=username)
    session.add(new_user)
    session.commit()
    return new_user

def add_product(session: session, user_id: int, url: str) -> Product:
    new_product = Product(user_id=user_id, url=url)
    session.add(new_product)
    session.commit()
    return new_product

def add_product_update(session: session, user_product_id: int, rating: float, grades: int, orders: int, values: int):
    new_update = ProductUpdate(user_product_id=user_product_id, rating=rating, grades=grades, orders=orders,
                               values=values)
    session.add(new_update)
    session.commit()

def get_product_statistics(session: session, product_id: int):
    updates = session.query(ProductUpdate).join(UserProduct).filter(UserProduct.product_id == product_id).order_by(
        ProductUpdate.updated_date).all()
    if len(updates) < 25:
        return None, None
    first_update = updates[0]
    last_update = updates[-1]
    return first_update, last_update

def add_user_product(session: session, telegram_id: int, username: str, url: str):
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = add_user(session, telegram_id=telegram_id, username=username)

    product = add_product(session, user.id, url)
    user_product = UserProduct(user_id=user.id, product_id=product.id)
    session.add(user_product)
    session.commit()
    return user, product, user_product
