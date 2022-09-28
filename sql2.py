import sqlite3

class SQL:
    def __init__(self, db_file):
        """Initializing Database Connection"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def createFirstTable(self):
        """Creating First Table"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `QRPetrol` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            qrname TEXT,
            kolichestvo int NOT NULL DEFAULT 4,
            kosiak int NOT NULL DEFAULT 0
            )""")
        self.conn.commit()

    def createSecondTable(self):
        """Creating Second Table"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `accounts` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TelegramNikName TEXT,
            IDTelegram TEXT,
            OstalosL int NOT NULL DEFAULT 8
            )""")
        self.conn.commit()

    def giveFreshQR(self):
        """gives out a code with fuel"""
        self.cursor.execute("SELECT qrname FROM QRPetrol WHERE kolichestvo = ?", ("4",))
        name = self.cursor.fetchone()
        return name[0]


    def addSQL(self, message):
        """checks if the photo exists in the database and adds"""
        name = message.photo[0].file_unique_id + ".jpeg"
        try:
            self.cursor.execute("SELECT qrname FROM QRPetrol WHERE qrname = (?)", (name,))
            data = self.cursor.fetchone()
            if data is None:
                self.cursor.execute(f"INSERT INTO QRPetrol (qrname) VALUES (?)", (name,))
                return True
            else:
                return False
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite addSQL", error)

    def changeCount(self, num, id):
        """changes the amount of fuel in the remainder"""
        try:
            self.cursor.execute('''UPDATE QRPetrol SET kolichestvo = ? WHERE qrname = ?''', (num, id))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite changeCount", error)

    def changeCountClient(self, id):
        """changes the amount of fuel on the client's balance"""
        try:
            self.cursor.execute('''UPDATE accounts SET OstalosL = (OstalosL -4) WHERE IDTelegram = ?''', (id,))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite changeCountClient", error)

    def kosyakus(self, id):
        """changes the number of joints on the map"""
        try:
            self.cursor.execute('''UPDATE QRPetrol SET kosiak = (kosiak + 1) WHERE qrname = ?''', (id,))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite kosyakus", error)

    def nullCount(self):
        """zeroes in on fuel for the week"""
        try:
            self.cursor.execute('''UPDATE QRPetrol SET kolichestvo = 4''')
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite nullCount", error)

    def howMutchIsTheFish(self):
        """counts the fuel balance"""
        print("Ошибка")
        try:
            self.cursor.execute(f"""SELECT SUM(kolichestvo) FROM `QRPetrol`""")
            print("Ошибка")
            result = self.cursor.fetchone()[0]
            print("Ошибка")
            return result
            print(self.cursor.fetchone()[0])
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite howMutchIsTheFish", error)

    def howMutchIsTheFishClient(self, id):
        """counts the fuel balance"""
        try:
            self.cursor.execute(f"""SELECT SUM(OstalosL) FROM `accounts` WHERE IDTelegram = ?""", (id,))
            return self.cursor.fetchone()[0]
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite howMutchIsTheFishClient", error)

    def CheckAccount(self, message):
        """checks if the id exists in the database"""
        try:
            self.cursor.execute("SELECT IDTelegram FROM accounts WHERE IDTelegram = (?)", (message.chat.id,))
            if self.cursor.fetchone() is None:
                return False
            else:
                return True
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite addSQL", error)

    def addAccountSQL(self, username, id):
        """checks if the photo exists in the database and adds"""
        try:
            self.cursor.execute(f"INSERT INTO accounts (TelegramNikName, IDTelegram) VALUES (?, ?)", (username, id))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite addSQL", error)

    def nullCountPetrol(self):
        """zeroes in on fuel for the week"""
        try:
            self.cursor.execute('''UPDATE QRPetrol SET kolichestvo = 4''')
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite nullCount", error)

    def close(self):
        self.conn.close()