from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class CounterMiddleware(BaseMiddleware):
    """
    Элементарный Пример работы Класса Промежуточного Слоя
    """
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        # handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        # event: Message,
        # Общий случай Событий не только сообщение:
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        self.counter += 1
        data['counter'] = self.counter
        return await handler(event, data)

# router = Router()
# router.message.middleware(CounterMiddleware())