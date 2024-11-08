from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.enums import Role
from src.models.models import User
from src.api.user import UserAPI


from src.keyboard import start_menu
from settings import dependency


commands_router= Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message):
   user_api = UserAPI("./storage/users.json")
   user_is_owner = await user_api.check_owner(message.from_user.id)
   
   user_role = Role.ADMIN
   if not user_is_owner:
      user_role = Role.USER

   user = User(id = message.from_user.id,
            username=message.from_user.username,
            role=user_role)   
   
   if not await user_api.exist(message.from_user.id):
      await user_api.register(user)
   
   await dependency.inject(user=user)

   await message.answer(f"Добро пожаловать {user.username} HRBot!", reply_markup=start_menu.as_markup(resize_keyboard=True))