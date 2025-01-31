import telebot

token = '7851422609:AAGLGzpbLltyAgu0g_F_Orogf27AuBl6-8c'
bot = telebot.TeleBot(token)

admins_list = [6979004370]

categories = {
    "вакансии": ["курьер", "менеджер"],
    "товары": ["ноутбук", "телефон"],
}

descriptions = {
    "курьер": "Описание вакансии курьера...",
    "менеджер": "Описание вакансии менеджера...",
    "ноутбук": "Описание товара ноутбук...",
    "телефон": "Описание товара телефон...",
}

seen_users = []

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id not in seen_users:
        seen_users.append(user_id)

    if user_id in admins_list:
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add("Посмотреть список категорий", "Количество пользователей")
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Привет! Выбери категорию:")
        show_categories(message)

def show_categories(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for category in categories.keys():
        keyboard.add(telebot.types.KeyboardButton(category))
    bot.send_message(message.chat.id, "Выбери категорию:", reply_markup=keyboard)

def show_items(message):
    category = message.text
    if category in categories:
        items = categories[category]
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for item in items:
            keyboard.add(telebot.types.KeyboardButton(item))
        bot.send_message(message.chat.id, f"Выбери элемент из категории '{category}':", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Категория не найдена.")

def show_description(message):
    item = message.text
    if item in descriptions:
        bot.send_message(message.chat.id, descriptions[item])
    else:
        bot.send_message(message.chat.id, "Описание не найдено.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    if user_id in admins_list:
        if text == "Посмотреть список категорий":
            show_categories(message)
        elif text == "Количество пользователей":
            bot.send_message(message.chat.id, f"Количество пользователей: {len(seen_users)}")
    else:
        if text in categories:
            show_items(message)
        elif text in descriptions:
            show_description(message)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда.")

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)