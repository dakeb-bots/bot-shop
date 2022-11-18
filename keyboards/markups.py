from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btn_go_to_main_menu = InlineKeyboardButton('Главное меню', callback_data='main_menu')
btn_exit = InlineKeyboardButton(text='Выход', callback_data='exit')

# CLIENT | LEVEL 1
def main_menu():
    btn_products = InlineKeyboardButton(text='Товары 🛍', callback_data='products')
    btn_about = InlineKeyboardButton(text='Информация ℹ', callback_data='about', url='google.com')

    markup_menu = InlineKeyboardMarkup()
    markup_menu.add(btn_products)
    markup_menu.row(btn_about, btn_exit)

    return markup_menu

# ADMIN | LEVEL 1
def admin_menu():
    btn_add_product = InlineKeyboardButton(text='Добавить товар', callback_data='add_product')
    btn_show_product = InlineKeyboardButton(text='Показать товары', callback_data='show_products')
    upload_in_file = InlineKeyboardButton(text='Загрузить товары из файла', callback_data='upload_in_file')

    markup_admin = InlineKeyboardMarkup()
    markup_admin.row(btn_add_product, upload_in_file)
    markup_admin.add(btn_show_product)
    markup_admin.add(btn_exit)

    return markup_admin

def edit_menu(text = '', cb_data = ''):
    btn_delete = InlineKeyboardButton(text=f'Удалить', callback_data=f'delete_product {cb_data}')
    btn_edit = InlineKeyboardButton(text=f'Редактировать', callback_data=f'edit_product {cb_data}')

    markup_edit = InlineKeyboardMarkup()
    markup_edit.add(btn_edit, btn_delete)

    return markup_edit

def edit_question(text = '', cb_data = ''):
    btn_edit_photo = InlineKeyboardButton(text=f'Фото', callback_data=f'photo {cb_data}')
    btn_edit_name = InlineKeyboardButton(text=f'Название', callback_data=f'name {cb_data}')
    btn_edit_description = InlineKeyboardButton(text=f'Описание', callback_data=f'description {cb_data}')
    btn_edit_price = InlineKeyboardButton(text=f'Цену', callback_data=f'price {cb_data}')
    btn_edit_all = InlineKeyboardButton(text=f'Всё', callback_data=f'all {cb_data}')

    markup_edit_question = InlineKeyboardMarkup()
    markup_edit_question.add(btn_edit_photo, btn_edit_name, btn_edit_description, btn_edit_price, btn_edit_all, btn_exit)

    return markup_edit_question

def show_last_changes(cb_data = ''):
    btn_show_last = InlineKeyboardButton(text='Посмотреть', callback_data=f'last {cb_data}')
    markup_last = InlineKeyboardMarkup()
    markup_last.add(btn_show_last)

    return markup_last

# CLIENT LEVEL 1.
def buy(cb_data = ''):
    btn_buy = InlineKeyboardButton(text='Купить', callback_data=f'buy {cb_data}')
    markup_buy = InlineKeyboardMarkup()
    markup_buy.add(btn_buy)

    return markup_buy