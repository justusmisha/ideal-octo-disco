from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from data.db_base import get_final_srub_price, uptd_final_srub_price, get_srub_dict, add_roof_price
from keyboards.users.buttons import final_kb
from loader import dp, bot
from utils.data_calculator.roof_calculator import RoofCalculator


@dp.callback_query_handler(lambda query: query.data.startswith('add_roof_price'), state='*')
async def add_roof_price_handler(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    srub_price = await get_final_srub_price(user_id)
    srub_dict = await get_srub_dict(callback_query.from_user.id)
    roof = RoofCalculator(a=srub_dict['a'], b=srub_dict['b'])
    roof_price = await roof.roof_price()
    await add_roof_price(callback_query.from_user.id, roof_price)
    for row in final_kb.inline_keyboard:
        for button in row:
            if button.callback_data == 'add_roof_price':
                button.text = "Добавлена стоимость крыши ✅"
                setattr(button, 'callback_data', 'add_roof_price_modified')
                async with state.proxy() as data:
                    data['text_message'] += f"\nСтоимость крыши {roof_price}"
                await uptd_final_srub_price(user_id, roof_price + srub_price)
                await callback_query.message.edit_reply_markup(reply_markup=final_kb)

            elif button.callback_data == 'add_roof_price_modified':
                button.text = "Добавить стоимость крыши ✅"
                setattr(button, 'callback_data', 'add_roof_price')
                async with state.proxy() as data:
                    if 'text_message' in data:
                        data['text_message'] = data['text_message'].replace(f"\nСтоимость крыши {roof_price}", "")
                await uptd_final_srub_price(user_id, srub_price - roof_price)
                await callback_query.message.edit_reply_markup(reply_markup=final_kb)

    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Рассчитайте стоимость с учетом или без учета выбранных параметров",
                                reply_markup=final_kb)
