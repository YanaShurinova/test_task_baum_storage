"""Модуль для автогенерации таблиц."""
from sqlalchemy import Column, DateTime, Integer, String

from src.app.db.base import Base


class XInTextString(Base):
    """Таблица БД.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'x_in_text_string'

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, nullable=True)
    title = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
