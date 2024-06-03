from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from data.db_base import get_final_srub_price, uptd_final_srub_price, get_dost_price
from keyboards.users.buttons import final_kb
from loader import dp, bot


@dp.callback_query_handler(lambda query: query.data == 'add_dost_price', state='*')
async def add_roof_price_handler(callback_query: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                text="Введите количество километров до Нижнего Новгорода",
                                message_id=callback_query.message.message_id,
                                reply_markup=InlineKeyboardMarkup().add(
                                    InlineKeyboardButton(text="Назад", callback_data='final_srub_price_back')))
    async with state.proxy() as data:
        data['dost_price'] = ""


@dp.callback_query_handler(lambda query: query.data == 'del_dost_price', state='*')
async def del_roof_price_handler(callback_query: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback_query.message.chat.id, text=f"Стоимость доставки удалена")
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Рассчитайте стоимость с учетом или без учета выбранных параметров",
                                reply_markup=final_kb)
    user_id = callback_query.from_user.id
    dost_price = await get_dost_price(user_id)
    srub_price = await get_final_srub_price(user_id)
    await uptd_final_srub_price(user_id, srub_price - dost_price)
    async with state.proxy() as data:
        del data['dost_price']
