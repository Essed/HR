from aiogram.types import  KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_menu = ReplyKeyboardBuilder()
start_menu.add(
    KeyboardButton(text="Подробнее об ассистенте"),
    KeyboardButton(text="Тарифы"),
    KeyboardButton(text="Присоединиться к организации")
)
start_menu.adjust(1)

pay_menu = ReplyKeyboardBuilder()
pay_menu.add(
    KeyboardButton(text="Пополнить баланс"),
    KeyboardButton(text="Купить")
)


start_menu_admin = ReplyKeyboardBuilder()
start_menu_admin.add(
    KeyboardButton(text="Создать организацию"),
    KeyboardButton(text="Создать гильдию"),
    KeyboardButton(text="Добавить сотрудника")
)
start_menu_admin.adjust(2,2)

menu_hr = ReplyKeyboardBuilder()
menu_hr.add(
    KeyboardButton(text="Наградить сотрудника"),
    KeyboardButton(text="Профиль")
)

menu_employe = ReplyKeyboardBuilder()
menu_employe.add(
    KeyboardButton(text="Профиль"),
    KeyboardButton(text="Кубки"),
    KeyboardButton(text="Гильдия")
)


menu_guild = ReplyKeyboardBuilder()
menu_guild.add(
    KeyboardButton(text="Рейтинг сотрудников")    
)