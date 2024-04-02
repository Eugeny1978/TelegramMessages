from aiogram import F, Router, types
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply_buttons import get_keyboard
from middlewares.db import CounterMiddleware
import database.orm_queries as queries

admin_router = Router()
admin_router.message.middleware(CounterMiddleware())
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())



admin_keyboard = get_keyboard(
    buttons=["Добавить Товар", "Ассортимент"],
    placeholder="Выберите действие:",
    sizes=(2,) )

remove_keyboard = get_keyboard(buttons=['Назад', 'Отмена'], placeholder="Выберите действие:")

@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=admin_keyboard)

@admin_router.message(F.text.casefold() == 'ассортимент')
async def starring_at_product(message: types.Message, session: AsyncSession):
    await message.answer("Список товаров:")
    for product in await queries.orm_get_all_products(session):
        await message.answer_photo(product.image,
            caption=f"<b>{product.name}</b>\n{product.description}\nЦена: {round(product.price, 2)}")


# @admin_router.message(F.text.casefold() == "изменить товар")
# async def change_product(message: types.Message):
#     await message.answer("Вот список товаров:")
#
# @admin_router.message(F.text.lower() == "удалить товар")
# async def delete_product(message: types.Message, counter):
#     print(counter)
#     await message.answer("Выберите товар(ы) для удаления")

# Код ниже для машины состояний (FSM)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    messages = {
        'AddProduct:name': 'Введите название Товара:',
        'AddProduct:description': 'Введите описание товара:',
        'AddProduct:price': 'Введите стоимость товара:',
        'AddProduct:image': 'Загрузите изображение товара:'
    }

@admin_router.message(F.text == "Добавить Товар", StateFilter(None))
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Введите название товара", reply_markup=remove_keyboard) # types.ReplyKeyboardRemove()
    await state.set_state(AddProduct.name)

@admin_router.message(Command("cancel"), StateFilter('*'))
@admin_router.message(F.text.casefold() == "отмена", StateFilter('*'))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if not current_state: return
    await state.clear()
    await message.answer("Действия отменены", reply_markup=admin_keyboard)

@admin_router.message(Command("back"))
@admin_router.message(F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await state.clear()
        await message.answer('Вы отменили введеное Название Товара и вернулись в начало.', reply_markup=admin_keyboard)
        return
    prev_state = None
    for step_state in AddProduct.__all_states__:
        if step_state == current_state:
            await state.set_state(prev_state)
            await message.answer(f"Вы вернулись к предыдущему шагу:\n{AddProduct.messages[prev_state]}", reply_markup=remove_keyboard)
            return
        prev_state = step_state

@admin_router.message(F.text, AddProduct.name)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара", reply_markup=remove_keyboard)
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.name) # Если Введен некорректный Тип данных
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимый тип данных.\nВведите ТЕКСТ: Названия товара", reply_markup=remove_keyboard)
    await message.delete()

@admin_router.message(F.text, AddProduct.description)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара", reply_markup=remove_keyboard)
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.description)  # Если Введен некорректный Тип данных
async def add_description(message: types.Message):
    await message.answer("Вы ввели недопустимый тип данных.\nВведите ТЕКСТ: Описание товара", reply_markup=remove_keyboard)
    await message.delete()

@admin_router.message(F.text, AddProduct.price)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара", reply_markup=remove_keyboard)
    await state.set_state(AddProduct.image)

@admin_router.message(AddProduct.price) # Если Введен некорректный Тип данных
async def add_price(message: types.Message):
    await message.answer("Вы ввели недопустимый тип данных.\nВведите ТЕКСТ: Стоимость товара", reply_markup=remove_keyboard)
    await message.delete()

@admin_router.message(F.photo, AddProduct.image)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        await queries.orm_add_product(session, data)
        await message.answer("Товар добавлен", reply_markup=admin_keyboard)
        # await message.answer(str(data))
    except Exception as error:
        await message.answer('Товар НЕ сохранен в Базе Данных | Ошибка Доступа.', reply_markup=admin_keyboard)
    await state.clear()  # await state.set_state(StateFilter(None))

@admin_router.message(AddProduct.image) # Если Введен некорректный Тип данных
async def add_image(message: types.Message):
    await message.answer("Вы ввели недопустимый тип данных.\nОтправьте ФОТО: Изображение товара", reply_markup=remove_keyboard)
    await message.delete()
