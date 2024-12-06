import config
from aiogram import types
from intagrations.telegram import dp, bot
from models.user import UserStates
from services.user_service import (
    get_club_keyboard, send_welcome, handle_start, handle_name, handle_moderation_approval,
    show_main_menu, get_ready_status_keyboard, get_meeting_type_keyboard,
    handle_callback_query
)
from models.user import UserStates
from models.user_manager import UserManager

user_manager = UserManager()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    text, keyboard = await send_welcome(message.chat.id)
    await bot.send_message(message.chat.id, text, reply_markup=keyboard)

@dp.message_handler(lambda message: user_manager.get_user(message.chat.id).state == UserStates.INIT)
async def handle_start_message(message: types.Message):
    response = await handle_start(message.text, message.chat.id)
    await bot.send_message(message.chat.id, response)

@dp.message_handler(lambda message: user_manager.get_user(message.chat.id).state == UserStates.WAITING_NAME)
async def handle_name_message(message: types.Message):
    response = await handle_name(message.text, message.chat.id)
    await bot.send_message(message.chat.id, response)
    await bot.send_message(config.MODER, f"Новый запрос на регистрацию от пользователя с именем: {message.text}. Подтвердите или отклоните.")
    await bot.send_message(config.MODER_1, f"Новый запрос на регистрацию от пользователя с именем: {message.text}. Подтвердите или отклоните.")
    
@dp.message_handler(lambda message: user_manager.get_user(message.chat.id).state == UserStates.EMAIL_SENT)
async def handle_moderation_approval_message(message: types.Message):
    response, approved = await handle_moderation_approval(message.chat.id)
    await bot.send_message(message.chat.id, response)
    if approved:
        text, keyboard = await show_main_menu(message.chat.id)
        await bot.send_message(message.chat.id, text, reply_markup=keyboard)

@dp.message_handler(lambda message: user_manager.get_user(message.chat.id).state == UserStates.ONBOARDING)
async def handle_onboarding_message(message: types.Message):
    if message.text == "Готовность":
        user_manager.get_user(message.chat.id).state = UserStates.READY_STATUS
        await bot.send_message(message.chat.id, "Укажите свой статус:", reply_markup=get_ready_status_keyboard())
    elif message.text == "Клубы":
        user_manager.get_user(message.chat.id).state = UserStates.CLUBS
        await bot.send_message(message.chat.id, "Выберите нужный вам клуб:", reply_markup=get_club_keyboard())
    elif message.text == "Подобрать собеседника":
        user_manager.get_user(message.chat.id).state = UserStates.CREATE_MEETING
        await bot.send_message(message.chat.id, "Выберите тип встречи:", reply_markup=get_meeting_type_keyboard())

@dp.callback_query_handler(lambda call: True)
async def handle_callback(call: types.CallbackQuery):
    response = await handle_callback_query(call.data, call.message.chat.id)
    if isinstance(response, tuple):
        text, keyboard = response
        await bot.send_message(call.message.chat.id, text, reply_markup=keyboard)
    else:
        await bot.send_message(call.message.chat.id, response)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)