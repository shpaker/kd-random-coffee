from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from random_coffee_fe.models.user_manager import UserManager
from random_coffee_be.config import MODER, MODER_1, URL
from random_coffee_fe.models.user import UserStates, User
from random_coffee_fe.intagrations.telegram import dp, bot
import httpx
import logging
import random
from random_coffee_be.services.club_groups import club_groups

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

user_manager = UserManager()

# Функция для отправки сообщения модераторам
# async def notify_moderators(message):
#    await bot.send_message(MODER, message)
#    await bot.send_message(MODER_1, message)

# Функция для отправки HTTP-запросов к бэкенду
async def backend_request(method, url, json=None):
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url)
            elif method == "POST":
                response = await client.post(url, json=json)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Backend request error: {e}")
            return None

# Функция для отправки приветственного сообщения
async def send_welcome(chat_id):
    user = user_manager.get_user(chat_id)
    user.state = UserStates.INIT
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("НАЧАТЬ"))
    return "Нажмите кнопку ниже, чтобы начать:", keyboard

# Функция для обработки команды /start
async def handle_start(message_text, chat_id):
    user = user_manager.get_user(chat_id)
    if user.state == UserStates.INIT and message_text == "НАЧАТЬ":
        user.state = UserStates.WAITING_NAME
        return "Привет! Добро пожаловать в Random Coffee V1 Students Edition! Отправьте ваше имя."
    else:
        return "Нажмите кнопку НАЧАТЬ, чтобы продолжить."

# Функция для обработки имени пользователя
async def handle_name(name, chat_id):
    user = user_manager.get_user(chat_id)
    user.name = name
    user.state = UserStates.EMAIL_SENT

    # Логируем ID пользователя
    logger.info(f"New user registered: ID={chat_id}, Name={name}")

    # Отправляем запрос на бэкенд для регистрации пользователя
    user_data = {
        "id": chat_id,
        "username": name,
        "email": f"{chat_id}@example.com",
        "status": "pending",
        "availability_interval": "9-18",
        "approved_at": None,
        "is_new": True,
        "created_at": "2023-10-01T12:00:00"
    }
    response = await backend_request("POST", f"{URL}/user", json=user_data)
    if response:
        return f"💌{name} Теперь твой запрос на регистрацию отправлен модератору.\nКак только он его одобрит, ты сможешь общаться."
    else:
        return "Напишите любое сообщение чтобы продолжения."

# Функция для обработки одобрения модератором
async def handle_moderation_approval(chat_id):
    user = user_manager.get_user(chat_id)
    approval_status = random.choice(["approved", "declined"])

    if approval_status == "approved":
        user.state = UserStates.ONBOARDING
        onboarding_messages = [
            "🏆Ура победа!\n🎉Модератор одобрил твою заявку🎉 \nДобро пожаловать в Random Coffee!🥺\nМы рады видеть тебя в нашем сообществе!\nДавай знакомиться!👋",
            "👌Отлично!\n🎉Модератор одобрил твою заявку🎉 \nРады видеть тебя в нашем сообществе Random Coffee!🥺\nДавай узнаем друг друга получше!👋",
            "😎Славно!\n🎉Модератор одобрил твою заявку🎉\nТы теперь часть Random Coffee!🥺\nДавай узнаем друг друга получше!👋"
        ]
        return random.choice(onboarding_messages), True
    else:
        return "🥹К сожалению, модератор ещё не одобрил вашу заявку, чуть чуть подождите и напишите ещё одно сообщение🥹", False

# Функция для отображения главного меню
async def show_main_menu(chat_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("✅ Готовность"))
    keyboard.add(KeyboardButton("🏠 Клубы"))
    keyboard.add(KeyboardButton("👨 Подобрать собеседника"))
    return "🧰 Выберите опцию:", keyboard

# Функция для получения клавиатуры готовности
def get_ready_status_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("✅ Готов к общению ✅", callback_data="ready"))
    keyboard.add(InlineKeyboardButton("❌ Не готов к общению ❌", callback_data="not_ready"))
    keyboard.add(InlineKeyboardButton("⬅️ Главное меню ⬅️", callback_data="main_menu"))
    return keyboard

# Функция для получения клавиатуры типов встреч
def get_meeting_type_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("💬 Tet-a-tet 💬", callback_data="Tet-a-tet"))
    keyboard.add(InlineKeyboardButton("🏠 Групповая 🏠", callback_data="group"))
    keyboard.add(InlineKeyboardButton("⬅️ Главное меню ⬅️", callback_data="main_menu"))
    return keyboard

# Функция для получения клавиатуры клубов
def get_club_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)  # Устанавливаем row_width=2 для добавления 2 кнопок в одну строку
    clubs = [
        ("⚔️ Dota 2 ⚔️", "Dota 2"),
        ("🔫 CS2 🔫", "CS2"),
        ("✨ Genshin Impact ✨", "Genshin Impact"),
        ("🚂 HonkaiStarRail 🚂", "HonkaiStarRail"),
        ("💬 Tet-a-tet 💬", "Tet-a-tet"),
        ("📺 ZZZ 📺", "ZZZ"),
        ("🗡 Valorant 🗡", "Valorant"),
        ("🤡 Mobile Legends 🤡", "Mobile Legends"),
        ("💿 ToF 💿", "ToF"),
        ("🌠 WutheringWaves 🌠", "WutheringWaves")
    ]
    buttons = [InlineKeyboardButton(emoji, callback_data=club) for emoji, club in clubs]
    keyboard.add(*buttons)  # Добавляем все кнопки в клавиатуру
    keyboard.add(InlineKeyboardButton("Главное меню", callback_data="main_menu"))
    return keyboard

# Функция для обработки callback-запросов
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
            invite_link = club_groups.get(call_data)
            if invite_link:
                # Создаем кнопку для перехода по ссылке
                keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("➕ Присоединиться", url=invite_link))
                return f"Вы присоединились к клубу: {call_data}", keyboard
            else:
                return f"Ссылка для присоединения к клубу {call_data} недоступна."
    elif call_data == "main_menu":
        user.state = UserStates.ONBOARDING
        return await show_main_menu(chat_id)
    elif call_data in ["Tet-a-tet", "group"]:
        user.state = UserStates.CREATE_MEETING
        return "Выберите клуб для встречи: \n (😢чтобы вернуться к использованию основных кнопок снизу, нажмите главное меню😢)", get_club_keyboard()

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user = user_manager.get_user(message.chat.id)
    user.state = UserStates.INIT
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("НАЧАТЬ"))
    await bot.send_message(message.chat.id, "Нажмите кнопку ниже, чтобы начать:", reply_markup=keyboard)

# Обработчик сообщений в состоянии INIT
@dp.message_handler(lambda message: user_manager.get_user(message.chat.id).state == UserStates.INIT)
async def handle_start_message(message: types.Message):
    if message.text == "НАЧАТЬ":
        user = user_manager.get_user(message.chat.id)
        user.state = UserStates.WAITING_NAME
        await bot.send_message(message.chat.id, "Привет! Добро пожаловать в Random Coffee V1 Students Edition! Отправьте ваше имя.")
        return
    else:
        await bot.send_message(message.chat.id, "Нажмите кнопку НАЧАТЬ, чтобы продолжить.")

# Обработчик сообщений в состоянии WAITING_NAME
@dp.message_handler(lambda message: user_manager.get_user(message.chat.id).state == UserStates.WAITING_NAME)
async def handle_name_message(message: types.Message):
    response = await handle_name(message.text, message.chat.id)
    await bot.send_message(message.chat.id, response)
#    await notify_moderators(f"Новый запрос на регистрацию от пользователя с именем: {message.text}. Подтвердите или отклоните.")

# Обработчик сообщений в состоянии EMAIL_SENT
@dp.message_handler(lambda message: user_manager.get_user(message.chat.id).state == UserStates.EMAIL_SENT)
async def handle_moderation_approval_message(message: types.Message):
    response, approved = await handle_moderation_approval(message.chat.id)
    await bot.send_message(message.chat.id, response)
    if approved:
        text, keyboard = await show_main_menu(message.chat.id)
        await bot.send_message(message.chat.id, text, reply_markup=keyboard)

# Обработчик сообщений в состоянии ONBOARDING
@dp.message_handler(lambda message: user_manager.get_user(message.chat.id).state == UserStates.ONBOARDING)
async def handle_onboarding_message(message: types.Message):
    if message.text == "✅ Готовность":
        user_manager.get_user(message.chat.id).state = UserStates.READY_STATUS
        await bot.send_message(message.chat.id, "Укажите свой статус: \n (😢чтобы вернуться к использованию основных кнопок снизу, нажмите главное меню😢)", reply_markup=get_ready_status_keyboard())
    elif message.text == "🏠 Клубы":
        user_manager.get_user(message.chat.id).state = UserStates.CLUBS
        await bot.send_message(message.chat.id, "Выберите нужный вам клуб: \n (😢чтобы вернуться к использованию основных кнопок снизу, нажмите главное меню😢)", reply_markup=get_club_keyboard())
    elif message.text == "👨 Подобрать собеседника":
        user_manager.get_user(message.chat.id).state = UserStates.CREATE_MEETING
        await bot.send_message(message.chat.id, "Выберите тип встречи: \n (😢чтобы вернуться к использованию основных кнопок снизу, нажмите главное меню😢)", reply_markup=get_meeting_type_keyboard())

# Обработчик callback-запросов
@dp.callback_query_handler(lambda call: True)
async def handle_callback(call: types.CallbackQuery):
    response = await handle_callback_query(call.data, call.message.chat.id)
    if isinstance(response, tuple):
        text, keyboard = response
        await bot.send_message(call.message.chat.id, text, reply_markup=keyboard)
    else:
        await bot.send_message(call.message.chat.id, response)


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

# Если есть какието вопросы пиши мне в лс, я и моя команда будут рады ответить на любой вопрос https://t.me/MeMnO228 либо https://t.me/kzrxxxt