"""Pydantic модель для первого запроса."""
from pydantic import BaseModel


class SendDownloadResponse(BaseModel):
    """Ответ первого эндпоинта - статус ответа.

    Args:
        BaseModel (_type_): _description_
    """

    status: str
