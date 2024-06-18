from app.scraper import ProductChecker
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
import app.bot.keyboard as kb
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from app.core import add_user, add_product, add_product_update, get_product_statistics, add_user_product
from app.database import session

rt = Router()
checker = ProductChecker()


class Connection(StatesGroup):
    url = State()
    time = State()
    confirm = State()


# SQLAlchemy session creation
engine = create_engine('sqlite:///your_database.db')  # Replace with your actual database URL
Session = sessionmaker(bind=engine)


@rt.message(CommandStart())
async def start(message: Message):
    await message.answer("Чекай продажи на Маркетплейсе с помощью меня!\nВот список всех команд:",
                         reply_markup=kb.start_btn())


# Стартовый хэндлер
@rt.message(F.text == "Поставить маркер")
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Connection.url)
    await message.reply("Введите URL:", reply_markup=ReplyKeyboardRemove())


# Хэндлер для проверки URL
@rt.message(StateFilter(Connection.url))
async def process_url(message: Message, state: FSMContext):
    url_pattern = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$')
    if not url_pattern.match(message.text):
        await message.reply("Некорректный URL. Попробуйте снова.")
        return

    await state.update_data(url=message.text)
    await state.set_state(Connection.time)
    await message.reply("Введите количество итераций:")


# Хэндлер для проверки количества итераций
@rt.message(StateFilter(Connection.time), lambda message: not message.text.isdigit())
async def process_iterations_invalid(message: Message):
    await message.reply("Время итераций должно быть числом. Попробуйте снова.")


@rt.message(StateFilter(Connection.time), lambda message: message.text.isdigit())
async def process_iterations(message: Message, state: FSMContext):
    await state.update_data(time=int(message.text))
    data = await state.get_data()
    await message.answer(f"Подтвердите информацию:\nURL: {data['url']}\nВремя итерации: {data['time']}",
                         reply_markup=kb.confirm())
    await state.set_state(Connection.confirm)


# Хэндлер для подтверждения
@rt.message(StateFilter(Connection.confirm), lambda message: message.text.lower() not in ['да', 'нет'])
async def process_confirm_invalid(message: Message):
    await message.reply("Ответ должен быть 'да' или 'нет'. Попробуйте снова.", reply_markup=kb.confirm())


@rt.message(StateFilter(Connection.confirm), lambda message: message.text.lower() == 'да')
async def process_confirm_yes(message: Message, state: FSMContext):
    data = await state.get_data()

    try:
        user, product, user_product = add_user_product(session, telegram_id=message.from_user.id,
                                                       username=message.from_user.username, url=data['url'])

        await message.reply(f"Спасибо! Введенные данные:\nURL: {data['url']}\nВремя итерации: {data['time']}",
                            reply_markup=ReplyKeyboardRemove())
        await state.clear()

        for _ in range(26):
            info = await asyncio.create_task(checker.markup(data['url'], int(data['time'])))

            rating = info.get('rating', 0.0)
            grades = info.get('grades', 0)
            orders = info.get('orders', 0)
            values = info.get('values', 0)
            add_product_update(session, user_product_id=user_product.id, rating=rating, grades=grades, orders=orders,
                               values=values)
            await message.answer(f"{info}")

        stats = get_product_statistics(session, product_id=user_product.product_id)
        if stats and len(stats) > 1:
            await message.answer(f"Статистика продукта: От {stats[0].updated_date} до {stats[-1].updated_date}")
        else:
            await message.answer("Недостаточно данных для статистики.")

    except Exception as e:
        await message.reply("Произошла ошибка при добавлении пользователя и продукта или обработке обновлений.")
        print(f"Error adding user and product or processing updates: {e}")

    finally:
        session.close()


@rt.message(StateFilter(Connection.confirm), lambda message: message.text.lower() == 'нет')
async def process_confirm_no(message: Message, state: FSMContext):
    await message.reply("Ввод данных отменен.", reply_markup=kb.start_btn())
    await state.clear()


@rt.message(F.text == "Узнать кол-во позиций")
async def markup_get_url(message: Message):
    data = await asyncio.create_task(checker.all_positions())
    await message.answer(data)
