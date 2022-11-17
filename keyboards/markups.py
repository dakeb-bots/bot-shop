from utils import sqlite_database
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btn_go_to_main_menu = InlineKeyboardButton('Главное меню', callback_data='main_menu')
btn_exit = InlineKeyboardButton(text='Выход ❌', callback_data='exit')

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

    markup_admin = InlineKeyboardMarkup()
    markup_admin.row(btn_add_product)
    markup_admin.add(btn_show_product)
    markup_admin.add(btn_exit)

    return markup_admin

def edit_menu(text = '', cb_data = ''):
    btn_delete = InlineKeyboardButton(text=f'Удалить', callback_data=f'delete_product {cb_data}')
    btn_edit = InlineKeyboardButton(text=f'Редактировать', callback_data=f'edit_product {cb_data}')

    markup_edit = InlineKeyboardMarkup()
    markup_edit.add(btn_edit, btn_delete)

    return markup_edit
