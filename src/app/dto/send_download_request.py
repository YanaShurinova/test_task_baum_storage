"""Pydantic модель для отправки сообщений брокеру."""
from datetime import datetime

from pydantic import BaseModel


class SendDownloadRequest(BaseModel):
    """.

    Args:
        BaseModel (_type_): _description_
    """

    datetime: datetime
    title: str
    text: str
