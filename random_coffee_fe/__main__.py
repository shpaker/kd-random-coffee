from aiogram import executor
from random_coffee_fe.intagrations.telegram import dp

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)