import sqlite3 as sql
from create_bot import bot

def sql_start():
    global base, cur
    base = sql.connect('shop.db',)
    cur = base.cursor()
    if base:
        print('Database connected!')
    # base.execute('CREATE TABLE IF NOT EXISTS item()')
    base.commit()

async def sql_query(query):
    try:
        cur.execute(query)
    except Exception as ex:
        print(ex)
    base.commit()