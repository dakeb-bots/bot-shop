from create_bot import bot, dp
from aiogram import Dispatcher, types
from keyboards import markups
from aiogram.types.input_file import InputFile
from utils import sqlalchemy_database
from states import admin_states
from aiogram.dispatcher import FSMContext

CURR_ID = None
async def welcome(message: types.Message):
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! 🤖\nЧтобы открыть меню /menu')

async def menu(message: types.Message):
    await bot.send_photo(message.chat.id, photo=InputFile('resources/images/menu.png'), reply_markup=markups.main_menu())

# Меню
@dp.callback_query_handler(lambda call: call.data)
async def event_buttons_client(call: types.CallbackQuery, state: FSMContext):
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
        await admin_states.FSM_Add_Product.photo.set()
        await bot.answer_callback_query(call.id)
    elif call.data == 'show_products':
        await sqlalchemy_database.write_products(call, True)
        await bot.answer_callback_query(call.id)

    # Удалить / изменить товар
    if call.data and call.data.startswith('delete_product '):
        await sqlalchemy_database.delete_by_id(call, call.data.replace('delete_product ', ''))
    elif call.data and call.data.startswith('edit_product '):
        name = sqlalchemy_database.get_name_product(call.data.replace("edit_product ", ""))
        # Передаем в функцию edit_question id кнопки которая была нажата, т.к. id одинаковый
        await bot.send_message(call.from_user.id, f'Товар: [{name}]\nЧто будем редактировать?', reply_markup=markups.edit_question(cb_data=call.data.replace("edit_product ", "")))
        await bot.answer_callback_query(call.id)

    # Поменять фото
    if call.data and call.data.startswith('photo '):
        async with state.proxy() as data:
            data['id_button'] = call.data.replace("photo ", "")
            print(f'[client.py] data["idbutton"] = {data["id_button"]}')
        await admin_states.FSM_Edit_photo.photo.set()
        await bot.send_message(call.from_user.id, 'Загрузите новое фото')
        await bot.answer_callback_query(call.id)
    # Поменять название
    elif call.data and call.data.startswith('name '):
        async with state.proxy() as data:
            data['id_button'] = call.data.replace("name ", "")
            print(f'[client.py] data["idbutton"] = {data["id_button"]}')
        await admin_states.FSM_Edit_name.name.set()
        await bot.send_message(call.from_user.id, 'Введите новое название')
        await bot.answer_callback_query(call.id)
    # Поменять описание
    elif call.data and call.data.startswith('description '):
        async with state.proxy() as data:
            data['id_button'] = call.data.replace("description ", "")
            print(f'[client.py] data["idbutton"] = {data["id_button"]}')
        await admin_states.FSM_Edit_description.description.set()
        await bot.send_message(call.from_user.id, 'Введите новое описание')
        await bot.answer_callback_query(call.id)
    # Поменять цену
    elif call.data and call.data.startswith('price '):
        async with state.proxy() as data:
            data['id_button'] = call.data.replace("price ", "")
            print(f'[client.py] data["idbutton"] = {data["id_button"]}')
        await admin_states.FSM_Edit_price.price.set()
        await bot.send_message(call.from_user.id, 'Введите новую цену')
        await bot.answer_callback_query(call.id)

    # Показать нажатую кнопку
    # print(call.data)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=['help', 'start'])
    dp.register_message_handler(menu, commands='menu')