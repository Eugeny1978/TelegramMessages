from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder # Более Гибко Подробное Создание Кнопок

# Удаление Текущих Клавиатур
delete_keyboard = ReplyKeyboardRemove()

# 1й Способ Создания. Используя Класс ReplyKeyboardMarkup
start_keyboard = ReplyKeyboardMarkup(
    keyboard=
    [
        [ # 1й ряд кнопок
        KeyboardButton(text='Menu'),
        KeyboardButton(text='About Us')
        ],
        [ # 2й ряд кнопок
        KeyboardButton(text='Payment'),
        KeyboardButton(text='Shipping')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Хотите сделать заказ?'
)

# 1й Способ Создания. Используя Класс ReplyKeyboardBuilder
start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(KeyboardButton(text='Menu'),
    KeyboardButton(text='About Us'),
    KeyboardButton(text='Payment'),
    KeyboardButton(text='Shipping')
)
start_kb2.adjust(2, 2)
start_keyboard_2 = start_kb2.as_markup(resize_keyboard=True, input_field_placeholder='Хотите сделать заказ?')

# Возможность Присоединять и добавлять новые кнопки
start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
# start_kb3.add(KeyboardButton(text='Send Review'))
# start_kb3.adjust(2, 2, 1)
start_kb3.row(KeyboardButton(text='Send Review'))
start_keyboard_3 = start_kb3.as_markup(resize_keyboard=True, input_field_placeholder='Хотите сделать заказ?')


payment_kb = ReplyKeyboardBuilder()
for i in range(1, 16):
    payment_kb.add(KeyboardButton(text=str(i)))
payment_kb.adjust(5, 5, 5)
payment_keyboard = payment_kb.as_markup(resize_keyboard=True, input_field_placeholder='Наберите Номер заказа:')


review_keyboard = ReplyKeyboardMarkup(
    keyboard=
    [
        [ # 1й ряд кнопок
        KeyboardButton(text='Create Poll', request_poll=KeyboardButtonPollType())
        ],
        [ # 2й ряд кнопок
        KeyboardButton(text='Send Telephone Number', request_contact=True),
        KeyboardButton(text='Send Location ', request_location=True)
        ]
    ],
    resize_keyboard=True
)



