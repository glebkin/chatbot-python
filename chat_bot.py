import apiai
import json
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater(token='760593078:AAE3MJQ7_a2svpFRqOkwjfVOKmwQHhfRqOc')  # Токен API к Telegram

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# Обработка команд
def start_command(bot, update):
    print('start command')
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def text_message(bot, update):
    print('some message')

    request = apiai.ApiAI('e8ccc8d307564ac5a37ca7de38e09964').text_request()  # Токен API к Dialogflow
    request.lang = 'ru'  # На каком языке будет послан запрос
    request.session_id = 'GLKOAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')


# Хендлеры
start_command_handler = CommandHandler('/start', start_command)
text_message_handler = MessageHandler(Filters.text, text_message)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling()
# Останавливаем бота, если были нажаты Ctrl + C

updater.idle()
