from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, KeyboardButtonPollType # Лаконичное Быстрое Создание Кнопок
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
start_kb2.add(KeyboardButton(text='Menu v2'),
    KeyboardButton(text='About Us v2'),
    KeyboardButton(text='Payment v2'),
    KeyboardButton(text='Shipping v2')
)
start_kb2.adjust(2, 2)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
# start_kb3.add(KeyboardButton(text='Send Review'))
# start_kb3.adjust(2, 2, 1)
start_kb3.row(KeyboardButton(text='Send Review'))

test_keyboard = ReplyKeyboardMarkup(
    keyboard=
    [
        [ # 1й ряд кнопок
        KeyboardButton(text='Create Test', request_poll=KeyboardButtonPollType())
        ],
        [ # 2й ряд кнопок
            KeyboardButton(text='Send Telephone Number tofu :on :fire :smile :aircraft :nerd_face :is missing  ', request_contact=True),
        KeyboardButton(text='Send Location ', request_location=True)
        ]
    ],
    resize_keyboard=True
)

