from aiogram.types import CallbackQuery
from keyboards.users.buttons import *
from data.db_base import *
from loader import dp, bot
from utils.data_calculator.srub_calculator import SrubCalculator
from handlers.users.start import *
from utils.functions import message_updt


@dp.callback_query_handler(lambda query: query.data == 'final_srub_price', state='*')
async def add_roof_price_handler(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    message = await message_updt(user_id)
    async with state.proxy() as data:
        message += data['text_message'] if 'text_message' in data else ''
        if 'dost_price' in data:
            message += data['dost_price']
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=message,
                                        reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                            InlineKeyboardButton(text="Добавлена стоимость доставки ✅",
                                                                 callback_data='del_dost_price'),
                                            InlineKeyboardButton(text="Оставить заявку",
                                                                 callback_data='application_form'),
                                            InlineKeyboardButton(text="Назад", callback_data='final_srub_price_back'),
                                            ))
        else:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=message,
                                        reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                            InlineKeyboardButton(text="Добавить стоимость доставки",
                                                                 callback_data='add_dost_price'),
                                            InlineKeyboardButton(text="Оставить заявку",
                                                                 callback_data='application_form'),
                                            InlineKeyboardButton(text="Назад", callback_data='final_srub_price_back'),
                                            ))


@dp.callback_query_handler(lambda query: query.data == 'final_srub_price_back', state='*')
async def add_roof_price_handler(callback_query: CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Рассчитайте стоимость с учетом или без учета выбранных параметров",
                                reply_markup=final_kb)


@dp.callback_query_handler(lambda query: query.data == 'final_price_wo_mod' or query.data == 'count_srub_price', state='*')
async def all_add_false_handler(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['text_message'] = ''
    srub_dict = await get_srub_dict(callback_query.from_user.id)
    c = SrubCalculator(a=srub_dict['a'],
                       b=srub_dict['b'],
                       h=srub_dict['h'],
                       d=srub_dict['d'],
                       extra_wall=srub_dict['extra_wall'])
    srub_price = await c.srub_price()
    sborka_price = await c.final_sborka_price()
    if callback_query.data == "final_price_wo_mod":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=f"Сумма сруба с текущими параметрами составляет"
                                    f"\n{srub_price} рублей"
                                    f"\n                Текущие параметры:"
                                    f"\nСтена A: {srub_dict['a']} метров"
                                    f"\nСтена B: {srub_dict['b']} метров"
                                    f"\nВысота сруба: {srub_dict['h']} метров"
                                    f"\nСредний диаметр бревен по малой вершине: {srub_dict['d']} сантиметров"
                                    f"\nНаличие 5 стены: {'Да' if srub_dict['extra_wall'] else 'Нет'}"
                                    f"\nЦена сборки: {sborka_price}, она влючена в стоимость",
                                    reply_markup=InlineKeyboardMarkup().add(
                                        InlineKeyboardButton(text="Оставить заявку",
                                                             callback_data='application_form'),
                                        InlineKeyboardButton(text="Назад", callback_data='final_srub_price_back'),
                                        )
                                    )
    elif callback_query.data == "count_srub_price":
        await uptd_final_srub_price(callback_query.from_user.id, srub_price)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Рассчитайте стоимость с учетом или без учета выбранных параметров",
                                    reply_markup=final_kb)


@dp.callback_query_handler(lambda query: query.data == 'add_back', state='*')
async def add_roof_price_handler(callback_query: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Чтобы расчитать стоимость сруба нужно ввести следующие параметры:",
        reply_markup=srub_keyboard
    )
