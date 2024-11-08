from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from src.keyboard import start_menu_admin, cancel_menu

from src.models.models import Company, User
from src.api.company import CompanyAPI
from src.api.user import UserAPI
from src.enums import Role


from settings import dependency

company_router = Router()

class CompanyForm(StatesGroup):
    name = State()


@company_router.message(StateFilter(CompanyForm), F.text.casefold() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действия отменены", reply_markup=start_menu_admin.as_markup(resize_keyboard=True))


@company_router.message(F.text.casefold() == "создать организацию")
async def create(message: Message, state: FSMContext):
    userapi: UserAPI = UserAPI("./storage/users.json")
    if await userapi.check_owner(message.from_user.id):
        await message.answer("Компания уже создана!", reply_markup=start_menu_admin.as_markup(resize_keyboard=True))
        return

    await message.answer("Введите название компании", reply_markup=cancel_menu.as_markup(resize_keyboard=True))
    await state.set_state(CompanyForm.name)


@company_router.message(CompanyForm.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    company_data = await state.get_data()
    company = company_data["name"]

    company = Company(name=company, owner_id=message.from_user.id)
    
    company_api = CompanyAPI("./storage/companies.json")

    if not await company_api.exist(company.name):
        userapi: UserAPI = UserAPI("./storage/users.json")
        user: User = dependency.key_value_parameters["user"]
        
        updated_user = User(id=user.id, username=user.username, role=Role.ADMIN, balance=user.balance)             
        await userapi.update(user.id, updated_user)
        await company_api.create(company)

    await state.clear()
    await message.answer(f"Компания {company.name} успешно добавлена!", reply_markup=start_menu_admin.as_markup(resize_keyboard=True))

