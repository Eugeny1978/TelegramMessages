from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command, or_f
from filtres.chat_types import ChatTypeFilter

router_user_private = Router()
router_user_private.message.filter(ChatTypeFilter(['private']))  # разделяю где будут работать роутер и его хендлеры


@router_user_private.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помошник!')

# Несколько разнотипных условий повесил на один обработчик
# @router_user_private.message(Command('menu'))
@router_user_private.message(or_f(Command('menu'), F.text.lower().contains('меню')))
async def trades_cmd(message: types.Message):
    await message.answer('MENU:')

# @router_user_private.message(Command('about'))
@router_user_private.message(or_f(Command('about'), F.text.lower().contains('о вас'), F.text.lower().contains('о нас')))
async def about_cmd(message: types.Message):
    await message.answer('About us')

# @router_user_private.message(Command('payment'))
@router_user_private.message(or_f(Command('payment'), F.text.lower().contains('плати')))
async def payment_cmd(message: types.Message):
    await message.answer('Payment variants')

# @router_user_private.message(Command('shipping'))
@router_user_private.message(or_f(Command('shipping'), F.text.lower().contains('достав')))
async def shipping_cmd(message: types.Message):
    await message.answer('Shipping variants')

# @router_user_private.message(F.text.lower() == 'варианты доставки')
# async def magic_v1(message: types.Message):
#     await message.answer('Executing "варианты доставки"')
#
# @router_user_private.message(F.text.contains('достав'))
# async def magic_v2(message: types.Message):
#     await message.answer('Executing contains "достав"')
#
# @router_user_private.message(F.from_user.id.in_({444, 555, 666, 381042342}))
# async def magic_v3(message: types.Message):
#     await message.answer('Executing from_user.id.in_')
#
# @router_user_private.message(F.text)
# async def magic_text_filter(message: types.Message):
#     pprint(message)
#     await message.answer('Executing TEXT magic filter')
#
# @router_user_private.message(F.photo)
# async def magic_photo_filter(message: types.Message):
#     await message.answer('Executing PHOTO magic filter')


# @router_user_private.message(Command('trades'))
# async def menu_cmd(message: types.Message):
#     await message.answer('Responce to command Trades')

# @router_user_private.message()
# async def get_echo(message: types.Message):
#     text: str | None = message.text
#     autor = message.from_user.first_name
#     if text in ('hi', 'hello', 'привет', 'здравствуй'):
#         answer = f'{autor}, Наше Вам с кисточкой! Привет!'
#     elif text in ('bye', 'пока', 'прощай', 'до свидания'):
#         answer = f'{autor}, Пока! Приходите еще!'
#     else:
#         answer = f'{autor}, я понял Вас. Вы написали: "{text}"'
#     await message.answer(answer)
#     await message.reply(answer)