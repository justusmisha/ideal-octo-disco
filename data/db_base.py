import json
import asyncpg


async def create_connection():
    return await asyncpg.connect(user="postgres",
                                 password="postgres",
                                 database="justusles_db",
                                 host="localhost",
                                 port="5432")


async def get_value_by_user_id_and_key(user_tg_id, key):
    conn = await create_connection()
    try:
        fetch_query = "SELECT srub_dict FROM users WHERE tg_id = $1;"
        srub_dict_json = await conn.fetchval(fetch_query, user_tg_id)

        if srub_dict_json is None:
            return None

        srub_dict = json.loads(srub_dict_json)

        value = srub_dict.get(key, None)

        return value

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return None
    finally:
        await conn.close()


async def add_user_db(user_tg_id, username, tg_chat_id):
    conn = await asyncpg.connect(user="postgres",
                                 password="postgres",
                                 database="justusles_db",
                                 host="localhost",
                                 port="5432")

    try:
        existing_user_query = "SELECT COUNT(*) FROM users WHERE tg_id = $1;"
        existing_user_count = await conn.fetchval(existing_user_query, user_tg_id)

        if existing_user_count == 0:
            sql_query = "INSERT INTO users (tg_id, username, tg_chat_id) VALUES ($1, $2, $3);"
            await conn.execute(sql_query, user_tg_id, username, tg_chat_id)
            return True
        else:
            return False

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def add_key_value_to_dict(user_tg_id, key, value):
    conn = await asyncpg.connect(user="postgres",
                                 password="postgres",
                                 database="justusles_db",
                                 host="localhost",
                                 port="5432")

    try:
        fetch_query = "SELECT srub_dict FROM users WHERE tg_id = $1;"
        srub_dict_json = await conn.fetchval(fetch_query, user_tg_id)

        if srub_dict_json is None:
            srub_dict = {}
        else:
            srub_dict = json.loads(srub_dict_json)

        srub_dict[key] = value

        updated_sruc_dict_json = json.dumps(srub_dict)

        update_query = "UPDATE users SET srub_dict = $1::jsonb WHERE tg_id = $2;"
        await conn.execute(update_query, updated_sruc_dict_json, user_tg_id)

        return True

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def get_srub_dict(user_tg_id):
    connection = await create_connection()

    try:
        fetch_query = "SELECT srub_dict FROM users WHERE tg_id = $1;"
        srub_dict_json = await connection.fetchval(fetch_query, user_tg_id)

        if srub_dict_json is None:
            return None

        srub_dict = json.loads(srub_dict_json)

        return srub_dict

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return None
    finally:
        await connection.close()


async def add_roof_price(user_tg_id, price):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")

        sql_query = "UPDATE users SET roof_price = $1 WHERE tg_id = $2"
        await conn.execute(sql_query, price, user_tg_id)
        return True

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def get_roof_price(user_tg_id):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")

        fetch_query = "SELECT roof_price FROM users WHERE tg_id = $1;"
        roof_price = await conn.fetchval(fetch_query, user_tg_id)
        return roof_price

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def add_fundament_price(user_tg_id, price):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")

        sql_query = "UPDATE users SET fundament_price = $1 WHERE tg_id = $2"
        await conn.execute(sql_query, price, user_tg_id)
        return True

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def get_fund_price(user_tg_id):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")

        fetch_query = "SELECT fundament_price FROM users WHERE tg_id = $1;"
        fundament_price = await conn.fetchval(fetch_query, user_tg_id)
        return fundament_price

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def add_dost_price(user_tg_id, price):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")

        sql_query = "UPDATE users SET dostavka_price = $1 WHERE tg_id = $2"
        await conn.execute(sql_query, price, user_tg_id)
        return True

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def get_dost_price(user_tg_id):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")

        fetch_query = "SELECT dostavka_price FROM users WHERE tg_id = $1;"
        fundament_price = await conn.fetchval(fetch_query, user_tg_id)
        return fundament_price

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def uptd_final_srub_price(user_tg_id, price):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")

        sql_query = "UPDATE users SET final_srub_price = $1 WHERE tg_id = $2"
        await conn.execute(sql_query, price, user_tg_id)
        return True

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def get_final_srub_price(user_tg_id):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")

        fetch_query = "SELECT final_srub_price FROM users WHERE tg_id = $1;"
        srub_price = await conn.fetchval(fetch_query, user_tg_id)
        return srub_price

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def get_user_id_by_tg(user_tg_id):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")

        sql_query = "SELECT id FROM users WHERE tg_id = $1;"
        user_id = await conn.fetchval(sql_query, user_tg_id)
        return user_id

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def add_fio_db(user_tg_id, fio):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")

        existing_user_query = "SELECT COUNT(*) FROM app_forms WHERE user_id = $1;"
        user_id = await get_user_id_by_tg(user_tg_id)
        existing_user_count = await conn.fetchval(existing_user_query, user_id)
        if existing_user_count == 0:
            sql_query = "INSERT INTO app_forms (fio, user_id) VALUES ($1, $2);"
            await conn.execute(sql_query, fio, user_id)
            return True
        else:
            return False

    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()


async def add_phone_number_db(user_tg_id, phone_number: int):
    try:
        conn = await asyncpg.connect(user="postgres",
                                     password="postgres",
                                     database="justusles_db",
                                     host="localhost",
                                     port="5432")
        user_id = await get_user_id_by_tg(user_tg_id)
        sql_query = "UPDATE app_forms SET phone_number = $1 WHERE user_id = $2"
        await conn.execute(sql_query, phone_number, user_id)
    except asyncpg.exceptions.PostgresError as error:
        print(error)
        return False
    finally:
        await conn.close()
