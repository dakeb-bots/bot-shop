from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, CheckConstraint, select
from create_bot import bot
import sqlite3 as sql
from datetime import datetime
from keyboards import markups

metadata = MetaData()
engine = create_engine('sqlite:///shop.db')

# Connect to table
products = Table('products', metadata, autoload_with=engine)

# Create table
# products = Table('products', metadata,
#                 Column('id', Integer, primary_key=True),
#                 Column('img', String(255), nullable=False),
#                 Column('name', String(255), nullable=False),
#                 Column('description', String(255), nullable=False),
#                 Column('price', String(255), nullable=False),
# )

async def write_products(message, id=False):
    q = select(products)
    if id:
        result = engine.execute(q)
        for row in result.fetchall():
            await bot.send_photo(message.from_user.id, photo=row['img'], caption=f'ID=[{row["id"]}] *{row["name"]}*\n{row["description"]}\nЦена: {row["price"]} руб.', parse_mode="Markdown", reply_markup=markups.edit_menu(text=f' {row["name"]}', cb_data=f'{row["id"]}'))
    else:
        result = engine.execute(q)
        for row in result.fetchall():
            await bot.send_photo(message.from_user.id, photo=row['img'], caption=f'*{row["name"]}*\n{row["description"]}\nЦена: {row["price"]} руб.', parse_mode="Markdown")

async def write_by_id(message, id):
    q = select(products).where(products.c.id == id)
    result = engine.execute(q)
    await bot.send_photo(message.from_user.id, photo=result['img'],caption=f'*{result["name"]}*\n{result["description"]}\nЦена: {result["price"]} руб.',parse_mode="Markdown")

def get_name_product(id):
    q = products.select().where(products.c.id == id)
    result = engine.execute(q).fetchall()
    return result[0]['name']
async def delete_by_id(message, id):
    q = products.delete().where(products.c.id == id)
    engine.execute(q)
    await bot.send_message(message.from_user.id, 'Товар удален')

def sqlalchimey_start():
    metadata.create_all(engine)
    print('Database connected!')
