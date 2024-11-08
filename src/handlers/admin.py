from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from src.models.models import Company, User, Employee
from src.api.company import CompanyAPI

from src.enums import Role
from settings import dependency

from src.keyboard import start_menu_admin


admin_router = Router()

class Admin(StatesGroup):
    manager = State()
    employee = State()


@admin_router.message(StateFilter(Admin), F.text.casefold() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действия отменены", reply_markup=start_menu_admin.as_markup(resize_keyboard=True))


@admin_router.message(F.text.casefold() == "добавить руководителя")
async def add_manager(message: Message, state: FSMContext):
    
    user: User = dependency.key_value_parameters["user"]

    if user.role != Role.ADMIN:
        await message.answer("Для назначения руководителей необходимо быть админом")
        return
    
    await state.set_state(Admin.manager)
    await message.answer("Введите имя пользователя в телеграме")


@admin_router.message(StateFilter(Admin.manager))
async def add_username(message: Message, state: FSMContext):
    user: User = dependency.key_value_parameters["user"]
    company_api = CompanyAPI("./storage/companies.json")
    company = await company_api.handle_company(user.id)
    manager: Employee = await company_api.handle_employee(message.text, company.name) 

    if manager is None:
        await message.answer("Сотруднка с таким именем нет в организации")
        return
    manager.role = Role.MANAGER

    await message.answer("Вы назначили руководителя гильдии!")
    await state.clear()


@admin_router.message(F.text.casefold() == "добавить пользователя")
async def add_employee(message: Message, state: FSMContext):
    user: User = dependency.key_value_parameters["user"]
    if user.role != Role.ADMIN:
        await message.answer("Для добавления сотрудников необходимо быть админом")
        return
    
    await state.set_state(Admin.employee)
    await message.answer("Введите имя пользователя в телеграме")


@admin_router.message(StateFilter(Admin.employee))
async def employee_username(message: Message, state: FSMContext):
    employee = Employee(username=message.text, role=Role.USER)
    company_api = CompanyAPI("./storage/companies.json")
    user: User = dependency.key_value_parameters["user"] 
    company: Company = await company_api.handle_company(user.id)

    await company_api.add_employee(employee, company.name)
    await message.answer("Вы добавили сотрудника в компанию!\nОн сможет присоединиться к организации по коду-приглашению")
    await state.clear()

