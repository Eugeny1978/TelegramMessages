from string import punctuation
from aiogram import F, Router, types, Bot
from aiogram.filters import Command, or_f

from filters.chat_types import ChatTypeFilter
from common import restricted_words

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup'])) # разделяю где будут работать роутер и его хендлеры


def remove_punctuation(text: str):
    return text.translate(str.maketrans('', '', punctuation))

@user_group_router.message(Command('admin'))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins = await bot.get_chat_administrators(chat_id)
    # print(admins) # просмотреть все данные полученного объекта
    admin_ids = [admin.user.id for admin in admins]
    bot.my_admins_list = admin_ids
    if message.from_user.id in admin_ids:
        await message.delete()
    # print(bot.my_admins_list)

@user_group_router.edited_message()
@user_group_router.message()
async def cleaner_restricted_words(message: types.Message):
    cleaned_text = remove_punctuation(message.text.lower())
    if restricted_words.intersection(cleaned_text.split()):
        await message.reply(f'{message.from_user.first_name}, - Ругаться в группе запрещено! Будьте корректны в общении с коллегами')
        await message.delete()
        # await message.chat.ban(message.from_user.id)
    # # Узнать ID чата.
    # chat_id = message.chat.id  # работает и для приватного(лс) чата и для общих чатов (групп)
    # # print(chat_id)
    # await message.answer('Следуйте Указаниям!') # chat_id=chat_id, text=

