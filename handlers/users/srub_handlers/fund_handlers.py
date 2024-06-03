from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.db_base import get_srub_dict, add_fundament_price, get_final_srub_price, \
    uptd_final_srub_price, get_fund_price
from keyboards.users.buttons import final_kb, fundament_kb
from loader import dp, bot
from utils.data_calculator.srub_calculator import SrubCalculator


@dp.callback_query_handler(lambda query: query.data.startswith('option_fundament'), state='*')
async def fundament_choice_handler(callback_query: CallbackQuery, state: FSMContext):
    fundaments_names = ['Ленточного фундамента', "Забивных Свай", "Винтовых Свай"]
    option = callback_query.data
    if option == 'option_fundament_lent':
        fundament = 1
    elif option == 'option_fundament_zabiv':
        fundament = 2
    elif option == 'option_fundament_vint':
        fundament = 3
    elif option == 'option_fundament_back':
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Рассчитайте стоимость с учетом или без учета выбранных параметров",
                                    reply_markup=final_kb)
    srub_dict = await get_srub_dict(callback_query.from_user.id)
    c = SrubCalculator(a=srub_dict['a'],
                       b=srub_dict['b'],
                       h=srub_dict['h'],
                       d=srub_dict['d'],
                       extra_wall=srub_dict['extra_wall'],
                       fundament=fundament)
    fund_price = await c.fundament_price()
    user_id = callback_query.from_user.id
    await add_fundament_price(user_id, fund_price)
    srub_price = await get_final_srub_price(user_id)
    await uptd_final_srub_price(user_id, srub_price + fund_price)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=f"Стоимость {fundaments_names[fundament - 1]} составляет {int(fund_price)} рублей\n"
                                     f"Она была добавлена в итоговую стоимость",
                                reply_markup=fundament_kb)
    async with state.proxy() as data:
        data['text_message'] += f"\nСтоимость фундамента {int(fund_price)}"


@dp.callback_query_handler(lambda query: query.data.startswith('add_fund_price'), state='*')
async def add_fund_price_handler(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    fund_price = await get_fund_price(user_id)
    srub_price = await get_final_srub_price(user_id)
    for row in final_kb.inline_keyboard:
        for button in row:
            if button.callback_data == 'add_fund_price':
                await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            text="Выберите какой фундамент вам нужен:",
                                            reply_markup=fundament_kb)
                button.text = "Добавлена стоимость фундамента ✅"
                setattr(button, 'callback_data', 'add_fund_price_modified')

            elif button.callback_data == 'add_fund_price_modified':
                button.text = "Добавить стоимость фундамента"
                setattr(button, 'callback_data', 'add_fund_price')
                async with state.proxy() as data:
                    if 'text_message' in data:
                        data['text_message'] = data['text_message'].replace(f"\nСтоимость фундамента {fund_price}", "")
                await uptd_final_srub_price(user_id, srub_price - fund_price)
                await callback_query.message.edit_reply_markup(reply_markup=final_kb)
