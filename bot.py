import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import TLG_TOKEN

from utils import group_by_city


logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    format="%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.INFO,
)

bot = Bot(token=TLG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Тыкните команду /city")


@dp.message_handler(commands=["city"])
async def test(message: types.Message):
    await message.answer(group_by_city())


# long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
