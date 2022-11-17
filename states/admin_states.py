from aiogram.dispatcher.filters.state import State, StatesGroup

class FSM_Add_Product(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

class FSM_Edit_all(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
