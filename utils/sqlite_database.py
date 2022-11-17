import sqlite3 as sql
from create_bot import bot

def sql_start():
    global base, cur
    base = sql.connect('shop.db',)
    cur = base.cursor()
    if base:
        print('Database connected!')
    base.execute('CREATE TABLE IF NOT EXISTS products(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()

async def sql_insert_four(state, table):
    async with state.proxy() as data:
        cur.execute(f'INSERT INTO {table} VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read_table(message, table):
    for ret in cur.execute(f'SELECT * FROM {table}').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n{ret[2]}\nЦена: {ret[-1]} руб.')