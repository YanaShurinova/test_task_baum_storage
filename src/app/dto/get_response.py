"""Pydantic модель для результата одного из эндпоинтов."""
from datetime import datetime

from pydantic import BaseModel


class GetResponse(BaseModel):
    """Ответ второго эндпоинта состоит из списка объектов данного типа.

    Args:
        BaseModel (_type_): _description_
    """

    datetime: datetime
    title: str
    x_avg_count_in_line: float
