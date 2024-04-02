from aiogram import F, Router, types
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import ReplyKeyboardRemove

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply_buttons import get_keyboard
from keyboards.inline_buttons import get_inline_buttons
from middlewares.db import CounterMiddleware
import database.orm_queries as queries

admin_router = Router()
admin_router.message.middleware(CounterMiddleware())
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

admin_keyboard = get_keyboard(buttons=["❇️ Добавить Товар", "🍕 Ассортимент"])
remove_keyboard = get_keyboard(buttons=['◀️ Назад', '🟥 Отмена']) #  https://www.emojiall.com/ru/categories/I

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    product_for_update = None
    messages = {
        'AddProduct:name': 'Введите название Товара:',
        'AddProduct:description': 'Введите описание товара:',
        'AddProduct:price': 'Введите стоимость товара:',
        'AddProduct:image': 'Загрузите изображение товара:'
    }


@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Используйте Кнопки Клавиатуры:\n| Добавить Товар | Ассортимент |", reply_markup=admin_keyboard)

@admin_router.message(F.text.casefold().contains('ассортимент'))
async def get_assortment_products(message: types.Message, session: AsyncSession):
    await message.answer("Список товаров:")
    for product in await queries.orm_get_all_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<b>{product.name}</b>\n{product.description}\nЦена: <b>{round(product.price, 2)}</b> руб.",
            reply_markup=get_inline_buttons(buttons={'Изменить': f'update_{product.id}', 'Удалить': f'delete_{product.id}'})
        )

@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = int(callback.data.split('_')[-1])
    await queries.orm_delete_product(session, product_id)
    await callback.answer('Товар Удален', show_alert=True)
    await callback.message.answer('Товар Удален!')

# # Код для машины состояний (FSM) -------------------------------------------------------------------------------------

# Изменение Товара - Становимся в состояние ожидания ввода name
@admin_router.callback_query(F.data.startswith('update_'), StateFilter(None))
async def update_product(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    product_id = int(callback.data.split('_')[-1])
    # product_id = int(callback.data.replace('update_', ''))
    product_for_update = await queries.orm_get_product(session, product_id)
    AddProduct.product_for_update = product_for_update
    print(str(AddProduct.product_for_update))
    await callback.answer() # отправляю ответ - тк нажатие на кнопку ожидает ответа
    await callback.message.answer('Введите Название Товара', reply_markup=remove_keyboard)
    await state.set_state(AddProduct.name)

 # Добавлние Товара - Становимся в состояние ожидания ввода name
@admin_router.message(F.text.casefold().contains('добавить товар'), StateFilter(None))
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Введите название товара", reply_markup=remove_keyboard) # types.ReplyKeyboardRemove()
    await state.set_state(AddProduct.name)

# Хендлер отмены и сброса состояния должен быть всегда именно хдесь,
# после того как только встали в состояние номер 1 (очередность фильтров)
@admin_router.message(Command("cancel"), StateFilter('*'))
@admin_router.message(F.text.casefold().contains("отмена"), StateFilter('*'))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if not current_state:
        return
    if AddProduct.product_for_update:
        AddProduct.product_for_update = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=admin_keyboard)

# Вернутся на шаг назад (на прошлое состояние)
@admin_router.message(Command("back"), StateFilter("*"))
@admin_router.message(F.text.casefold().contains("назад"), StateFilter("*"))
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

# Ловим данные для состояние name и потом меняем состояние на description
@admin_router.message(F.text, AddProduct.name) # or_f(F.text, F.text == '.')
async def add_name(message: types.Message, state: FSMContext):
    if message.text == '-':
        await state.update_data(name=AddProduct.product_for_update.name)
    else:
        # Проверка на кол-во символов:
        if len(message.text) > 150:
            await message.reply_to_message(f'Макс. длина Названия = 150 символов.\nВы ввели {len(message.text)} символов.\nПовторите Ввод:')
            return
        await state.update_data(name=message.text)
    await message.answer("Введите описание товара", reply_markup=remove_keyboard)
    await state.set_state(AddProduct.description)

# Хендлер Если Введен некорректный Тип данных для состояния name
@admin_router.message(AddProduct.name) # Если Введен некорректный Тип данных
async def add_incorrect_name(message: types.Message):
    await message.answer("Вы ввели недопустимый тип данных.\nВведите ТЕКСТ: Названия товара", reply_markup=remove_keyboard)
    await message.delete()

# Ловлю данные для состояние description и потом меняю состояние на price
@admin_router.message(F.text, AddProduct.description)
async def add_description(message: types.Message, state: FSMContext):
    if message.text == "-":
        await state.update_data(description=AddProduct.product_for_update.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара", reply_markup=remove_keyboard)
    await state.set_state(AddProduct.price)

# Хендлер Если Введен некорректный Тип данных для состояния description
@admin_router.message(AddProduct.description)  # Если Введен некорректный Тип данных
async def add_incorrect_description(message: types.Message):
    await message.answer("Вы ввели недопустимый тип данных.\nВведите ТЕКСТ: Описание товара", reply_markup=remove_keyboard)
    await message.delete()

# Ловим данные для состояние price и потом меняем состояние на image
@admin_router.message(F.text, AddProduct.price)
async def add_price(message: types.Message, state: FSMContext):
    if message.text == "-":
        await state.update_data(price=AddProduct.product_for_update.price)
    else:
        # Проверка на число
        try: price = round(float(message.text), 2)
        except ValueError:
            await message.reply_to_message('Введите Цену числом. Если есть копейки - дробная часть "." (точка)!\nПовторите Ввод:')
            return
        await state.update_data(price=str(price))
    await message.answer("Загрузите изображение товара", reply_markup=remove_keyboard)
    await state.set_state(AddProduct.image)

# Хендлер Если Введен некорректный Тип данных для состояния price
@admin_router.message(AddProduct.price) # Если Введен некорректный Тип данных
async def add_incorrect_price(message: types.Message):
    await message.answer("Вы ввели недопустимый тип данных.\nВведите ТЕКСТ: Стоимость товара", reply_markup=remove_keyboard)
    await message.delete()

# Ловим данные для состояние image и потом выходим из состояний
@admin_router.message(or_f(F.photo, F.text == "-"), AddProduct.image)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == "-":
        await state.update_data(image=AddProduct.product_for_update.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddProduct.product_for_update:
            await queries.orm_update_product(session, data, AddProduct.product_for_update.id)
            info = 'Изменен'
        else:
            await queries.orm_add_product(session, data)
            info = 'Добавлен'
        await message.answer(f"Товар {info}", reply_markup=admin_keyboard)
    except Exception:
        await message.answer('Товар НЕ сохранен в Базе Данных | Ошибка Доступа.', reply_markup=admin_keyboard)
    await state.clear() # очищаю состояние в любом случае. чтобы не было застревания в этом состоянии # await state.set_state(StateFilter(None))
    AddProduct.product_for_update = None

# Хендлер Если Введен некорректный Тип данных для состояния image
@admin_router.message(AddProduct.image) #
async def add_incorrect_image(message: types.Message):
    await message.answer("Вы ввели недопустимый тип данных.\nОтправьте ФОТО: Изображение товара", reply_markup=remove_keyboard)
    await message.delete()
