from utils import sqlite_database
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btn_go_to_main_menu = InlineKeyboardButton('Главное меню', callback_data='main_menu')

# CLIENT | LEVEL 1
def main_menu():
    btn_products = InlineKeyboardButton(text='Товары 🛍', callback_data='products')
    btn_about = InlineKeyboardButton(text='Информация ℹ', callback_data='about')
    btn_exit = InlineKeyboardButton(text='Выход ❌', callback_data='exit')

    markup_menu = InlineKeyboardMarkup()
    markup_menu.add(btn_products)
    markup_menu.row(btn_about, btn_exit)

    return markup_menu

# ADMIN | LEVEL 1
def admin_menu():
    pass