"""
Заготовка для Бота отправляющего в Чат (групповой например)
Сообщений при наступлении некоторого ВНЕШНЕГО События
В качестве имитации такого события - Время - четные минуты
"""
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN, CHAT_ID_GROUP

date_format = '%Y-%m-%d %H:%M:%S'
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def get_event():
    dt_format = ('%M')
    minutes = int(datetime.now().strftime(dt_format))
    event = True if not minutes % 2 else False
    signal = 'Покупайте' if int(str(minutes)[-1]) > 4 else 'Продавайте'
    return event, signal

async def send_message_to_chat_by_event():
    while True:
        event, signal = get_event()
        if event:
            await bot.send_message(chat_id=CHAT_ID_GROUP, text=f'EVENT BOT | Следуйте Инструкциям: {signal}')
        await asyncio.sleep(60)

async def main():
    print(f'Бот начал работу. | {datetime.now().strftime(date_format)}')

    # Игнорирует те обновления события, пока Бот был неактивен
    await bot.delete_webhook(drop_pending_updates=False)

    # Отправка Сообщений по внешнему событию
    await send_message_to_chat_by_event()

    # Запускает Процесс (бесконечный цикл) проверки обновлений событий
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())