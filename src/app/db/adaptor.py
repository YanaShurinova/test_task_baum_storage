"""Модуль для подключения к БД."""
from asyncio import current_task

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


class DatabaseConnection:
    """Класс для подключения к БД."""

    def __init__(self):
        """."""
        _engine = create_async_engine(
            url='postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}'.format(
                DB_USER,
                DB_PASS,
                DB_HOST,
                DB_PORT,
                DB_NAME,
            ),
        )
        async_session_factory = sessionmaker(
            _engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self._session_generator = async_scoped_session(
            async_session_factory,
            scopefunc=current_task,
        )

    def get_session(self) -> AsyncSession:
        """_summary_.

        Returns:
            AsyncSession: _description_
        """
        return self._session_generator()
