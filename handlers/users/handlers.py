from aiogram.types import ReplyKeyboardRemove
from filters import *
from loader import dp


HELP_COMMAND = """ 
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>начните работать с ботом</em>
<b>/description</b> - <em>описание бота</em>
"""


# GENERAL COMMANDS
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND,
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await message.answer(
        text=f"ЮстусЛес - это компания, специализирующаяся на пиломатериалах и срубах.🪵✨\n\nНаш бот поможет вам самостоятельно рассчитать стоимость сруба по вашим параметрам. Начните прямо сейчас, нажав /start!\n\n"
             f"🌟 Лидер компании, Станислав Юстус, имеет более 20 лет опыта в продаже древесины и строительстве срубов. 🌲🏠")
