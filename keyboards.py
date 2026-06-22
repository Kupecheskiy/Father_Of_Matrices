from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сложение"), KeyboardButton(text="Вычитание")],
        [KeyboardButton(text="Умножение"), KeyboardButton(text="Транспонирование")],
        [KeyboardButton(text="Определитель"), KeyboardButton(text="Обратная матрица")],
        [KeyboardButton(text="Ранг"), KeyboardButton(text="❌ Отмена ❌")],
    ],
    resize_keyboard=True
)