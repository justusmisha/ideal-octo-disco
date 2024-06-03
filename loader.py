import psycopg2

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from data.config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(LoggingMiddleware())


async def cur(sql_query, additional_value=None):
    conn = psycopg2.connect(
        dbname="justusles_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    try:
        cur = conn.cursor()
        if additional_value:
            cur.execute(sql_query, (additional_value,))
        else:
            cur.execute(sql_query)
        rows = cur.fetchone()
        cur.fetchone()
        return rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



