import config
from create_bot import bot, dp
from aiogram import Dispatcher, types
from keyboards import markups
from aiogram.types.input_file import InputFile
from utils import sqlalchemy_database
from states import admin_states
from aiogram.dispatcher import FSMContext

async def welcome(message: types.Message):
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! 🤖\nЧтобы открыть меню /menu')
    if sqlalchemy_database.check_user(message.from_user.id) != True: sqlalchemy_database.write_user(message.from_user.id)
    print(f'{message.from_user.id} started bot')

async def menu(message: types.Message):
    await bot.send_photo(message.chat.id, photo=InputFile('resources/images/menu.png'), reply_markup=markups.main_menu())

# Выводим сообщение при успешной оплаты
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    await bot.send_message(message.chat.id, 'Операция прошла успешно, спасибо что выбрали нас!')

# Обрабатываем платеж
@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_check_out_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_check_out_query.id, ok=True)

# Меню
@dp.callback_query_handler(lambda call: call.data)
async def event_buttons_client(call: types.CallbackQuery, state: FSMContext):
    # CLIENT MENU
    if call.data == 'products':
        await sqlalchemy_database.write_products(call)
        await bot.answer_callback_query(call.id)
    elif call.data == 'about':
        await bot.send_message(call.from_user.id, 'Магазин-бот')
        await bot.answer_callback_query(call.id)
    elif call.data == 'exit':
        await call.message.delete()
        await bot.answer_callback_query(call.id)
    elif call.data and call.data.startswith('buy '):   # Обработка кнопки купить
        q = sqlalchemy_database.select(sqlalchemy_database.products).where(sqlalchemy_database.products.c.id == call.data.replace('buy ', ''))
        result = sqlalchemy_database.engine.execute(q).fetchall()
        PRICES = types.LabeledPrice(label=result[0]['name'], amount=int(result[0]['price'])*100)
        if config.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(call.from_user.id, '*Тестовый платеж*')
            await bot.send_invoice(
                call.from_user.id,
                title=result[0]['name'],
                description='Оплата товара',
                provider_token=config.PAYMENTS_TOKEN,
                currency='rub',
                is_flexible=False,
                prices=[PRICES],
                start_parameter='time-machine-example',
                payload='some-invoice-payload-for-our-internal-use'
            )
            # await bot.send_message(call.from_user.id, int(result[0]['price'])*100)
        await bot.answer_callback_query(call.id)
    # ADMIN MENU
    elif call.data and call.data == 'add_product':
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
        await admin_states.FSM_Edit_photo.photo.set()
        await bot.send_message(call.from_user.id, 'Загрузите новое фото')
        await bot.answer_callback_query(call.id)
    # Поменять название
    elif call.data and call.data.startswith('name '):
        async with state.proxy() as data:
            data['id_button'] = call.data.replace("name ", "")
        await admin_states.FSM_Edit_name.name.set()
        await bot.send_message(call.from_user.id, 'Введите новое название')
        await bot.answer_callback_query(call.id)
    # Поменять описание
    elif call.data and call.data.startswith('description '):
        async with state.proxy() as data:
            data['id_button'] = call.data.replace("description ", "")
        await admin_states.FSM_Edit_description.description.set()
        await bot.send_message(call.from_user.id, 'Введите новое описание')
        await bot.answer_callback_query(call.id)
    # Поменять цену
    elif call.data and call.data.startswith('price '):
        async with state.proxy() as data:
            data['id_button'] = call.data.replace("price ", "")
        await admin_states.FSM_Edit_price.price.set()
        await bot.send_message(call.from_user.id, 'Введите новую цену')
        await bot.answer_callback_query(call.id)

    # Показать последнее цену
    if call.data and call.data.startswith('last '):
        await sqlalchemy_database.write_by_id(message=call, id=call.data.replace("last ", ""))
        await bot.answer_callback_query(call.id)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=['help', 'start'])
    dp.register_message_handler(menu, commands='menu')