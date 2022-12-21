import sqlite3


class DataBase:
    def __init__(self, name='cd_catalog.db'):
        self.db = sqlite3.connect(f"{name}")
        cur = self.db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS CDs (
            CD_ID integer primary key,
            CD_Name TEXT,
            CD_Description TEXT,
            CD_Genre TEXT,
            CD_Publisher TEXT
            )
        """)
        cur.execute("""CREATE TABLE IF NOT EXISTS Debtors (
            Debtor_ID integer primary key,
            Debtor_Name TEXT,
            Debtor_Date TEXT,
            CD_ID INT
            )
       """)

        self.db.commit()
        cur.close()

    def get_from_cds(self):
        cur = self.db.cursor()
        cur.execute("""SELECT * FROM CDs""")
        records = cur.fetchall()
        cur.close()
        return records

    def get_from_debtors(self):
        cur = self.db.cursor()
        cur.execute("""SELECT * FROM Debtors""")
        records = cur.fetchall()
        cur.close()
        return records

    def get_cds(self):  # Данные для комбобокса
        cur = self.db.cursor()
        cur.execute("""SELECT CD_ID, CD_Name FROM CDs""")
        records = cur.fetchall()
        l = []
        for i in records:
            l.append(str(i[0])+' '+i[1])
        cur.close()
        return l

    def add_in_cds(self, name, description, genre, publisher):
        cur = self.db.cursor()
        cur.execute("INSERT INTO CDs VALUES (NULL, ?, ?, ?, ?)", (name, description, genre, publisher))
        self.db.commit()
        cur.close()

    def add_in_debtors(self, name, date, cd_id):
        cd_id = int(cd_id)
        cur = self.db.cursor()
        cur.execute("INSERT INTO Debtors VALUES (NULL, ?, ?, ?)", (name, date, cd_id))
        self.db.commit()
        cur.close()

    def delete_from_cds(self, id):
        cur = self.db.cursor()
        cur.execute(f"""DELETE from CDs WHERE CD_ID={id}""")
        cur.execute(f"""SELECT COUNT(Debtor_ID) FROM Debtors WHERE CD_ID={id}""")
        records = cur.fetchall()
        for i in range(records[0][0]):
            self.delete_from_debtors2(id)
        self.db.commit()
        cur.close()

    def delete_from_debtors2(self, id):
        id = int(id)
        cur = self.db.cursor()
        cur.execute(f"""DELETE from Debtors WHERE CD_ID={id}""")
        self.db.commit()
        cur.close()

    def delete_from_debtors(self, id):
        id = int(id)
        cur = self.db.cursor()
        cur.execute(f"""DELETE from Debtors WHERE Debtor_ID={id}""")
        self.db.commit()
        cur.close()

    def update_cds(self, id, name, description, genre, publisher):
        id = int(id)
        cur = self.db.cursor()
        cur.execute(f""" UPDATE CDs set CD_Name="{name}", CD_Description="{description}", CD_Genre="{genre}", CD_Publisher="{publisher}"  WHERE CD_ID={id}""")
        self.db.commit()
        cur.close()

    def update_debtors(self, id, name, date, cd_id):
        id = int(id)
        cd_id = int(cd_id)
        cur = self.db.cursor()
        cur.execute(f""" UPDATE Debtors set Debtor_Name="{name}", Debtor_Date="{date}", CD_ID={cd_id} WHERE Debtor_ID={id}""")
        self.db.commit()
        cur.close()


if __name__ == "__main__":
    db = DataBase()
    rec = db.get_from_cds()
    print(rec)
