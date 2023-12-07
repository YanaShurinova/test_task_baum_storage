"""Модуль для работы с БД."""

from datetime import datetime
from typing import List

from sqlalchemy import insert, select
from sqlalchemy.sql import functions

from src.app.db.model import XInTextString
from src.app.dto.get_response import GetResponse
from src.app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository):
    """Класс для работы с БД.

    Args:
        BaseRepository (_type_): _description_
    """

    async def input_value(self, datetime: datetime, title: str, line: str):
        """Метод для сохранения записи в БД.

        Args:
            datetime (datetime): дата запроса
            title (str): название файла
            line (str): строка
        """
        await self._session.execute(
            insert(XInTextString).values(
                datetime=datetime,
                title=title,
                length=len(line),
                value=line.count('х'),
            ),
        )
        await self._session.commit()

    async def get_all(self) -> List[GetResponse]:
        """Метод получения информации о среднем содержании х в файле.

        Returns:
            List[GetResponse]: список из (дата, название, ср. значение х)
        """
        notes_of_sum_x_in_text = (await self._session.execute(
            select(
                XInTextString.title,
                functions.sum(XInTextString.length),
                functions.sum(XInTextString.value),
                functions.max(XInTextString.datetime),
            ).group_by(XInTextString.title)
        )).all()
        x_avg_in_text = []
        for note in notes_of_sum_x_in_text:
            x_avg_in_text.append(GetResponse(
                datetime=note[3],
                title=note[0],
                x_avg_count_in_line=round(note[2]/note[1],3),
            ))
        return x_avg_in_text
