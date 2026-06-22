import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from config import BOT_TOKEN
from keyboards import main_keyboard
from matrix_ops import Matrix
from utils import user_data

router = Router()


def format_number(x: float) -> str:
    """Форматирует число для определителя и ранга."""
    if abs(x - round(x)) < 1e-10:
        return str(int(round(x)))
    s = f"{x:.4f}".rstrip('0').rstrip('.')
    return s


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Приветствую! Я бот для работы с матрицами.\n"
        "Выбери операцию на клавиатуре.",
        reply_markup=main_keyboard
    )


@router.message(F.text == "❌ Отмена ❌")
async def cancel_handler(message: Message):
    user_id = message.from_user.id
    if user_id in user_data:
        del user_data[user_id]
    await message.answer(
        "Операция отменена. Выбери новую операцию.",
        reply_markup=main_keyboard
    )


@router.message(F.text.in_(["Сложение", "Вычитание", "Умножение"]))
async def binary_operation_handler(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {
        "operation": message.text,
        "step": 1
    }
    await message.answer(
        "Введи первую матрицу построчно.\nПример:\n1 2\n3 4\n\n"
        "Числа разделяй пробелами, строки — переносом строки. "
        "Можно использовать запятые вместо пробелов."
    )


@router.message(F.text.in_(["Транспонирование", "Определитель", "Обратная матрица", "Ранг"]))
async def unary_operation_handler(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {
        "operation": message.text,
        "step": 1
    }
    await message.answer(
        "Введи матрицу построчно.\nПример:\n1 2\n3 4\n\n"
        "Числа разделяй пробелами, строки — переносом строки."
    )


@router.message()
async def process_matrix_input(message: Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        await message.answer(
            "Сначала выбери операцию с помощью кнопок.",
            reply_markup=main_keyboard
        )
        return

    operation = user_data[user_id]["operation"]
    step = user_data[user_id]["step"]

    try:
        # Создаём объект Matrix из текста
        matrix = Matrix.from_text(message.text)

        # Бинарные операции
        if operation in ["Сложение", "Вычитание", "Умножение"]:
            if step == 1:
                user_data[user_id]["matrix1"] = matrix
                user_data[user_id]["step"] = 2
                await message.answer("Теперь введи вторую матрицу.")
                return

            elif step == 2:
                matrix1 = user_data[user_id]["matrix1"]
                matrix2 = matrix

                if operation == "Сложение":
                    result = matrix1 + matrix2
                    await message.answer(f"Результат сложения:\n{result}")

                elif operation == "Вычитание":
                    result = matrix1 - matrix2
                    await message.answer(f"Результат вычитания:\n{result}")

                elif operation == "Умножение":
                    result = matrix1 @ matrix2
                    await message.answer(f"Результат умножения:\n{result}")

                user_data.pop(user_id)

        # Унарные операции
        else:
            if operation == "Транспонирование":
                result = matrix.transpose()
                await message.answer(f"Транспонированная матрица:\n{result}")

            elif operation == "Определитель":
                result = matrix.determinant()
                await message.answer(f"Определитель: {format_number(result)}")

            elif operation == "Обратная матрица":
                result = matrix.inverse()
                await message.answer(f"Обратная матрица:\n{result}")

            elif operation == "Ранг":
                result = matrix.rank()
                await message.answer(f"Ранг матрицы: {result}")

            user_data.pop(user_id)

    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())