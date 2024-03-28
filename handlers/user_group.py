from string import punctuation
from aiogram import F, Router, types
from filtres.chat_types import ChatTypeFilter

router_user_group = Router()
router_user_group.message.filter(ChatTypeFilter(['group', 'supergroup'])) # разделяю где будут работать роутер и его хендлеры

restricted_words = {'кабан', 'хомяк', 'хер', 'выхухоль', 'бармалей'}

def remove_punctuation(text: str):
    return text.translate(str.maketrans('', '', punctuation))

@router_user_group.edited_message()
@router_user_group.message()
async def cleaner_restricted_words(message: types.Message):
    cleaned_text = remove_punctuation(message.text.lower())
    if restricted_words.intersection(cleaned_text.split()):
        await message.reply(f'{message.from_user.first_name}, - Ругаться в группе запрещено! Будьте корректны в общении с коллегами')
        await message.delete()
        # await message.chat.ban(message.from_user.id)