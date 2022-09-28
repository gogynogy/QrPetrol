import sqlite3

class SQL:

    def __init__(self):
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
            OstalosL int NOT NULL DEFAULT 8
            )"""
            sql.executescript(table)
    def giveFreshQR(self):
        with sqlite3.connect("Petrol.db") as QrPetrol:
            sql = QrPetrol.cursor()
            sql.execute("SELECT qrname FROM QRPetrol WHERE kolichestvo = ?", ("4",))
            name = sql.fetchone()
            return name[0]

    def addSQL(self, message):  # checks if the photo exists in the database and adds
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

    def changeCount(self, num, id):  # changes the amount of fuel in the remainder
        try:
            with sqlite3.connect("Petrol.db") as QrPetrol:
                sql = QrPetrol.cursor()
                sql.execute('''UPDATE QRPetrol SET kolichestvo = ? WHERE qrname = ?''', (num, id))
                QrPetrol.commit()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite changeCount", error)

    def changeCountClient(self, id):  # changes the amount of fuel on the client's balance
        try:
            with sqlite3.connect("Petrol.db") as QrPetrol:
                sql = QrPetrol.cursor()
                sql.execute('''UPDATE accounts SET OstalosL = (OstalosL -4) WHERE IDTelegram = ?''', (id,))
                QrPetrol.commit()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite changeCountClient", error)

    def kosyakus(self, id):  # changes the number of joints on the map
        try:
            with sqlite3.connect("Petrol.db") as QrPetrol:
                sql = QrPetrol.cursor()
                sql.execute('''UPDATE QRPetrol SET kosiak = (kosiak + 1) WHERE qrname = ?''', (id,))
                QrPetrol.commit()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite kosyakus", error)

    def nullCount(self):  # zeroes in on fuel for the week
        try:
            with sqlite3.connect("Petrol.db") as QrPetrol:
                sql = QrPetrol.cursor()
                sql.execute('''UPDATE QRPetrol SET kolichestvo = 4''')
                QrPetrol.commit()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite nullCount", error)

    def howMutchIsTheFish(self):  # counts the fuel balance
        try:
            with sqlite3.connect("Petrol.db") as QrPetrol:
                sql = QrPetrol.cursor()
                sql.execute(f"""SELECT SUM(kolichestvo) FROM `QRPetrol`""")
                result = sql.fetchone()[0]
                return result
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite howMutchIsTheFish", error)

    def howMutchIsTheFishClient(self, id):  # counts the fuel balance
        try:
            with sqlite3.connect("Petrol.db") as QrPetrol:
                sql = QrPetrol.cursor()
                sql.execute(f"""SELECT SUM(OstalosL) FROM `accounts` WHERE IDTelegram = ?""", (id,))
                result = sql.fetchone()[0]
                return result
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite howMutchIsTheFishClient", error)

    def CheckAccount(self, message):  # checks if the id exists in the database
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

    def addAccountSQL(self, username, id):  # checks if the photo exists in the database and adds
        try:
            with sqlite3.connect("Petrol.db") as QrPetrol:
                sql = QrPetrol.cursor()
                sql.execute(f"INSERT INTO accounts (TelegramNikName, IDTelegram) VALUES (?, ?)", (username, id))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite addSQL", error)

    def nullCount(self):  # zeroes in on fuel for the week
        try:
            with sqlite3.connect("Petrol.db") as QrPetrol:
                sql = QrPetrol.cursor()
                sql.execute('''UPDATE QRPetrol SET kolichestvo = 4''')
                QrPetrol.commit()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite nullCount", error)

