from create_bot import bot, dp
from aiogram import Dispatcher, types
from keyboards import markups
async def welcome(message: types.Message):
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! 🤖', reply_markup=markups.main_menu())

@dp.callback_query_handler(lambda call: True)
async def event_buttons(call: types.CallbackQuery):
    if call.data == 'products':
        await bot.send_message(call.from_user.id, 'Товары!')
    elif call.data == 'about':
        await bot.send_message(call.from_user.id, 'Информация!')
    elif call.data == 'exit':
        await bot.send_message(call.from_user.id, 'Выход!')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome)