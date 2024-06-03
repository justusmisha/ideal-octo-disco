from aiogram import types
from loader import dp


async def set_default_commands():
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Список всех команд"),
            types.BotCommand("description", "Описание бота"),
        ]
    )
