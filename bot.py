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
from config import TOKEN, private_commands
from database import get_token
from handlers.admin_private import admin_router
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
# from middlewares.db import CounterMiddleware

# Ограничил виды обновлений которые будет бот отслеживать | https://core.telegram.org/bots/api#getting-updates
# 'channel_post', 'edited_channel_post', 'message_reaction', 'shipping_query', 'chosen_inline_result' и другие
ALLOWED_UPDATES = ['message', 'edited message']

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


async def main():
    print('Бот начал работу!')
    # Игнорирует те обновления события, пока Бот был неактивен
    await bot.delete_webhook(drop_pending_updates=False)
    # Меню / для Лички
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats())
    # Запускает Процесс (бесконечный цикл) проверки обновлений событий
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
    asyncio.run(main())


