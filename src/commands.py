from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.models.models import User
from src.keyboard import start_menu

from src.utils.json_utils import add_data_to_json, read_data_from_json_as_list


commands_router= Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message):

   user = User(id = message.from_user.id,
               username=message.from_user.username)
   
   users = await read_data_from_json_as_list("./storage/users.json")

   user_model = user.model_dump()

   if user_model not in users:
      await add_data_to_json(user_model, "./storage/users.json")

   await message.answer(f"Добро пожаловать{user.username} HRB0ot!", reply_markup=start_menu.as_markup(resize_keyboard=True))