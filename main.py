import telebot


token = '7851422609:AAGLGzpbLltyAgu0g_F_Orogf27AuBl6-8c'
bot = telebot.TeleBot(token)

admins_list = [6979004370]

categories = {
    "Вакансии": ["Курьер", "Фасовщик"],
    "Выплаты": ["Карта Альфабанка", "Карта Т банка"],
    "Промокоды": ["Мегамаркет", "Яндекс маркет"],
}

descriptions = {
    "Курьер": "Описание вакансии курьера...",
    "Фасовщик": "Описание вакансии фасовщика...",
    "Карта Альфабанка": "Описание + рефка",
    "Карта Т банка": "Описание + рефка",
    "Мегамаркет": "Описание + промокод",
    "Яндекс маркет": "Описание + промокод",
}

seen_users = []


def show_categories(call_or_message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for category in categories.keys():
        keyboard.add(telebot.types.InlineKeyboardButton(text=category, callback_data=f"category_{category}"))
    if isinstance(call_or_message, telebot.types.CallbackQuery):
        if call_or_message.from_user.id in admins_list:
            keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_admin_menu"))
        else:
            keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_user_menu"))
    if isinstance(call_or_message, telebot.types.CallbackQuery):
        bot.edit_message_text(
            chat_id=call_or_message.message.chat.id,
            message_id=call_or_message.message.message_id,
            text="Выбери категорию:",
            reply_markup=keyboard)
    else:
        bot.send_message(call_or_message.chat.id, "Выбери категорию:", reply_markup=keyboard)


def show_items(call, category):
    found_category = next((cat for cat in categories.keys() if cat.lower() == category.lower()), None)
    if found_category:
        items = categories[found_category]
        keyboard = telebot.types.InlineKeyboardMarkup()
        for item in items:
            keyboard.add(telebot.types.InlineKeyboardButton(text=item, callback_data=f"item_{item}"))
        keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_categories"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Выбери элемент из категории '{found_category}':",
            reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, "Категория не найдена.")


def show_description(call, item):
    if item in descriptions:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"back_to_items_{item}"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=descriptions[item],
            reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, "Описание не найдено.")


def show_admin_menu(chat_id, message_id=None):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(text="Посмотреть список категорий", callback_data="admin_categories"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Количество пользователей", callback_data="admin_users"))
    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Выберите действие:",
            reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)


def send_welcome_message(chat_id, is_admin=False):
    welcome_text = (
        "Добро пожаловать в нашего бота!\n\n"
        "Здесь вы можете найти полезную информацию о товарах и вакансиях.")
    if is_admin:
        welcome_text += "\n\nВы вошли как администратор."
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Начать", callback_data="start_menu"))
    with open("welcome.jpg", "rb") as photo:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=welcome_text,
            reply_markup=keyboard)


def show_user_menu(chat_id, message_id=None):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Выбор категории", callback_data="user_categories"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Помощь", callback_data="user_help"))
    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Выберите действие:",
            reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)


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
        show_categories(call)
    elif data.startswith("back_to_items_"):
        item = data.split("_")[-1]
        category = next((cat for cat, items in categories.items() if item in items), None)
        if category:
            show_items(call, category)
    elif data == "admin_categories":
        show_categories(call)
    elif data == "admin_users":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_admin_menu"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Количество пользователей: {len(seen_users)}",
            reply_markup=keyboard)
    elif data == "back_to_admin_menu":
        show_admin_menu(call.message.chat.id, call.message.message_id)
    elif data == "start_menu":
        if call.from_user.id in admins_list:
            show_admin_menu(call.message.chat.id)
        else:
            show_user_menu(call.message.chat.id)
    elif data == "user_categories":
        show_categories(call)
    elif data == "user_help":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_user_menu"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Если у вас остались вопросы, или вы столкнулись с техническими проблемами, напишите оператору техподдержки: @operatortag",
            reply_markup=keyboard)
    elif data == "back_to_user_menu":
        show_user_menu(call.message.chat.id, call.message.message_id)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in seen_users:
        seen_users.append(user_id)
    send_welcome_message(message.chat.id, is_admin=(user_id in admins_list))


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


if __name__ == '__main__':
    bot.polling(none_stop=True)