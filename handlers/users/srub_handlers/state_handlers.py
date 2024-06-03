from aiogram.types import Message
from data.db_base import *
from loader import dp, bot
from states.fio_state import Form
from utils.data_calculator.srub_calculator import SrubCalculator
from handlers.users.start import *
from utils.functions import is_valid_phone_number, validator_for_opts, validator_for_kms


@dp.message_handler(lambda message: validator_for_opts(message.text),state='*')
async def process_response(message: types.Message, state: FSMContext):
    user_float = float(message.text.replace(',', '.'))
    current_state = await state.get_state()

    if current_state == 'StateEnum:waiting_for_a_wall':
        await add_key_value_to_dict(message.from_user.id, 'a', user_float)
        srub_dict = await get_srub_dict(message.from_user.id)
        await state.finish()
        await bot.send_message(chat_id=message.chat.id, text=f"Длинна стены A {srub_dict['a']} м")

    elif current_state == 'StateEnum:waiting_for_b_wall':
        await add_key_value_to_dict(message.from_user.id, 'b', user_float)
        srub_dict = await get_srub_dict(message.from_user.id)
        await state.finish()
        await bot.send_message(chat_id=message.chat.id, text=f"Длинна стены B {srub_dict['b']} м")

    elif current_state == 'StateEnum:waiting_for_height':
        await add_key_value_to_dict(message.from_user.id, 'h', user_float)
        srub_dict = await get_srub_dict(message.from_user.id)
        await state.finish()
        await bot.send_message(chat_id=message.chat.id, text=f"Высота сруба {srub_dict['h']} м")

    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(lambda message: validator_for_kms(message.text), state='*')
async def process_dost(message: types.Message, state: FSMContext):
    user_float = int(message.text)
    async with state.proxy() as data:
        if 'dost_price' in data:
            srub_dict = await get_srub_dict(message.from_user.id)
            c = SrubCalculator(a=srub_dict['a'],
                               b=srub_dict['b'],
                               h=srub_dict['h'],
                               d=srub_dict['d'],
                               extra_wall=srub_dict['extra_wall'],
                               dostavka=int(user_float))
            dostavka_price = await c.dostavka_price()
            data['dost_price'] += f'\nДоставка сруба {dostavka_price}'
            srub_price = await get_final_srub_price(message.from_user.id)
            await add_dost_price(message.from_user.id, dostavka_price)
            await uptd_final_srub_price(message.from_user.id, srub_price + dostavka_price)
            await bot.send_message(chat_id=message.chat.id,
                                   text=f"Стоимость доставки {dostavka_price}\nОна добавлена в стоимость")

    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(state=Form.fio)
async def process_fio(message: Message, state: FSMContext):
    if await add_fio_db(message.from_user.id, message.text):
        await add_fio_db(message.from_user.id, message.text)
        await message.reply("Спасибо! Вы написали свое ФИО: " + message.text)
        await bot.send_message(chat_id=message.chat.id,
                               text="Предоставьте телефон для отслеживания заявки")
        await Form.phone_number.set()
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text="Уже существет заявка\nПродолжайте заполнение чтобы изменить ее")
        await Form.fio_edit.set()


@dp.message_handler(state=Form.fio_edit)
async def process_fio_edit(message: Message, state: FSMContext):
    await add_fio_db(message.from_user.id, message.text)
    await message.reply("Спасибо! Вы написали свое ФИО: " + message.text)
    await bot.send_message(chat_id=message.chat.id,
                           text="Предоставьте телефон для завершения заявки")
    await Form.phone_number.set()


@dp.message_handler(lambda message: is_valid_phone_number(message.text), state=Form.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    phone_number = int(message.text)
    await add_phone_number_db(message.from_user.id, phone_number)
    await message.reply("Заявка сохранена!\nСпасибо что выбираете нас!")
    await state.finish()
