import sqlite3
import sys
import json


class DB:
    def __init__(self):
        try:
            sqliteConnector = sqlite3.connect("user_data.db")
            self.cursor = sqliteConnector.cursor()

            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS user_data(
                ID INTEGER PRIMARY KEY,
            NAME TEXT NOT NULL,
            TEMP REAL,
            VANITY INTEGER
                            

            );"""
            )
            self.fields = ["NAME", "TEMP", "VANITY"]
        except sqlite3.Error as error:
            print(f"Error occured: {error}")
            sys.exit(1)

    def getUserData(self, id):
        cnt = self.cursor.execute(f"SELECT * from user_data WHERE ID='{id}'")

        columns = [column[0] for column in cnt.description]
        out = cnt.fetchone()

        json_data = []
        row_data = {}
        for i in range(len(columns)):
            row_data[columns[i]] = out[i]
        json_data.append(row_data)
        return json.dumps(json_data)

    def updateUserData(self, id, name, temp, van):
        updates=(name,temp,van)
        for field in range(len(self.fields)):
            if updates[field]==None:
                continue
            self.cursor.execute(f"UPDATE Book SET {self.fields[field]}='{updates[field]}' WHERE ID={id};")

    def getUserVanity(self,id):
        out = self.cursor.execute(f"SELECT VANITY from user_data WHERE ID={id}").fetchone()
        return out

