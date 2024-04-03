from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.utils.formatting import as_list, as_section, as_marked_section, Bold

from sqlalchemy.ext.asyncio import AsyncSession
from filters.chat_types import ChatTypeFilter
from keyboards import reply_buttons_video5 as rbs
from keyboards import reply_buttons as rb
import database.orm_queries as queries

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))  # разделяю где будут работать роутер и его хендлеры

@user_private_router.message(CommandStart(), StateFilter(None))
async def start_cmd(message: types.Message):
    # await message.answer('Привет, я виртуальный помошник!', reply_markup=rbs.start_keyboard)
    # await message.answer('Привет, я виртуальный помошник!', reply_markup=rbs.start_keyboard_3)
    await message.answer('Привет, я виртуальный помошник!',
             reply_markup=rb.get_keyboard(
                 buttons=["Меню", "О магазине", "Варианты оплаты", "Варианты доставки"],
                 placeholder="Что вас интересует?",
                 request_contact=4,  # индекс кнопки. начинается с 1
                 sizes=(2, 2) ) )
    # await message.answer(f"CHAT ID: {message.chat.id}") # id чата
# Несколько разнотипных условий повесил на один обработчик
# @user_private_router.message(Command('menu'))
@user_private_router.message(or_f(Command('menu'), F.text.lower().contains('меню'), F.text.lower().contains('menu')))
async def trades_cmd(message: types.Message, session: AsyncSession):
    await message.answer('MENU:', reply_markup=rbs.delete_keyboard)
    for product in await queries.orm_get_all_products(session):
        await message.answer_photo(product.image,
            caption=f"<b>{product.name}</b>\n{product.description}\nЦена: {round(product.price, 2)}")

# @user_private_router.message(Command('about'))
@user_private_router.message(or_f(Command('about'), F.text.lower().contains('о нас'), F.text.lower().contains('about')))
async def about_cmd(message: types.Message):
    await message.answer('About us')

# @user_private_router.message(Command('payment'))
@user_private_router.message(or_f(Command('payment'), F.text.lower().contains('плати'), F.text.lower().contains('payment')))
async def payment_cmd(message: types.Message):
    answer = as_marked_section(
        Bold('Payment variants (Варианты Оплаты):'),
        'Онлайн в этом Боте',
            'При получении Картой',
            'При получении Наличными',
            'В Пиццерии',
        marker='✅ '
    )
    await message.answer(answer.as_html(), reply_markup=rbs.payment_keyboard)

# @user_private_router.message(Command('shipping'))
@user_private_router.message(or_f(Command('shipping'), F.text.lower().contains('достав'), F.text.lower().contains('shipping')))
async def shipping_cmd(message: types.Message):
    is_yes = as_marked_section(
        Bold('Варианты Доставки (Shipping variants):'),
        'Курьером',
        'Самовывоз',
        'Поем у вас в пиццерии',
        marker='✔️ '
    )
    is_no = as_marked_section(
        Bold('Невозможно:'),
        'Почтой',
        'Голубями',
        marker='❌ '
    )
    div_line = '\n' + '-' * 60 + '\n'
    answer = as_list(is_yes, is_no, sep=div_line)
    await message.answer(answer.as_html())

@user_private_router.message(or_f(Command('review'), F.text.lower().contains('отзыв'), F.text.lower().contains('review')))
async def shipping_cmd(message: types.Message):
    await message.answer('<b>Review</b>', reply_markup=rbs.review_keyboard)

@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer('Telephone Number GETs')
    await message.answer(str(message.contact))

@user_private_router.message(F.location)
async def get_contact(message: types.Message):
    await message.answer('Locatiom GETs')
    await message.answer(str(message.location))



# @user_private_router.message(F.text.lower() == 'варианты доставки')
# async def magic_v1(message: types.Message):
#     await message.answer('Executing "варианты доставки"')
#
# @user_private_router.message(F.text.contains('достав'))
# async def magic_v2(message: types.Message):
#     await message.answer('Executing contains "достав"')
#
# @user_private_router.message(F.from_user.id.in_({444, 555, 666, 381042342}))
# async def magic_v3(message: types.Message):
#     await message.answer('Executing from_user.id.in_')
#
# @user_private_router.message(F.text)
# async def magic_text_filter(message: types.Message):
#     pprint(message)
#     await message.answer('Executing TEXT magic filter')
#
# @user_private_router.message(F.photo)
# async def magic_photo_filter(message: types.Message):
#     await message.answer('Executing PHOTO magic filter')


# @user_private_router.message(Command('trades'))
# async def menu_cmd(message: types.Message):
#     await message.answer('Responce to command Trades')

# @user_private_router.message()
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