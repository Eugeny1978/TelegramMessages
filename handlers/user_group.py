from string import punctuation
from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, Command, or_f, StateFilter
import json

from filters.chat_types import ChatTypeFilter
# from common.banned_words import restricted_words

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup'])) # разделяю где будут работать роутер и его хендлеры


def remove_punctuation(text: str):
    return text.translate(str.maketrans('', '', punctuation))

@user_group_router.message(CommandStart(), StateFilter(None))
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помошник!')
    # await message.answer(f'CHAT ID: {message.chat.id}') # id чата

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
    # cleaned_text = remove_punctuation(message.text.lower())
    # if restricted_words.intersection(cleaned_text.split()):
    #     await message.reply(f'{message.from_user.first_name}, - Ругаться в группе запрещено! Будьте корректны в общении с коллегами')
    #     await message.delete()
    #     # await message.chat.ban(message.from_user.id)

    path_file_cenz = r'./common/cenz.json'
    cenzored_words = set(json.load(open(path_file_cenz)))
    message_words = remove_punctuation(message.text.lower()).split()
    if cenzored_words.intersection(message_words):
        await message.reply(f'{message.from_user.first_name}, Ругаться в группе запрещено! Будьте корректны в общении с коллегами')
        await message.delete()
        # await message.chat.ban(message.from_user.id)






