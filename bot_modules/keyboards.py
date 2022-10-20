from telebot import types


main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = types.InlineKeyboardButton("Каталог")
button_2 = types.InlineKeyboardButton("Корзина")
main_keyboard.row(button_1)
main_keyboard.row(button_2)


catalog_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = types.InlineKeyboardButton("Предыдущие")
button_2 = types.InlineKeyboardButton("Следующие")
button_3 = types.InlineKeyboardButton("Назад")
catalog_keyboard.row(button_1, button_2)
catalog_keyboard.row(button_3)

sumbit_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = types.InlineKeyboardButton("Оплатить")
button_2 = types.InlineKeyboardButton("Назад")
sumbit_keyboard.row(button_1)
sumbit_keyboard.row(button_2)
