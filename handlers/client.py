from create_bot import bot, dp
from aiogram import Dispatcher, types
from keyboards import markups
from aiogram.types.input_file import InputFile
from utils import sqlalchemy_database

from states.admin_states import FSM_Add_Product

async def welcome(message: types.Message):
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! 🤖\nЧтобы открыть меню /menu')

async def menu(message: types.Message):
    await bot.send_photo(message.chat.id, photo=InputFile('resources/images/menu.png'), reply_markup=markups.main_menu())

# Меню
@dp.callback_query_handler(lambda call: call.data)
async def event_buttons_client(call: types.CallbackQuery):
    # CLIENT MENU
    if call.data == 'products':
        await sqlalchemy_database.write_products(call)
    elif call.data == 'about':
        await bot.send_message(call.from_user.id, 'Магазин-бот')
        await bot.answer_callback_query(call.id)
    elif call.data == 'exit':
        await call.message.delete()
        await bot.answer_callback_query(call.id)
    # ADMIN MENU
    elif call.data == 'add_product':
        await call.message.delete()
        await bot.send_message(call.from_user.id, 'Кинь фото товара, чтобы отменить /cancel')
        await FSM_Add_Product.photo.set()
        await bot.answer_callback_query(call.id)
    elif call.data == 'show_products':
        await sqlalchemy_database.write_products(call, True)

    if call.data and call.data.startswith('delete_product '):
        await sqlalchemy_database.delete_by_id(call, call.data.replace('delete_product ', ''))
    elif call.data and call.data.startswith('edit_product '):
        print(call.data)
        print(call.data.replace('edit_product ', ''))
        name = sqlalchemy_database.get_name_product(call.data.replace("edit_product ", ""))
        await bot.send_message(call.from_user.id, f'Товар: [{name}]\nЧто будем редактировать?', reply_markup=markups.edit_question())

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=['help', 'start'])
    dp.register_message_handler(menu, commands='menu')