from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter


employee_router = Router()
async def hello(message: Message):
    await message.answer("Добро пожаловать!")