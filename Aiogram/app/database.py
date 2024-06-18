from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings
from contextlib import contextmanager

# Создание движка базы данных
engine = create_engine(settings.DB_url, echo=True)

# Создание фабрики сессий
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()

class Base(DeclarativeBase):
    pass

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
