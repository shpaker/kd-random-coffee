from models.user_manager import UserManager
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import MODER, MODER_1
import random
from models.user import UserStates, User

user_manager = UserManager()

async def send_welcome(chat_id):
    user = user_manager.get_user(chat_id)
    user.state = UserStates.INIT
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("НАЧАТЬ"))
    return "Нажмите кнопку ниже, чтобы начать:", keyboard

async def handle_start(message_text, chat_id):
    user = user_manager.get_user(chat_id)
    if user.state == UserStates.INIT and message_text == "НАЧАТЬ":
        user.state = UserStates.WAITING_NAME
        return "Привет! Добро пожаловать в Random Coffee V1 Students Edition! Отправьте ваше имя."
    else:
        return "Нажмите кнопку НАЧАТЬ, чтобы продолжить."
   
async def handle_name(name, chat_id):
    user = user_manager.get_user(chat_id)
    user.name = name
    user.state = UserStates.EMAIL_SENT
    return f"💌{name} Теперь твой запрос на регистрацию отправлен модератору.\nКак только он его одобрит, ты получишь уведомление."

async def handle_moderation_approval(chat_id):
    user = user_manager.get_user(chat_id)
    approval_status = random.choice(["approved", "declined"])

    if approval_status == "approved":
        user.state = UserStates.ONBOARDING
        onboarding_messages = [
            "Добро пожаловать в Random Coffee! 🎉\nМы рады видеть тебя в нашем сообществе!\nДавай знакомиться!",
            "Отлично! 🎉\nРады видеть тебя в нашем сообществе Random Coffee!\nДавай узнаем друг друга получше!",
            "Ура! 🎉\nТы теперь часть Random Coffee!\nДавай узнаем друг друга получше!"
        ]
        return random.choice(onboarding_messages), True
    else:
        return "К сожалению, модератор отклонил вашу заявку. Пожалуйста, попробуйте еще раз позже.", False

async def show_main_menu(chat_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Готовность"))
    keyboard.add(KeyboardButton("Клубы"))
    keyboard.add(KeyboardButton("Подобрать собеседника"))
    return "Выберите опцию:", keyboard

def get_ready_status_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Готов к общению", callback_data="ready"))
    keyboard.add(InlineKeyboardButton("Не готов к общению", callback_data="not_ready"))
    keyboard.add(InlineKeyboardButton("Главное меню", callback_data="main_menu"))
    return keyboard

def get_meeting_type_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Tet-a-tet", callback_data="tet_a_tet"))
    keyboard.add(InlineKeyboardButton("Групповая", callback_data="group"))
    keyboard.add(InlineKeyboardButton("Главное меню", callback_data="main_menu"))
    return keyboard

def get_club_keyboard():
    keyboard = InlineKeyboardMarkup()
    clubs = ["Dota 2", "CS2", "Genshin Impact", "HonkaiStarRail", "Tet-a-tet", "ZZZ", "Valorant", "Mobile Legends", "ToF", "WutheringWaves"]
    for club in clubs:
        keyboard.add(InlineKeyboardButton(club, callback_data=club))
    keyboard.add(InlineKeyboardButton("Главное меню", callback_data="main_menu"))
    return keyboard

async def handle_callback_query(call_data, chat_id):
    user = user_manager.get_user(chat_id)
    if call_data in ["ready", "not_ready"]:
        user.ready_status = call_data == "ready"
        return "Ваш статус обновлен: " + ("Готов к общению" if call_data == "ready" else "Не готов к общению")
    elif call_data in ["Dota 2", "CS2", "Genshin Impact", "HonkaiStarRail", "Tet-a-tet", "ZZZ", "Valorant", "Mobile Legends", "ToF", "WutheringWaves"]:
        if call_data in user.clubs:
            user.clubs.remove(call_data)
            return f"Вы вышли из клуба: {call_data}"
        else:
            user.clubs.append(call_data)
            return f"Вы присоединились к клубу: {call_data}"
    elif call_data == "main_menu":
        user.state = UserStates.ONBOARDING
        return await show_main_menu(chat_id)
    elif call_data in ["tet_a_tet", "group"]:
        user.state = UserStates.CREATE_MEETING
        return "Выберите клуб для встречи:", get_club_keyboard()