import asyncio
from aiogram import Bot, Dispatcher
from src.commands import commands_router
from src.handlers.admin import admin_router
from src.handlers.company import company_router
from src.handlers.guild import guild_router

bot = Bot("")
dp = Dispatcher()

dp.include_router(commands_router)
dp.include_router(admin_router)
dp.include_router(company_router)
dp.include_router(guild_router)


async def run_app():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":    
    asyncio.run(run_app())
