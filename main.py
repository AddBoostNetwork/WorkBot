import telebot
from telebot.types import InputMediaPhoto

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


# Главное меню (категории)
def show_categories(call_or_message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for category in categories.keys():
        keyboard.add(telebot.types.InlineKeyboardButton(text=category, callback_data=f"category_{category}"))

    # Добавляем кнопку "Назад" для админов
    if isinstance(call_or_message, telebot.types.CallbackQuery) and call_or_message.from_user.id in admins_list:
        keyboard.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data="back_to_admin_menu"))

    if isinstance(call_or_message, telebot.types.CallbackQuery):
        bot.edit_message_text(
            chat_id=call_or_message.message.chat.id,
            message_id=call_or_message.message.message_id,
            text="Выбери категорию:",
            reply_markup=keyboard
        )
    else:
        bot.send_message(call_or_message.chat.id, "Выбери категорию:", reply_markup=keyboard)


# Меню элементов категории
def show_items(call, category):
    if category.lower() in categories:
        items = categories[category.lower()]
        keyboard = telebot.types.InlineKeyboardMarkup()
        for item in items:
            keyboard.add(telebot.types.InlineKeyboardButton(text=item, callback_data=f"item_{item}"))
        # Добавляем кнопку "Назад"
        keyboard.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data="back_to_categories"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Выбери элемент из категории '{category}':",
            reply_markup=keyboard
        )
    else:
        bot.send_message(call.message.chat.id, "Категория не найдена.")


# Показ описания элемента
def show_description(call, item):
    if item in descriptions:
        keyboard = telebot.types.InlineKeyboardMarkup()
        # Добавляем кнопку "Назад"
        keyboard.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data=f"back_to_items_{item}"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=descriptions[item],
            reply_markup=keyboard
        )
    else:
        bot.send_message(call.message.chat.id, "Описание не найдено.")


# Главное меню админа
def show_admin_menu(call_or_message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(text="Посмотреть список категорий", callback_data="admin_categories"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Количество пользователей", callback_data="admin_users"))

    if isinstance(call_or_message, telebot.types.CallbackQuery):
        bot.edit_message_text(
            chat_id=call_or_message.message.chat.id,
            message_id=call_or_message.message.message_id,
            text="Выберите действие:",
            reply_markup=keyboard
        )
    else:
        bot.send_message(call_or_message.chat.id, "Выберите действие:", reply_markup=keyboard)


# Приветственное сообщение с фото и кнопкой "Начать"
def send_welcome_message(chat_id, is_admin=False):
    # Текст приветствия
    welcome_text = (
        "Добро пожаловать в нашего бота!\n\n"
        "Здесь вы можете найти полезную информацию о товарах и вакансиях."
    )

    # Если пользователь — админ, добавляем сообщение об этом
    if is_admin:
        welcome_text += "\n\nВы вошли как администратор."

    # Кнопка "Начать"
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Начать", callback_data="start_menu"))

    # Отправка фото с текстом и кнопкой
    with open("welcome.jpg", "rb") as photo:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=welcome_text,
            reply_markup=keyboard
        )


# Обработка callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    data = call.data

    if data.startswith("category_"):
        category = data.split("_")[1]
        show_items(call, category)
    elif data.startswith("item_"):
        item = data.split("_")[1]
        show_description(call, item)
    elif data == "back_to_categories":
        # Возврат к категориям
        show_categories(call)
    elif data.startswith("back_to_items_"):
        # Возврат к элементам категории
        item = data.split("_")[-1]
        category = next((cat for cat, items in categories.items() if item in items), None)
        if category:
            show_items(call, category)
    elif data == "admin_categories":
        # Обработка кнопки "Посмотреть список категорий" для админов
        show_categories(call)
    elif data == "admin_users":
        # Обработка кнопки "Количество пользователей" для админов
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data="back_to_admin_menu"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Количество пользователей: {len(seen_users)}",
            reply_markup=keyboard
        )
    elif data == "back_to_admin_menu":
        # Возврат к главному меню админа
        show_admin_menu(call)
    elif data == "start_menu":
        # Обработка кнопки "Начать"
        if call.from_user.id in admins_list:
            # Отправляем текстовое сообщение с меню админа
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Выберите действие:",
                reply_markup=telebot.types.InlineKeyboardMarkup().add(
                    telebot.types.InlineKeyboardButton(text="Посмотреть список категорий",
                                                       callback_data="admin_categories"),
                    telebot.types.InlineKeyboardButton(text="Количество пользователей", callback_data="admin_users")
                )
            )
        else:
            show_categories(call)


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id not in seen_users:
        seen_users.append(user_id)

    # Отправляем приветственное сообщение с фото и кнопкой "Начать"
    send_welcome_message(message.chat.id, is_admin=(user_id in admins_list))


# Обработка сообщений
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
            bot.send_message(message.chat.id, "Неизвестная команда.")
    else:
        bot.send_message(message.chat.id, "Используйте кнопки для выбора.")


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)