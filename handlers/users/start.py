from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.db_base import add_user_db, get_srub_dict
from handlers.users.srub_handlers.srub_keyboard_handlers import main_options
from keyboards.users.buttons import *
from loader import dp
from states.base_state import StateEnum
from utils.functions import check_main_options, message_updt


@dp.message_handler(Command('start'), state="*")
async def start(message: types.Message, state: FSMContext):
    try:
        srub_dict = await get_srub_dict(message.from_user.id)
        if srub_dict:
            await check_main_options(srub_dict, main_options, srub_keyboard)
        user_id = message.from_user.id
        username = message.from_user.username
        tg_chat_id = message.chat.id

        if not message.from_user.is_bot:
            await add_user_db(user_id, username, tg_chat_id)

        await message.answer("""
👋 Добро пожаловать в Telegram-бот компании "Юстус Лес"! 📊
Рассчитывайте стоимость сруба в удобном мессенджере
""", reply_markup=kb_first_message)

    except Exception as e:
        print(f"An error occurred while handling /start command: {e}")
