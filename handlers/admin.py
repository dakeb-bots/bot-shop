from create_bot import bot, dp
from aiogram import Dispatcher, types
from keyboards import markups
from aiogram.types.input_file import InputFile
from aiogram.dispatcher import FSMContext
from states.admin_states import FSM_Add_Product
from utils import sqlalchemy_database

async def admin_menu(message: types.Message):
    await bot.send_photo(message.chat.id, photo=InputFile('resources/images/admin_menu.png'), reply_markup=markups.admin_menu())
async def cancel_state(message: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await bot.send_message(message.chat.id, 'Отмена')
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSM_Add_Product.next()
    await bot.send_message(message.chat.id, 'Введите название товара')

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSM_Add_Product.next()
    await bot.send_message(message.chat.id, 'Введите описание товара')

async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSM_Add_Product.next()
    await bot.send_message(message.chat.id, 'Введите цену')

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    insertProducts = sqlalchemy_database.products.insert().values(img=data['photo'], name=data['name'], description=data['description'], price=data['price'])
    sqlalchemy_database.engine.execute(insertProducts)
    await bot.send_message(message.chat.id, f'Товар {data["name"]} добавлен!')
    await state.finish()
    await bot.send_photo(message.chat.id, photo=InputFile('resources/images/admin_menu.png'), reply_markup=markups.admin_menu())
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_menu, commands='admin')
    dp.register_message_handler(cancel_state, state='*', commands=['cancel'])
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSM_Add_Product.photo)
    dp.register_message_handler(load_name, state=FSM_Add_Product.name)
    dp.register_message_handler(load_description, state=FSM_Add_Product.description)
    dp.register_message_handler(load_price, state=FSM_Add_Product.price)
