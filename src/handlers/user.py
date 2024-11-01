from aiogram import Router, F
from aiogram.types import Message

user_router = Router()


@user_router.message(F.text.casefold() == "привет")
async def hello(message: Message):
    await message.answer("Добро пожаловать!")
