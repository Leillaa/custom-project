import os

import aiohttp
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from dotenv import load_dotenv

load_dotenv()

button_1 = KeyboardButton(text='В меню')
button_2 = KeyboardButton(text='Назад')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard.row(button_1, button_2)


async def get_keyboard_base(url):
    """Формирование инлайн-кнопок."""
    result = dict()
    result['title'] = 'Выберите'
    inline_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json = await response.json()
            for i in range(len(json)):
                title = json[i].get('title')
                content_id = json[i].get('id')
                url = json[i].get('proof_link')
                parent_title = json[i].get('parent_title')
                if parent_title:
                    result['title'] = parent_title
                inline_button = InlineKeyboardButton(
                    text=title,
                    url=url,
                    callback_data=f'content_{content_id}',
                )
                inline_keyboard.add(inline_button)
        result['inline_keyboard_markup'] = inline_keyboard
        return result


async def get_keyboard(telegram_id, pk):
    """Получение дочернего контента для инлайн-кнопки с id=pk.
    Отправка данных о нажатии на кнопку.
    """
    url = (
            os.getenv('URL_CONTENT') +
            f'{telegram_id}' +
            (f'/{pk}' if pk else '')
    )
    async with aiohttp.ClientSession() as session:
        await session.post(url, data={'telegram_id': telegram_id, 'pk': pk})
    return await get_keyboard_base(url)


async def get_keyboard_back(telegram_id):
    """Получение предыдущего контента."""
    url = os.getenv('URL_CONTENT') + f'back/{telegram_id}'
    return await get_keyboard_base(url)
