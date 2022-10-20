from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.dj_db import basket_creation, get_products_in_basket
from db.dj_db import get_product_by_id, get_basket_by_telegram
from db.dj_db import change_product_in_busket, remove_product_from_busket
from db.dj_db import clear_busket
from config import bot
from bot_modules.keyboards import main_keyboard, sumbit_keyboard


def get_basket(telegram_id):
    basket = basket_creation(telegram_id)
    data = get_products_in_basket(basket)
    bot.send_message(telegram_id, 'Товары вашей корзины:')
    for i in data:
        text = f'Название: *{i["title"]}*\nКоличество: *{i["count"]}*\nЦена: *{i["price"]}*'
        callback_keyboard = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(
            text='Изменить Количество',
            callback_data=f"{i['id']}/Изменить"
        )
        button2 = InlineKeyboardButton(
            text='Удалить',
            callback_data=f"{i['id']}/Удалить"
        )
        callback_keyboard.add(button1, button2)
        bot.send_message(
            telegram_id,
            text,
            reply_markup=callback_keyboard,
            parse_mode="Markdown"
        )


def sum_cheker(telegram_id):
    basket = basket_creation(telegram_id)
    data = get_products_in_basket(basket)
    errors = []
    result = True
    total = 0
    for i in data:
        product = get_product_by_id(i['id'])
        if i['count'] > product.count:
            errors.append({
                'message': f"""
Максимальное количество товара {product.title}
 для заказа на данный момент: {product.count}
 в вашей корзине его: {i['count']}, уменьшите количество
 этого товара до доступного
"""})
            result = False
        else:
            total += i['count'] * product.price
    return result, errors, total


def remove_product(message, product_id):
    product = get_product_by_id(product_id)
    basket = get_basket_by_telegram(message.chat.id)
    remove_product_from_busket(product, basket)
    get_basket(message.chat.id)
    # bot.register_next_step_handler(message, basket_total_amount)
    bot.send_message(
        message.chat.id,
        'Если вы хотите оплатить покупки - нажмите оплатить',
        reply_markup=sumbit_keyboard
    )


def change_product_count(message, product_id):
    try:
        count = int(message.text)
        product = get_product_by_id(product_id)
        basket = get_basket_by_telegram(message.chat.id)
        if count > 0:
            change_product_in_busket(product, basket, count)
        else:
            remove_product_from_busket(product, basket)
    except Exception as e:
        pass
    get_basket(message.chat.id)
    bot.register_next_step_handler(message, basket_total_amount)
    bot.send_message(
        message.chat.id,
        'Если вы хотите оплатить покупки - нажмите оплатить',
        reply_markup=sumbit_keyboard
    )


def basket_total_amount(message):
    if message.text == 'Оплатить':
        result, errors, total = sum_cheker(message.chat.id)
        if result:
            bot.send_message(
                message.chat.id,
                f'Итоговая сумма вашего заказа {total}',
                reply_markup=sumbit_keyboard
            )
            bot.register_next_step_handler(message, waiting_to_payment)
        else:
            for i in errors:
                bot.send_message(message.chat.id, i['message'])
            get_basket(message.chat.id)
            bot.register_next_step_handler(message, basket_total_amount)
            bot.send_message(
                message.chat.id,
                'Если вы хотите оплатить покупки - нажмите оплатить',
                reply_markup=sumbit_keyboard
            )
    elif message.text == 'Назад':
        bot.send_message(
            message.chat.id,
            'Выберете вариант',
            reply_markup=main_keyboard
        )
    else:
        pass


def waiting_to_payment(message):
    if message.text == 'Оплатить':
        basket = get_basket_by_telegram(message.chat.id)
        clear_busket(basket)
        bot.send_message(
            message.chat.id,
            'Тут будет кнопка отправки чека',
            reply_markup=main_keyboard
        )
    elif message.text == 'Назад':
        get_basket(message.chat.id)
        bot.send_message(
            message.chat.id,
            'Выберете вариант',
            reply_markup=sumbit_keyboard
        )
        bot.register_next_step_handler(message, basket_total_amount)
    else:
        pass
