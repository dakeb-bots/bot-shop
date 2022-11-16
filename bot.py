from create_bot import dp
from aiogram import executor

from handlers import client
from handlers import admin

client.register_handlers_client(dp)

async def on_startup(_):
    print('Bot is online!')

if __name__ == '__main__':
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )