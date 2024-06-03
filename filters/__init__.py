from aiogram import Dispatcher
from filters.users import *


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AuthenticatedUser)
    dp.filters_factory.bind(NotAuthenticatedUser)
    dp.filters_factory.bind(AdminUser)

