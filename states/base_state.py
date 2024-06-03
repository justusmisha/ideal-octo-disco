from aiogram.dispatcher.filters.state import StatesGroup, State


class StateEnum(StatesGroup):
    waiting_for_registration = State()
    waiting_for_a_wall = State()
    waiting_for_b_wall = State()
    waiting_for_height = State()
    waiting_for_diameter = State()
    waiting_for_extra_wall = State()
    waiting_for_dostavka = State()
    state_message = State()
