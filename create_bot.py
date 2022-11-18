from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN
import asyncio

storage = MemoryStorage()
loop = asyncio.get_event_loop()

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, storage=storage, loop=loop)
