from aiogram.types import CallbackQuery
from keyboards.users.buttons import *
from data.db_base import *
from loader import dp, bot
from states.fio_state import Form
from utils.data_calculator.srub_calculator import SrubCalculator
from handlers.users.start import *
from utils.functions import message_updt


@dp.callback_query_handler(lambda query: query.data == 'application_form', state='*')
async def add_roof_price_handler(callback_query: CallbackQuery):
    await Form.fio.set()
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text="Напишите свое ФИО")
