"""
Модуль Запуска
Модуль Создания Логики Бота
Создать Бот Через БотФазер
Токен
Натсройки - описание
Создать группу
Добавить бота в группу
Установить его как администратора в группе
в настройках бота отключить возможность добавки бота в новые группы:
    Allow groups?
    переключатель на Turn groups on
"""
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from datetime import datetime
from config import TOKEN, private_commands
from handlers.admin_private import admin_router
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from database.engine import create_db, drop_db, session_maker # обязательно импорт после config.py чтобы загрузилась переменная с адресом Базы Данных
# from middlewares.db import CounterMiddleware
from middlewares.db import DataBaseSession


# Ограничил виды обновлений которые будет бот отслеживать | https://core.telegram.org/bots/api#getting-updates
# 'channel_post', 'edited_channel_post', 'message_reaction', 'shipping_query', 'chosen_inline_result' и другие
# ALLOWED_UPDATES = ['message', 'edited message', 'callback_query'] # явно прописать те обновления которые нужно отслеживать
# В коде сделал по другому: с помощью метода отслеживающего кикие есть у меня типы изменений

# bot = Bot(token=get_token())
# форматирование сообщений с помощью HTML тегов, также мсожно вставлять в каждый хендлер, но проще прописать тут
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # ParseMode.MARKDOWN_V2
bot.my_admins_list = []

dp = Dispatcher()
# dp.update.outer_middleware(CounterMiddleware()) # действует для всех типов событий для всех роутеров перед фильтрами
# dp.include_routers(router_user_private, router_user_group)
dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)

# chat_id = '-4102589186'
# async def send_message(message: types.Message):
#     await bot.send_message(chat_id=chat_id, text=message)

async def on_startup(bot):
    drop_case = False
    if drop_case:
        await drop_db()
    await create_db() # если таблицы уже существуют создания заново не произойдет

async def on_shutdown(bot):
    print(f'Бот отключился. | {datetime.now().strftime(date_format)}')

date_format = '%Y-%m-%d %H:%M:%S'

async def main():
    print(f'Бот начал работу. | {datetime.now().strftime(date_format)}')

    # Подключаем Базу Данных
    # await create_db()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    # Игнорирует те обновления события, пока Бот был неактивен
    await bot.delete_webhook(drop_pending_updates=False)

    # Меню / для Лички
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats())

    # Запускает Процесс (бесконечный цикл) проверки обновлений событий
    # await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) # см строку выше

if __name__ == '__main__':
    asyncio.run(main())


