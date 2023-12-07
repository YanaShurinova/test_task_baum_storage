"""Основной модуль."""
import asyncio
import json
from datetime import datetime
from typing import List

import uvicorn
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from confluent_kafka.admin import AdminClient, NewTopic
from fastapi import FastAPI, UploadFile, status

from src.app.db.adaptor import DatabaseConnection
from src.app.dto.get_response import GetResponse
from src.app.dto.send_download_request import SendDownloadRequest
from src.app.dto.send_download_response import SendDownloadResponse
from src.app.repositories.transaction import TransactionRepository


def create_app():
    """Метод  по созданию fastapi приложения.

    Returns:
        Fastapi: app
    """
    app = FastAPI(docs_url='/')
    session = DatabaseConnection().get_session()

    admin_client = AdminClient({
        "bootstrap.servers": "localhost:9092"
    })
    topic_list = []
    topic_list.append(NewTopic("test_topic", 1, 1))
    admin_client.create_topics(topic_list)

    producer, consumer = AIOKafkaProducer(), AIOKafkaConsumer('test_topic')
    loop = asyncio.get_event_loop()

    async def consume():
        """Обработка сообщения из брокера."""
        async for msg in consumer:
            resp = json.loads(msg.value.decode('utf-8'))
            date = datetime.strptime(resp.get('datetime').replace("T", " "), '%Y-%m-%d %H:%M:%S.%f')
            await TransactionRepository(session).input_value(date,resp.get('title'), resp.get('text'))


    @app.on_event("startup")
    async def startup_event():
        """Ивент при открытии приложения."""
        await producer.start()
        await consumer.start()
        loop.create_task(consume())


    @app.on_event("shutdown")
    async def shutdown_event():
        """Ивент при закрытии приложения."""
        await producer.stop()
        await consumer.stop()

    @app.put("/send_download_text")
    async def send_download_text(file: UploadFile):
        """Эндпоинт по загружке и отправки исходных данных в брокер построчно.

        Args:
            file (UploadFile): исходный файл txt

        Returns:
            SendDownloadResponse: Статус ответа
        """
        date = datetime.now()
        with file.file as f:
            for line in f:
                if not line.isspace():
                    event = SendDownloadRequest(datetime=date, title=file.filename, text=line)
                    await producer.send(
                        topic='test_topic',
                        value=bytes(
                            str(event.json()),
                            encoding='utf-8',
                        ))
                    #asyncio.sleep(3)

    @app.get("/get_x_avg")
    async def get_x_avg()-> List[GetResponse]:
        """Эндпоинт по получению списка из объектов: дата, название, среднее значение х в тексте.

        Returns:
            List[GetResponse]: _description_
        """
        return await TransactionRepository(session).get_all()

    return app

def main():
    """."""
    uvicorn.run(
        f"{__name__}:create_app",
        host='0.0.0.0', port=8888,
        debug=True,
    )

if __name__ == 'main':
    main()
