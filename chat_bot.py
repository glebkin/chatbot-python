import apiai
import json
import logging
import subprocess
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googletrans import Translator

updater = Updater(token='760593078:AAE3MJQ7_a2svpFRqOkwjfVOKmwQHhfRqOc')  # Токен API к Telegram

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def text_message(bot, update):
    if update.message.sticker is not None:
        bot.send_sticker(chat_id=update.message.chat_id, sticker=update.message.sticker)
    else:
        if update.message.text.startswith('@GLKOAIBot') or update.effective_chat.type == 'private':
            request = apiai.ApiAI('e8ccc8d307564ac5a37ca7de38e09964').text_request()
            request.lang = 'ru'
            request.session_id = 'GLKOAIBot'
            request.query = update.message.text.replace('@GLKOAIBot', '')
            response_json = json.loads(request.getresponse().read().decode('utf-8'))
            response = response_json['result']['fulfillment']['speech']

            if response:
                bot.send_message(chat_id=update.message.chat_id, text=response)
            else:
                bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем поняла!')


def photo_message(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Дайте подумать...')

    img = update.message.photo[-1]
    f_id = img.file_id + '.png'
    file = bot.get_file(img)
    file.download(custom_path=f_id)
    out = subprocess.check_output('python classify_image.py --image_file ' + f_id).decode('utf-8')

    best_score = out.split('\n', 1)[0]

    translator = Translator()

    result_msg = 'С наибольшей долей вероятности это: \n' + translator.translate(best_score, dest='ru').text
    bot.send_message(chat_id=update.message.chat_id, text=result_msg)

    os.remove(f_id)


dispatcher.add_handler(CommandHandler('start', start_command))
dispatcher.add_handler(MessageHandler(Filters.text, text_message))
dispatcher.add_handler(MessageHandler(Filters.photo, photo_message))

updater.start_polling()
updater.idle()
