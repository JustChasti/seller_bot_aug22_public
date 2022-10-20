import telebot


base_user_local = 'postgres'
base_user_server = 'padmin'
base_password = '6@cSo75q'
base_hostname = 'localhost'
base_port = 5432
maintenance = 'pgseller'

admin_username = 'admin'
admin_email = 'chastytim@mail.ru'
admin_password = '6@cSo75q'

bot_token = ''

bot = telebot.TeleBot(bot_token)

catalog_chunk = 3
