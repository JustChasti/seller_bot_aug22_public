from config import bot
from telebot.types import ReplyKeyboardRemove
from bot_modules.get_catalog import bot_catalog, working_with_catalog
from bot_modules.basket import get_basket, basket_total_amount
from bot_modules.basket import change_product_count, remove_product
from bot_modules.keyboards import main_keyboard, catalog_keyboard
from bot_modules.keyboards import sumbit_keyboard
from db.dj_db import basket_creation, get_product_by_id
from db.dj_db import get_basket_by_telegram, add_product_too_basket


@bot.message_handler(commands=['help', 'start'])
def start_message(message):
    basket_creation(message.chat.id)
    text = "Привет, я бот для продажи, вот что я умею:"
    image = open('files/hello image.png', 'rb')
    bot.send_photo(
        chat_id=message.chat.id,
        photo=image,
        caption=text,
        reply_markup=main_keyboard
    )


@bot.message_handler(content_types=['text'])
def raw_text_handler(message):
    if message.text == 'Каталог':
        bot_catalog(message, page=0)
        bot.register_next_step_handler(message, working_with_catalog, page=0)
    elif message.text == 'Корзина':
        get_basket(message.chat.id)
        bot.register_next_step_handler(message, basket_total_amount)
        bot.send_message(
            message.chat.id,
            'Если вы хотите оплатить покупки - нажмите оплатить',
            reply_markup=sumbit_keyboard
        )
    else:
        bot.send_message(message.chat.id, 'Такой комманды я пока не знаю, напишите /start, чтобы начать')


@bot.callback_query_handler(func=lambda call: True)
def basket_add_handler(call):
    call_text = call.message.reply_markup.keyboard[0][0].text
    if call_text == 'Добавить в Корзину':
        bot.send_message(
            call.message.chat.id,
            'Напишите количество добавляемого товара',
            reply_markup=ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(call.message, basket_checker, call.data)
    elif call_text == 'Изменить Количество':
        data, flag = call.data.split('/')
        if flag == 'Изменить':
            bot.send_message(
                call.message.chat.id,
                'Напишите новое количество товара',
                reply_markup=ReplyKeyboardRemove()
            )
            bot.register_next_step_handler(call.message, change_product_count, data)
        elif flag == 'Удалить':
            remove_product(call.message, data)
        else:
            pass
    else:
        pass


def basket_checker(message, product_id):
    try:
        count = int(message.text)
        product = get_product_by_id(product_id)
        if count > product.count:
            raise AttributeError
        basket = get_basket_by_telegram(message.chat.id)
        add_product_too_basket(product, basket, count)
        bot.send_message(message.chat.id, 'Товар успешно добавлен в корзину')
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Некорректное число товара')
    bot_catalog(message, page=0)
    bot.register_next_step_handler(message, working_with_catalog, page=0)


bot.infinity_polling()
