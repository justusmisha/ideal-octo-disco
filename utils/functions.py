import re

import asyncpg
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.db_base import *
from utils.data_calculator.srub_calculator import SrubCalculator


async def check_main_options(dictionary, main_options, kb: InlineKeyboardMarkup):
    for key in main_options:
        if key not in dictionary or (not dictionary[key] and dictionary[key] is not False):
            return False
    if not any(
            button.text == 'Дальше' for row in kb.inline_keyboard for button
            in row):
        kb.add(InlineKeyboardButton(text="Дальше", callback_data="count_srub_price"))


async def message_updt(user_id):
    srub_dict = await get_srub_dict(user_id)
    total_price = await get_final_srub_price(user_id)
    c = SrubCalculator(a=srub_dict['a'],
                       b=srub_dict['b'],
                       h=srub_dict['h'],
                       d=srub_dict['d'],
                       extra_wall=srub_dict['extra_wall'])
    srub_price = await c.srub_price()
    sborka_price = await c.final_sborka_price()
    message = f""" Сумма сруба с текущими параметрами составляет
{total_price} рублей
                Текущие параметры:
Стена A: {srub_dict['a']} метров
Стена B: {srub_dict['b']} метров
Высота сруба: {srub_dict['h']} метров
Средний диаметр бревен по малой вершине: {srub_dict['d']} сантиметров
Наличие 5 стены: {'Да' if srub_dict['extra_wall'] else 'Нет'}
Цена сруба: {srub_price}
Цена сборки: {sborka_price}, она влючена в стоимость"""
    return message


def is_valid_phone_number(phone_number: str) -> bool:
    return re.fullmatch(r'\d{10,15}', phone_number) is not None


def validator_for_opts(text: str) -> bool:
    try:
        number = float(text.replace(',', '.'))
        return 1 <= number <= 20
    except ValueError:
        return False


def validator_for_kms(text: str) -> bool:
    try:
        number = float(text.replace(',', '.'))
        return 1 <= number <= 100000
    except ValueError:
        return False
