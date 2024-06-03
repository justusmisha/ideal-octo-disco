from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
import psycopg2
from data.config import ADMIN_ID
from loader import cur


class AdminUser(BoundFilter):
    async def check(self, message: types.Message):
        user_id = message.from_user.id
        try:
            cur.execute("SELECT * FROM users WHERE tg_chat_id=%s", (user_id,))
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    if row[1] == ADMIN_ID:
                        return True
            return False
        except psycopg2.Error as e:
            print("Error fetching user from database:", e)
