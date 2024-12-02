import telebot
import config
from telebot import types
import random

bot = telebot.TeleBot(config.TOKEN)

# Состояния пользователя
STATE_INIT = 0
STATE_WAITING_NAME = 1
STATE_EMAIL_SENT = 2
STATE_WAITING_MODERATION = 3
STATE_ONBOARDING = 4
STATE_READY_STATUS = 5
STATE_CLUBS = 6
STATE_CREATE_MEETING = 7
MODER = "1990006956"
MODER_1 = "1583920568"

# Для хранения состояний пользователей
user_states = {}

# Для хранения имени пользователей
user_name = {}

# Для хранения выбранных клубов пользователей
user_clubs = {}

# Для хранения статуса готовности пользователей
user_ready_status = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.chat.id] = STATE_INIT

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton("НАЧАТЬ")
    keyboard.add(button_start)

    bot.send_message(message.chat.id, "Нажмите кнопку ниже, чтобы начать:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == STATE_INIT)
def handle_start(message):
    if message.text == "НАЧАТЬ":
        user_states[message.chat.id] = STATE_WAITING_NAME
        bot.send_message(message.chat.id, "Привет! 👋\nДобро пожаловать в Random Coffee V1 Students Edition!\nЧтобы начать, пожалуйста, зарегистрируйся, отправив нам своё имя.")
    else:
        bot.send_message(message.chat.id, "Нажмите кнопку НАЧАТЬ, чтобы продолжить.")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == STATE_WAITING_NAME)
def handle_name(message):
    name = message.text
    user_name[message.chat.id] = name
    user_states[message.chat.id] = STATE_EMAIL_SENT

    # Отправка запроса модератору
    bot.send_message(MODER, f"Новый запрос на регистрацию от пользователя с именем: {name}. Подтвердите или отклоните.")

    bot.send_message(MODER_1, f"Новый запрос на регистрацию от пользователя с именем: {name}. Подтвердите или отклоните.")

    bot.send_message(message.chat.id, f"💌{name} Теперь твой запрос на регистрацию отправлен модератору.\nКак только он его одобрит, ты получишь уведомление.")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == STATE_EMAIL_SENT)
def handle_moderation_approval(message):
    # Тут короче будет рофл виде сообщения модеру, но пока это в разработке 
    approval_status = random.choice(["approved", "declined"])  # РАНДОМ статуса модерации

    if approval_status == "approved":
        user_states[message.chat.id] = STATE_ONBOARDING
        onboarding_messages = [
            "Добро пожаловать в Random Coffee! 🎉\nМы рады видеть тебя в нашем сообществе!\nДавай знакомиться!",
            "Отлично! 🎉\nРады видеть тебя в нашем сообществе Random Coffee!\nДавай узнаем друг друга получше!",
            "Ура! 🎉\nТы теперь часть Random Coffee!\nДавай узнаем друг друга получше!"
        ]
        bot.send_message(message.chat.id, random.choice(onboarding_messages))
        show_main_menu(message.chat.id)
    else:
        bot.send_message(message.chat.id, "К сожалению, модератор отклонил вашу заявку. Пожалуйста, попробуйте еще раз позже.")

def show_main_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_ready = types.KeyboardButton("Готовность")
    button_clubs = types.KeyboardButton("Клубы")
    button_create_meeting = types.KeyboardButton("Подобрать собеседника")
    keyboard.add(button_ready)
    keyboard.add(button_clubs)
    keyboard.add(button_create_meeting)
    bot.send_message(chat_id, "Выберите опцию:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == STATE_ONBOARDING)
def handle_onboarding(message):
    if message.text == "Готовность":
        user_states[message.chat.id] = STATE_READY_STATUS
        bot.send_message(message.chat.id, "Укажите свой статус:", reply_markup=get_ready_status_keyboard())
    elif message.text == "Клубы":
        user_states[message.chat.id] = STATE_CLUBS
        send_club_options(message.chat.id)
    elif message.text == "Подобрать собеседника":
        user_states[message.chat.id] = STATE_CREATE_MEETING
        bot.send_message(message.chat.id, "Выберите тип встречи:", reply_markup=get_meeting_type_keyboard())

def get_ready_status_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button_ready = types.InlineKeyboardButton("Готов к общению", callback_data="ready")
    button_not_ready = types.InlineKeyboardButton("Не готов к общению", callback_data="not_ready")
    button_main_menu = types.InlineKeyboardButton("Главное меню", callback_data="main_menu")
        
    keyboard.add(button_ready)
    keyboard.add(button_not_ready)
    keyboard.add(button_main_menu)
    
    return keyboard

def get_meeting_type_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button_tet_a_tet = types.InlineKeyboardButton("Tet-a-tet", callback_data="tet_a_tet")
    button_group = types.InlineKeyboardButton("Групповая", callback_data="group")
    button_main_menu = types.InlineKeyboardButton("Главное меню", callback_data="main_menu")
        
    keyboard.add(button_tet_a_tet)
    keyboard.add(button_group)
    keyboard.add(button_main_menu)
    
    return keyboard

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == STATE_READY_STATUS)
def handle_ready_status(message):
    pass

def send_club_options(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    clubs = ["Dota 2", "CS2", "Genshin Impact", "HonkaiStarRail", "Tet-a-tet", "ZZZ", "Valorant", "Mobile Legends", "ToF", "WutheringWaves"]
    
    for club in clubs:
        keyboard.add(types.InlineKeyboardButton(club, callback_data=club))
    
    keyboard.add(types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))
    
    bot.send_message(chat_id, "Выберите нужный вам клуб:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id
    if call.data in ["ready", "not_ready"]:
        status_message = "Ваш статус обновлен: " + ("Готов к общению" if call.data == "ready" else "Не готов к общению")
        bot.send_message(chat_id, status_message)
        
    elif call.data in ["Dota 2", "CS2", "Genshin Impact", "HonkaiStarRail", "Tet-a-tet", "ZZZ", "Valorant", "Mobile Legends", "ToF", "WutheringWaves"]:
        if chat_id not in user_clubs:
            user_clubs[chat_id] = []
        if call.data in user_clubs[chat_id]:
            user_clubs[chat_id].remove(call.data)
            bot.send_message(chat_id, f"Вы вышли из клуба: {call.data}")
        else:
            user_clubs[chat_id].append(call.data)
            bot.send_message(chat_id, f"Вы присоединились к клубу: {call.data}")
        
    elif call.data == "main_menu":
        user_states[chat_id] = STATE_ONBOARDING 
        show_main_menu(chat_id)

    elif call.data in ["tet_a_tet", "group"]:
        user_states[chat_id] = STATE_CREATE_MEETING
        bot.send_message(chat_id, "Выберите клуб для встречи:", reply_markup=get_club_keyboard())

def get_club_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    clubs = ["Dota 2", "CS2", "Genshin Impact", "HonkaiStarRail", "Tet-a-tet", "ZZZ", "Valorant", "Mobile Legends", "ToF", "WutheringWaves"]
    
    for club in clubs:
        keyboard.add(types.InlineKeyboardButton(club, callback_data=club))
    
    keyboard.add(types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))
    
    return keyboard

# Запускаем бота
bot.polling()