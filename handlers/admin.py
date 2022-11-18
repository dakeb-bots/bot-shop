from create_bot import bot, dp
from aiogram import Dispatcher, types
from keyboards import markups
from aiogram.types.input_file import InputFile
from aiogram.dispatcher import FSMContext
from states import admin_states
from utils import sqlalchemy_database
from handlers.client import CURR_ID
async def admin_menu(message: types.Message):
    await bot.send_photo(message.chat.id, photo=InputFile('resources/images/admin_menu.png'), reply_markup=markups.admin_menu())

async def cancel_state(message: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await bot.send_message(message.chat.id, 'Отмена')

# Добавление товара #

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await admin_states.FSM_Add_Product.next()
    await bot.send_message(message.chat.id, 'Введите название товара')

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await admin_states.FSM_Add_Product.next()
    await bot.send_message(message.chat.id, 'Введите описание товара')

async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await admin_states.FSM_Add_Product.next()
    await bot.send_message(message.chat.id, 'Введите цену')

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    insertProducts = sqlalchemy_database.products.insert().values(img=data['photo'], name=data['name'], description=data['description'], price=data['price'])
    sqlalchemy_database.engine.execute(insertProducts)
    await bot.send_message(message.chat.id, f'Товар {data["name"]} добавлен!')
    await state.finish()
    await bot.send_photo(message.chat.id, photo=InputFile('resources/images/admin_menu.png'), reply_markup=markups.admin_menu())

# Изменение фото #
async def load_new_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_photo'] = message.photo[0].file_id
        button_id = data['id_button']
    q = sqlalchemy_database.products.update().where(sqlalchemy_database.products.c.id == button_id).values(img=data['new_photo'])
    sqlalchemy_database.engine.execute(q)
    await bot.send_message(message.chat.id, 'Фото обновлено!', reply_markup=markups.show_last_changes(cb_data=data['id_button']))
    await state.finish()

# Изменение названия #
async def load_new_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_name'] = message.text
        button_id = data['id_button']
    q = sqlalchemy_database.products.update().where(sqlalchemy_database.products.c.id == button_id).values(name=data['new_name'])
    sqlalchemy_database.engine.execute(q)
    await bot.send_message(message.chat.id, 'Имя обновлено!', reply_markup=markups.show_last_changes(cb_data=data['id_button']))
    await state.finish()

# Изменение описание #
async def load_new_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_description'] = message.text
        button_id = data['id_button']
    q = sqlalchemy_database.products.update().where(sqlalchemy_database.products.c.id == button_id).values(description=data['new_description'])
    sqlalchemy_database.engine.execute(q)
    await bot.send_message(message.chat.id, 'Описание обновлено!', reply_markup=markups.show_last_changes(cb_data=data['id_button']))
    await state.finish()

# Изменение цены #
async def load_new_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_price'] = message.text
        button_id = data['id_button']
    q = sqlalchemy_database.products.update().where(sqlalchemy_database.products.c.id == button_id).values(price=data['new_price'])
    sqlalchemy_database.engine.execute(q)
    await bot.send_message(message.chat.id, 'Цена обновлена!', reply_markup=markups.show_last_changes(cb_data=data['id_button']))
    await state.finish()

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_menu, commands='admin')
    dp.register_message_handler(cancel_state, state='*', commands=['cancel'])
    dp.register_message_handler(load_photo, content_types=['photo'], state=admin_states.FSM_Add_Product.photo)
    dp.register_message_handler(load_name, state=admin_states.FSM_Add_Product.name)
    dp.register_message_handler(load_description, state=admin_states.FSM_Add_Product.description)
    dp.register_message_handler(load_price, state=admin_states.FSM_Add_Product.price)

    dp.register_message_handler(load_new_photo, content_types=['photo'], state=admin_states.FSM_Edit_photo.photo)
    dp.register_message_handler(load_new_name, state=admin_states.FSM_Edit_name.name)
    dp.register_message_handler(load_new_description, state=admin_states.FSM_Edit_description.description)
    dp.register_message_handler(load_new_price, state=admin_states.FSM_Edit_price.price)
