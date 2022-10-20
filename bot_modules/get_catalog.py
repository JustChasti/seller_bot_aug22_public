from loguru import logger
from db.dj_db import get_catalog
from config import bot, catalog_chunk
from bot_modules.keyboards import catalog_keyboard, main_keyboard
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def bot_catalog(message, page):
    data = get_catalog(chunk=catalog_chunk)
    current_page = data[page]
    for i in current_page:
        try:
            image = open(i[4], 'rb')
            text = f'*{i[1]}*\nДоступно: *{i[2]}*\nЦена: *{i[3]}*'
            callback_keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(
                text='Добавить в Корзину',
                callback_data=i[0]
            )
            callback_keyboard.add(button)
            bot.send_photo(
                message.chat.id,
                image,
                caption=text,
                reply_markup=callback_keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.exception(e)
    bot.send_message(
        message.chat.id,
        'Выберете вариант',
        reply_markup=catalog_keyboard
    )


def working_with_catalog(message, page):
    if message.text == 'Следующие':
        bot_catalog(message, page+1)
        bot.register_next_step_handler(message, working_with_catalog, page+1)
    elif message.text == 'Предыдущие':
        if page <= 0:
            page = 1
        bot_catalog(message, page-1)
        bot.register_next_step_handler(message, working_with_catalog, page-1)
    elif message.text == 'Назад':
        bot.send_message(
            message.chat.id,
            'Выберете вариант',
            reply_markup=main_keyboard
        )
    else:
        pass
