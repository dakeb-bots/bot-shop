from create_bot import dp
from aiogram import executor

from handlers import client
from handlers import admin

import logging
logging.basicConfig(level=logging.INFO)

from utils import sqlite_database
from utils import sqlalchemy_database

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)

async def on_startup(_):
    print('Bot is online!')
    sqlalchemy_database.sqlalchimey_start()

if __name__ == '__main__':
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )