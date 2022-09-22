import os
from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
    qrname TEXT,
    kolichestvo int NOT NULL DEFAULT 4,
    kosiak int NOT NULL DEFAULT 0
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
        sql.execute("SELECT qrname FROM QRPetrol WHERE kolichestvo = ?", ("4", ))
        name = sql.fetchone()
        return name[0]


def addSQL(message):
    try:
        with sqlite3.connect("Petrol.db") as QrPetrol:
            name = message.photo[0].file_unique_id + ".jpeg"
            sql = QrPetrol.cursor()
            sql.execute("SELECT qrname FROM QRPetrol WHERE qrname = (?)", (name,))
            data = sql.fetchone()
            if data is None:
                sql.execute(f"INSERT INTO QRPetrol (qrname) VALUES (?)", (name,))
                return True
            else:
                return False
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite addSQL", error)


def changeParametr(parametr, num, id):  # обновляет заданный параметр в sql по одному
    try:
        with sqlite3.connect("Petrol.db") as QrPetrol:
            sql = QrPetrol.cursor()
            # sql.execute(f"""UPDATE QRPetrol SET kolichestvo = {num} WHERE `qrname` = `{id}`""")
            sql.execute('UPDATE QRPetrol SET ? = ? WHERE qrname = ?', (parametr, num, id))
            QrPetrol.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite changeParametr", error)


@dispatcher.callback_query_handler(lambda c: c.data == "GiveQR")
async def giveQR(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Заправился, спасибо)", callback_data="GiveQR")
    button2 = InlineKeyboardButton("QR не работает", callback_data="GiveQR")
    markup.add(button1, button2)
    name = giveFreshQR()
    photo = open(f"{name}", "rb")
    changeParametr('kolichestvo', '0', name)
    await bot.send_photo(call.message.chat.id, photo=photo, reply_markup=markup)
    await bot.answer_callback_query(call.id)


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
