import os

from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentType, Message
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
import logging
import time

if not os.path.exists("QrCode"):
    os.mkdir("QrCode")

os.chdir("QrCode")

with sqlite3.connect("Petrol.db") as QrPetrol:
    sql = QrPetrol.cursor()
    table = """CREATE TABLE IF NOT EXISTS `QRPetrol` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adress TEXT,
    count int NOT NULL DEFAULT 4
    )"""
    sql.executescript(table)

TOKEN = "5602345357:AAE3DfCvLMjthTou9tbU4S9uJbGj0jVTwSg"

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot)

id_gosha = 498332094



@dispatcher.message_handler(commands=["start"])  # обработка команды /start
async def begin(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Not work", callback_data="NewSdelka")
    button2 = InlineKeyboardButton("Выдать QR", callback_data="GiveQR")
    markup.add(button1, button2)
    await message.answer(f"Пс, парень! Не хочешь не много заправиться?)", reply_markup=markup)


def giveFreshQR():
    with sqlite3.connect("Petrol.db") as QrPetrol:
        sql = QrPetrol.cursor()
        sql.execute("SELECT adress FROM QRPetrol WHERE count = ?", ("4", ))
        name = sql.fetchone()
        return name[0]


@dispatcher.callback_query_handler(lambda c: c.data == "GiveQR")
async def giveQR(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("QR не работает", callback_data="GiveQR")
    markup.add(button2)
    name = giveFreshQR()
    photo = open("QrCode"/{name}, "rb")
    print(photo)
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, "Нажми, если QR не работает", reply_markup=markup)

@dispatcher.callback_query_handler(lambda c: c.data == "downloadQR")
async def giveQR(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("Отмена", callback_data="start")
    markup.add(button2)

    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, "sfeefef", reply_markup=markup)


def addSQL(message):
    try:
        with sqlite3.connect("Petrol.db") as QrPetrol:
            name = message.photo[0].file_unique_id + ".jpeg"
            sql = QrPetrol.cursor()
            sql.execute("SELECT adress FROM QRPetrol WHERE adress = ?", (name,))
            data = sql.fetchone()
            if data is None:
                sql.execute(f"INSERT INTO QRPetrol (adress) VALUES (?)", (name,))
                return True
            else:
                return False
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


@dispatcher.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    if message.chat.id == id_gosha:
        if addSQL(message):
            name = message.photo[0].file_unique_id + ".jpeg"
            await message.photo[-1].download(name)
            await message.answer("QR добавлен в базу")
        else:
            await message.answer("Этот QR уже загружен")
    else:
        await message.answer("Нет прав на добавление QR")






if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher,
                           skip_updates=True)