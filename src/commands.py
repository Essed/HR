from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.models.models import User
from src.api.user import UserAPI
from src.enums import Role


from src.keyboard import start_menu

commands_router= Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message):

   user = User(id = message.from_user.id,
               username=message.from_user.username,
               role=Role.ADMIN)
   
   userapi = UserAPI("./storage/users.json")
   print(await userapi.exist(user.id))
   
   await userapi.register(user)
   

   await message.answer(f"Добро пожаловать {user.username} HRBot!", reply_markup=start_menu.as_markup(resize_keyboard=True))