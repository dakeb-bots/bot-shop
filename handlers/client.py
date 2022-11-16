from create_bot import bot
from aiogram import Dispatcher, types

async def welcome(message: types.Message):
    await bot.send_message(message.chat.id, message.text)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome)