import asyncio
from aiogram import Bot, Dispatcher
from src.commands import commands_router
from src.handlers.user import user_router


bot = Bot("")
dp = Dispatcher()

dp.include_router(commands_router)
dp.include_router(user_router)


async def run_app():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":    
    asyncio.run(run_app())
