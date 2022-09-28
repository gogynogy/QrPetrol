import os
from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from config import TOKEN
from sql import SQL as SQL3

if not os.path.exists("QrCode"):
    os.mkdir("QrCode")
os.chdir("QrCode")


SQL = SQL3()

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot)
cb = CallbackData('action', 'username', 'id')


id_lesha = 243626777
id_gosha = 498332094
id_dopusk = (id_gosha, id_lesha)


@dispatcher.message_handler(commands=["start"])  # /start command processing
async def begin(message: types.Message):
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Обнулить все QR", callback_data="newWeekStart")
    button2 = InlineKeyboardButton("Выдать QR", callback_data="GiveQR")
    button3 = InlineKeyboardButton("Выдать QR", callback_data="GiveQRclient")
    if message.chat.id in id_dopusk:
        markup.add(button1, button2)
        await message.answer(f"Пс! Хочешь не много горючки?\n"
                             f"до конца недели осталось {SQL.howMutchIsTheFish()}L", reply_markup=markup)
    elif SQL.CheckAccount(message):
        markup.add(button3)
        count = SQL.howMutchIsTheFishClient(message.chat.id)
        await message.answer(f"Пс! Хочешь не много горючки?\n"
                             f"до конца недели осталось {count}L", reply_markup=markup)
    else:
        button = knopkaADDaccount(message.chat.id, message.chat.username)
        await message.answer(f"доброе утро\nА потом мопед заправим.")
        await bot.send_message(id_gosha, f"Кто-то с ником @{message.chat.username} хочет топлива\n"
                                         f"Вот его ID {message.chat.id}", reply_markup=button)


def knopkaADDaccount(id, username):  # Creates a button with the record id
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f'Добавить @{username} в клуб?', callback_data=cb.new(id=id, username=username))]
        ]
    )


@dispatcher.callback_query_handler(cb.filter())  # adds the account to the table
async def button_hendler(query: types.CallbackQuery, callback_data: dict):
    username = callback_data.get('username')
    id = callback_data.get("id")
    SQL.addAccountSQL(username, id)
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
    SQL.nullCount()
    await bot.send_message(call.message.chat.id, "Все qr обнулились", reply_markup=markup)


@dispatcher.callback_query_handler(lambda c: c.data == "Kosiak")
async def kosiak(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("Выдать QR", callback_data="GiveQR")
    markup.add(button2)
    SQL.kosyakus(name)
    await bot.send_message(call.message.chat.id, "QR помечен не рабочим", reply_markup=markup)


@dispatcher.callback_query_handler(lambda c: c.data == "GiveQR")  #даёт qr
async def giveQR(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Заправился, спасибо)", callback_data="sushi")
    button2 = InlineKeyboardButton("QR не работает", callback_data="Kosiak")
    markup.add(button1, button2)
    try:
        global name
        name = SQL.giveFreshQR()
        photo = open(f"{name}", "rb")
        SQL.changeCount('0', name)
        await bot.send_photo(call.message.chat.id, photo=photo, reply_markup=markup)
        await bot.answer_callback_query(call.id)
    except:
        await bot.send_message(call.message.chat.id, "Топливо на неделю кончилось")


@dispatcher.callback_query_handler(lambda c: c.data == "GiveQRclient")  #даёт qr
async def giveQRclient(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Заправился, спасибо)", callback_data="sushi")
    button2 = InlineKeyboardButton("QR не работает", callback_data="Kosiak")
    markup.add(button1, button2)
    try:
        global name
        name = SQL.giveFreshQR()
        photo = open(f"{name}", "rb")
        SQL.changeCountClient(call.message.chat.id)
        await bot.send_photo(call.message.chat.id, photo=photo, reply_markup=markup)
        await bot.answer_callback_query(call.id)
    except:
        await bot.send_message(call.message.chat.id, "Топливо на неделю кончилось")


@dispatcher.callback_query_handler(text='sushi')  # deletes the message
async def clearMessage(callback_query: types.CallbackQuery):
    await callback_query.message.delete()


@dispatcher.message_handler(content_types=['photo'])  # uploads photos
async def get_photo(message: types.Message):
    if message.chat.id in id_dopusk:
        if SQL.addSQL(message):
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
