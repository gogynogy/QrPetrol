import os
from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from aiogram.utils.callback_data import CallbackData

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


with sqlite3.connect("Petrol.db") as QrPetrol:
    sql = QrPetrol.cursor()
    table = """CREATE TABLE IF NOT EXISTS `accounts` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    TelegramNikName TEXT,
    IDTelegram TEXT,
    OstalosQR int NOT NULL DEFAULT 8
    )"""
    sql.executescript(table)


TOKEN = "5602345357:AAE3DfCvLMjthTou9tbU4S9uJbGj0jVTwSg"
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot)
cb = CallbackData('button1', 'username', 'id')


id_lesha = 243626777
id_gosha = 498332094
id_dopusk = (id_gosha, id_lesha)


def giveFreshQR():
    with sqlite3.connect("Petrol.db") as QrPetrol:
        sql = QrPetrol.cursor()
        sql.execute("SELECT qrname FROM QRPetrol WHERE kolichestvo = ?", ("4",))
        name = sql.fetchone()
        return name[0]


def addSQL(message):  #проверяет наличие фото в базе и добавляет
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


def changeCount(num, id):  # изменяет колличество топлива на остатке
    try:
        with sqlite3.connect("Petrol.db") as QrPetrol:
            sql = QrPetrol.cursor()
            sql.execute('''UPDATE QRPetrol SET kolichestvo = ? WHERE qrname = ?''', (num, id))
            QrPetrol.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite changeCount", error)


def kosyakus(id):  # изменяет колличество косяков на карте
    try:
        with sqlite3.connect("Petrol.db") as QrPetrol:
            sql = QrPetrol.cursor()
            sql.execute('''UPDATE QRPetrol SET kosiak = (kosiak + 1) WHERE qrname = ?''', (id, ))
            QrPetrol.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite kosyakus", error)


def nullCount():  # обнуляет топливо на неделю
    try:
        with sqlite3.connect("Petrol.db") as QrPetrol:
            sql = QrPetrol.cursor()
            sql.execute('''UPDATE QRPetrol SET kolichestvo = 4''')
            QrPetrol.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite nullCount", error)


def howMutchIsTheFish():  #считает остаток по топливу
    try:
        with sqlite3.connect("Petrol.db") as QrPetrol:
            sql = QrPetrol.cursor()
            sql.execute(f"""SELECT SUM(kolichestvo) FROM `QRPetrol`""")
            result = sql.fetchone()[0]
            return result
    except sqlite3.Error as error:
            print("Ошибка при работе с SQLite howMutchIsTheFish", error)


def CheckAccount(message):
    try:
        with sqlite3.connect("Petrol.db") as QrPetrol:
            sql = QrPetrol.cursor()
            sql.execute("SELECT IDTelegram FROM accounts WHERE IDTelegram = (?)", (message.chat.id,))
            data = sql.fetchone()
            if data is None:
                return False
            else:
                return True
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite addSQL", error)


def addAccountSQL(username, id):  #проверяет наличие фото в базе и добавляет
    try:
        with sqlite3.connect("Petrol.db") as QrPetrol:
            sql = QrPetrol.cursor()
            sql.execute(f"INSERT INTO accounts (TelegramNikName, IDTelegram) VALUES (?, ?)", (username, id))
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite addSQL", error)


@dispatcher.message_handler(commands=["start"])  # обработка команды /start
async def begin(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton("Обнулить все QR", callback_data="newWeekStart")
    button2 = InlineKeyboardButton("Выдать QR", callback_data="GiveQR")
    if message.chat.id in id_dopusk:
        markup.add(button1, button2)
        count = howMutchIsTheFish()
        await message.answer(f"Пс, парень! Не хочешь не много заправиться?\n "
                             f"до конца недели осталось {count}L", reply_markup=markup)
    elif CheckAccount(message):
        markup.add(button2)
        count = howMutchIsTheFish()
        await message.answer(f"Пс, парень! Не хочешь не много заправиться?\n "
                             f"до конца недели осталось {count}L", reply_markup=markup)
    else:
        button = knopkaADDaccount(message.chat.id, message.chat.username)
        await message.answer(f"доброе утро\nА потом мопед заправим.")
        await bot.send_message(id_gosha, f"Кто-то с ником @{message.chat.username} хочет топлива\n"
                                         f"Вот его ID {message.chat.id}", reply_markup=button)


def knopkaADDaccount(id, username):  #создает кнопку с id записи
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f'Добавить @{username} в клуб?', callback_data=cb.new(id=id, username=username))]
        ]
    )


@dispatcher.callback_query_handler(cb.filter())  #возвращает номер открытой сделки и открывает строчку в таблице
async def button_hendler(query: types.CallbackQuery, callback_data: dict):
    username = callback_data.get('username')
    id = callback_data.get("id")
    addAccountSQL(username, id)
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("Выдать QR", callback_data="GiveQR")
    markup.add(button2)
    await bot.send_message(id, "Поздравляю, тебе доступны QR кодя для заправки, недельный лимит 8 литров",
                           reply_markup=markup)
    await bot.send_message(id_gosha, "Добавлено")




@dispatcher.callback_query_handler(lambda c: c.data == "newWeekStart")
async def giveQR(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("Выдать QR", callback_data="GiveQR")
    markup.add(button2)
    nullCount()
    await bot.send_message(call.message.chat.id, "Все qr обнулились", reply_markup=markup)


@dispatcher.callback_query_handler(lambda c: c.data == "Kosiak")
async def kosiak(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("Выдать QR", callback_data="GiveQR")
    markup.add(button2)
    kosyakus(name)
    await bot.send_message(call.message.chat.id, "QR помечен не рабочим", reply_markup=markup)


@dispatcher.callback_query_handler(lambda c: c.data == "GiveQR")  #даёт qr
async def giveQR(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Заправился, спасибо)", callback_data="sushi")
    button2 = InlineKeyboardButton("QR не работает", callback_data="Kosiak")
    markup.add(button1, button2)
    try:
        global name
        name = giveFreshQR()
        photo = open(f"{name}", "rb")
        changeCount('0', name)
        await bot.send_photo(call.message.chat.id, photo=photo, reply_markup=markup)
        await bot.answer_callback_query(call.id)
    except:
        await bot.send_message(call.message.chat.id, "Топливо на неделю кончилось")


@dispatcher.callback_query_handler(text='sushi')  #удаляет сообщение
async def clearMessage(callback_query: types.CallbackQuery):
    await callback_query.message.delete()


@dispatcher.message_handler(content_types=['photo'])  #грузит фото
async def get_photo(message: types.Message):
    if message.chat.id in id_dopusk:
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
