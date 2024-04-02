from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_callback_buttons( *, buttons: dict[str, str], sizes: tuple = (2,)):
    keyboard = InlineKeyboardBuilder()
    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()

def get_url_buttons( *, buttons: dict[str, str], sizes: tuple = (2,)):
    keyboard = InlineKeyboardBuilder()
    for text, url in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))
    return keyboard.adjust(*sizes).as_markup()

def get_inline_buttons( *, buttons: dict[str, str], sizes: tuple[int] = (2, )):
    keyboard = InlineKeyboardBuilder()
    for text, value in buttons.items():
        url, callback = None, None
        if '://' in value:
            url = value
        else:
            callback = value
        keyboard.add(InlineKeyboardButton(text=text, url=url, callback_data=callback))
    return keyboard.adjust(*sizes).as_markup()
