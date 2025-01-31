from datetime import datetime
import telebot
from pyexpat.errors import messages

token = '7851422609:AAGLGzpbLltyAgu0g_F_Orogf27AuBl6-8c'
bot = telebot.TeleBot(token)
creator_id = 6979004370

admins_list = [
    6979004370,
]


def send_msg(id, message):
    try:
        bot.send_message(id, message, parse_mode='Markdown')
    except Exception as e:
        print(f"Произошла ошибка при отправке сообщения: {e}")



@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id in admins_list:
        print('Админ')
        message = "Привет, админ. Доступ открыт"
        send_msg(chat_id, message)
    else:
        print("Пользователь")
        message = "Привет, пользователь"
        send_msg(chat_id, message)


def main():
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Программа запущена")
    message = "Программа запущена"
    send_msg(creator_id, message)


main()
bot.infinity_polling()