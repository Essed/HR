from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from src.models.models import Guild, User, Company
from src.api.guild import GuildAPI
from src.api.company import CompanyAPI
from src.keyboard import start_menu_admin

from settings import dependency

guild_router = Router()

class MemberForm(StatesGroup):
    username = State()


@guild_router.message(StateFilter(MemberForm), F.text.casefold() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действия отменены", reply_markup=start_menu_admin.as_markup(resize_keyboard=True))


@guild_router.message(F.text.casefold() == "создать гильдию")
async def create(message: Message):
    user: User = dependency.key_value_parameters["user"]
   
    company_api = CompanyAPI("./storage/companies.json")
    company: Company = await company_api.handle_company(user.id)
    
    if company is None:
        await message.answer("Сначала необходимо создать организацию")
        return

    guild = Guild(company_name=company.name)
    
    guild_api = GuildAPI("./storage/guilds.json")
    
    if await guild_api.exist(guild.company_name):
        await message.answer("Гильдия уже была создана")
        return 
    
    await guild_api.create(guild)

    await message.answer("Гильдия создана!")


@guild_router.message(F.text.casefold() == "добавить сотрудника")
async def add_member(message: Message, state: FSMContext):
    guild_api = GuildAPI("./storage/guilds.json")
    company_api = CompanyAPI("./storage/companies.json")
    
    user: User = dependency.key_value_parameters["user"]
    company: Company = await company_api.handle_company(user.id)

    if not await guild_api.exist(company.name):
        await message.answer("Сначала необходимо создать гильдию")
        return

    await message.answer("Введите имя пользователя в телеграме")
    await state.set_state(MemberForm.username)


@guild_router.message(StateFilter(MemberForm))
async def enter_member(message: Message, state: FSMContext):
    await state.update_data(member=message.text)
    data = await state.get_data()
    member = data["member"]

    guild_api = GuildAPI("./storage/guilds.json")
    company_api = CompanyAPI("./storage/companies.json")

    user: User = dependency.key_value_parameters["user"]
    company: Company = await company_api.handle_company(user.id)
    
    employee = await company_api.handle_employee(member, company.name)
    if employee is None:
        await message.answer("Сотруднка с таким именем нет в организации")
        return

    await guild_api.add_member(member, company.name)

    await message.answer("Сотрудник добавлен!")
    await state.clear()
