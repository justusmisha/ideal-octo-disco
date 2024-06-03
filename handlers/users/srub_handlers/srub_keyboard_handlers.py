from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from data.db_base import get_srub_dict, add_key_value_to_dict
from keyboards.users.buttons import srub_keyboard, diameter_kb, true_false_kb
from loader import dp, bot
from states.base_state import StateEnum
from utils.functions import check_main_options


main_options = ['a', 'b', 'h', 'd', 'extra_wall']
dictionary = {'a': 'Стена А',
              'b': 'Стена B',
              'h': 'Высота сруба',
              'd': 'Диаметр Бревен',
              'extra_wall': '5 стена'
              }


@dp.callback_query_handler(lambda query: query.data == 'option_srub')
async def first_command(callback_query: CallbackQuery):
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Чтобы расчитать стоимость сруба нужно ввести следующие параметры:",
            reply_markup=srub_keyboard
        )

    except Exception as e:
        print(f"An error occurred while handling callback query: {e}")


@dp.callback_query_handler(lambda query: query.data.startswith('srub_option_wall_a'))
async def process_option_wall_a(callback_query: CallbackQuery):
    option = callback_query.data
    if option == 'srub_option_wall_a':
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Отправьте длинну первой стены в метрах\nЗатем нажмите 'Дальше'",
                                    reply_markup=InlineKeyboardMarkup().add(
                                        InlineKeyboardButton(text='Дальше', callback_data="srub_option_wall_a_back")))
        await StateEnum.waiting_for_a_wall.set()
    elif option == 'srub_option_wall_a_back':
        srub_dict = await get_srub_dict(callback_query.from_user.id)
        await check_main_options(srub_dict, main_options, srub_keyboard)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Чтобы расчитать стоимость сруба нужно ввести следующие параметры:",
                                    reply_markup=srub_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('srub_option_wall_b'))
async def process_option_wall_b(callback_query: CallbackQuery):
    option = callback_query.data
    if option == 'srub_option_wall_b':
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Отправьте длинну второй стены в метрах\nЗатем нажмите 'Дальше'",
                                    reply_markup=InlineKeyboardMarkup().add(
                                        InlineKeyboardButton(text='Дальше', callback_data="srub_option_wall_b_back")))
        await StateEnum.waiting_for_b_wall.set()
    elif option == 'srub_option_wall_b_back':
        srub_dict = await get_srub_dict(callback_query.from_user.id)
        await check_main_options(srub_dict, main_options, srub_keyboard)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Чтобы расчитать стоимость сруба нужно ввести следующие параметры:",
                                    reply_markup=srub_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('srub_option_height'))
async def process_option_height(callback_query: CallbackQuery):
    option = callback_query.data
    if option == 'srub_option_height':
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Отправьте высоту сруба в метрах\nЗатем нажмите 'Дальше'",
                                    reply_markup=InlineKeyboardMarkup().add(
                                        InlineKeyboardButton(text='Дальше', callback_data="srub_option_height_back")))
        await StateEnum.waiting_for_height.set()
    elif option == 'srub_option_height_back':
        srub_dict = await get_srub_dict(callback_query.from_user.id)
        await check_main_options(srub_dict, main_options, srub_keyboard)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Чтобы расчитать стоимость сруба нужно ввести следующие параметры:",
                                    reply_markup=srub_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith('srub_option_diameter'))
async def process_option_diameter(callback_query: CallbackQuery):
    option = callback_query.data
    if option == 'srub_option_diameter':
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Выберете диаметр бревен",
                                    reply_markup=diameter_kb)

    elif option == 'srub_option_diameter_20' or option == 'srub_option_diameter_22':
        diameter = int(option.split('_')[-1])
        await add_key_value_to_dict(callback_query.from_user.id, 'd', diameter)
        srub_dict = await get_srub_dict(callback_query.from_user.id)
        await check_main_options(srub_dict, main_options, srub_keyboard)
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text=f"Диаметр бревен   {srub_dict['d']} cм")
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Чтобы расчитать стоимость сруба нужно ввести следующие параметры:",
                                    reply_markup=srub_keyboard)

        @dp.callback_query_handler(lambda query: query.data.startswith('srub_option_extra_wall'))
        async def process_option_extra_wall(callback_query: CallbackQuery):
            option = callback_query.data
            if option == 'srub_option_extra_wall':

                await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            text="Вам нужна 5 стена?\n5 стена всегда равна по длине самой малой стене",
                                            reply_markup=true_false_kb)

            elif option == 'srub_option_extra_wall_True' or option == 'srub_option_extra_wall_False':
                answer = True if option.split('_')[-1] == 'True' else False
                await add_key_value_to_dict(callback_query.from_user.id, 'extra_wall', answer)
                srub_dict = await get_srub_dict(callback_query.from_user.id)
                await bot.send_message(chat_id=callback_query.message.chat.id,
                                       text=f"5 стена: {'Да' if srub_dict['extra_wall'] else 'Нет'}")
                await check_main_options(srub_dict, main_options, srub_keyboard)
                await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            text="Чтобы расчитать стоимость сруба нужно ввести следующие параметры:",
                                            reply_markup=srub_keyboard)
