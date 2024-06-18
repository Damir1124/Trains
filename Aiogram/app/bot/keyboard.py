from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,\
     KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio


def start_btn():
    kb = [
        [KeyboardButton(text="Help")],
        [KeyboardButton(text="Поставить маркер"), KeyboardButton(text="Узнать кол-во позиций")]
    ]
    kb_start = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду")
    return kb_start


def time_set():
    builder = ReplyKeyboardBuilder()

    for i in range(1, 13):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True)


def confirm():
    kb = [
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ]
    kb_start = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Подтвердите ввод данных")
    return kb_start
