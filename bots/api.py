import os

import aiohttp
from aiohttp import client_exceptions
from dotenv import load_dotenv

load_dotenv()


async def get_content(pk):
    """Получение json с медиа-контентом."""
    url = os.getenv('URL_CONTENT') + 'media' + f'/{pk}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json = await response.json()
            return json[0]


async def get_media_by_url(url):
    """Получение файла изображения по url."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response_image:
                if response_image.status == 200:
                    return await response_image.read()
                return None
        except (
                client_exceptions.ClientConnectorError,
                client_exceptions.InvalidURL
        ):
            return None


async def send_file_id(pk, file_id):
    """Отправка file_id изображений из Телеграм в БД."""
    url = os.getenv('URL_CONTENT') + 'media' + f'/{pk}'
    async with aiohttp.ClientSession() as session:
        await session.post(url, data={'pk': pk, 'file_id': file_id})
