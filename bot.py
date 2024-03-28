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
from config import TOKEN, private_commands
from database import get_token
from handlers.user_private import router_user_private
from handlers.user_group import router_user_group

# Ограничил виды обновлений которые будет бот отслеживать
ALLOWED_UPDATES = ['message', 'edited message']

# bot = Bot(token=get_token())
bot = Bot(token=TOKEN)
dp = Dispatcher()
# dp.include_routers(router_user_private, router_user_group)
dp.include_router(router_user_private)
dp.include_router(router_user_group)



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


