import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы увидеть список всех доступных валют, введите команду: /values\n\
Чтобы начать работу, введите команду для бота следующего содержания через пробел:\n\
- <имя валюты, которую хотите поменять>\n\
- <имя валюты, в которую хотите перевести>\n\
- <количество переводимой валюты>\n\
Например:\n\
- юань лира 100"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Список доступных валют:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(" ")

        if len(values) != 3:
            raise APIException("Неверное количество параметров. Введите три параметра через пробел")

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка ввода!\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная команда.\n{e}. Получить информацию можно введя команду /start или /help")
    else:
        text = f'Цена {amount} {quote} в {base} составляет {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
