from create_bot import dp
from aiogram import executor

from handlers import client
from handlers import admin

from utils import sqlite_database

client.register_handlers_client(dp)

async def on_startup(_):
    print('Bot is online!')
    sqlite_database.sql_start()

if __name__ == '__main__':
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )