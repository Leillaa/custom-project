import logging
import os
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling, start_webhook
from dotenv import load_dotenv

import api
import keyboards as kb

load_dotenv()


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

TOKEN_BBT_BOT = os.getenv('TOKEN_BBT_BOT')

DEBUG = os.getenv('DEBUG')

HOST_APP_NAME = os.getenv('HOST_APP_NAME')

WEBHOOK_HOST = f'https://{HOST_APP_NAME}'
WEBHOOK_PATH = f'/webhook/{TOKEN_BBT_BOT}'

WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.getenv('PORT', default=8000)
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

logging.basicConfig(
    level=logging.DEBUG,
    filename='bot.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('logger.log',
                              maxBytes=50000000,
                              backupCount=5)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """Выдача контента меню."""
    telegram_id = message.from_user.id
    keyboard = await kb.get_keyboard(telegram_id, pk=None)
    await message.reply(
        f'{keyboard["title"]} 👇',
        reply_markup=keyboard['inline_keyboard_markup']
    )
    await message.answer(
        'Вы всегда можете вернуться, нажав кнопку "Назад" или "В меню"',
        reply_markup=kb.keyboard
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('content_'))
async def process_callback(callback_query: types.CallbackQuery):
    """Выдача контента по нажатию на инлайн-кнопку."""
    telegram_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    content_id = callback_query.data.replace('content_', '')
    keyboard = await kb.get_keyboard(telegram_id, content_id)
    if keyboard['inline_keyboard_markup']['inline_keyboard']:
        await callback_query.message.answer(
            f'{keyboard["title"]} 👇',
            reply_markup=keyboard['inline_keyboard_markup']
        )
    else:
        content = await api.get_content(content_id)
        media_url = content.get('media')
        program = content.get('program')
        file_id = content.get('file_id')
        date_on = content.get('date_on')
        date_off = content.get('date_off')
        if date_on and date_off:
            date_on = datetime.strptime(date_on, '%Y-%m-%d')
            date_off = datetime.strptime(date_off, '%Y-%m-%d')
            delta = date_off - date_on + timedelta(days=1)
            program = (
                    'Даты проведения программы: ' +
                    date_on.strftime('%d.%m.%Y') + ' - ' +
                    date_off.strftime('%d.%m.%Y') +
                    f' ({delta.days} дней)' + '\n\n' +
                    program
            )
        if file_id:
            return await send_message_with_photo(
                chat_id=telegram_id,
                photo=file_id,
                program=program
            )
        media = await api.get_media_by_url(media_url)
        if media:
            res = await send_message_with_photo(
                chat_id=telegram_id,
                photo=media,
                program=program
            )
            file_id = res.photo[-1].file_id
            return await api.send_file_id(content_id, file_id)
        return await bot.send_message(chat_id=telegram_id, text=program)


async def send_message_with_photo(chat_id, photo, program):
    """Отправка фото и текста."""
    if len(program) < 1024:
        res = await bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=program
        )
    else:
        res = await bot.send_photo(chat_id=chat_id, photo=photo)
        await bot.send_message(chat_id=chat_id, text=program)
    return res


@dp.message_handler(lambda message: message.text == 'В меню')
async def process_back_to_menu(message: types.Message):
    """Возврат в контент меню."""
    telegram_id = message.from_user.id
    keyboard = await kb.get_keyboard(telegram_id, pk=None)
    await message.answer(
        f'{keyboard["title"]} 👇',
        reply_markup=keyboard['inline_keyboard_markup']
    )


@dp.message_handler(lambda message: message.text == 'Назад')
async def process_back(message: types.Message):
    """Возврат к предыдущему контенту."""
    telegram_id = message.from_user.id
    keyboard = await kb.get_keyboard_back(telegram_id)
    await message.answer(
        f'{keyboard["title"]} 👇',
        reply_markup=keyboard['inline_keyboard_markup']
    )


if __name__ == '__main__':
    if DEBUG:
        start_polling(dp)
    else:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            skip_updates=True,
            on_shutdown=on_shutdown,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
