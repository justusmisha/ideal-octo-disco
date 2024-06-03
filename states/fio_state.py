from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    fio = State()
    phone_number = State()
    fio_edit = State()
