import sqlite3
import sys
import json
import time


class DB:
    def __init__(self):
        try:
            self.sqliteConnector = sqlite3.connect("user_data.db")
            self.cursor = self.sqliteConnector.cursor()

            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS user_data(
            NAME TEXT PRIMARY KEY,
            TEMP REAL,
            VANITY INTEGER,
                CONDITION TEXT,
            UV_INDEX REAL,
            HUMIDITY REAL,
            CALORIES REAL,
            STEPS INTEGER,
            DISTANCE_WALKED REAL,
            HEART REAL,
            LASTUPDATE REAL

            );"""
            )
            self.cursor.execute("SELECT * FROM user_data WHERE NAME = 'Default'")
            existing_entry = self.cursor.fetchone()

            if existing_entry is None:
                # ID 0 does not exist, so insert the new entry
                new_entry = (
                    "Default",
                    75,
                )  # Replace 'Your data here' with your actual data
                self.cursor.execute(
                    "INSERT INTO user_data(NAME,VANITY) VALUES (?, ?)",
                    new_entry,
                )

            # self.cursor.execute("SELECT * FROM user_data WHERE NAME='User1'")
            # existing_entry = self.cursor.fetchone()

            # if existing_entry is None:
            #     new_entry = (
            #         "User1",
            #         100,
            #     )  # Replace 'Your data here' with your actual data
            #     self.cursor.execute(
            #         "INSERT INTO user_data(NAME,VANITY) VALUES (?,?)",
            #         new_entry,
            #     )

            self.sqliteConnector.commit()
            self.fields = [
                "NAME",
                "TEMP",
                "VANITY",
                "CONDITION",
                "UV_INDEX",
                "HUMIDITY",
                "CALORIES",
                "STEPS",
                "DISTANCE_WALKED",
                "HEART",
                "LASTUPDATE",
            ]
            self.link = [0, 1, 3, 4, 5, 6, 7, 8, 9]
        except sqlite3.Error as error:
            print(f"Error occured: {error}")
            sys.exit(1)

    def addUser(self, name):
        sqliteConnector = sqlite3.connect("user_data.db")
        cursor = self.sqliteConnector.cursor()
        cursor.execute(
            "INSERT INTO user_data(NAME) VALUES (?)",
            name,
        )

        sqliteConnector.commit()

    def getUserData(self, name):

        sqliteConnector = sqlite3.connect("user_data.db")
        cursor = sqliteConnector.cursor()
        cnt = cursor.execute(f"SELECT * from user_data WHERE NAME='{name}'")
        columns = [column[0] for column in cnt.description]
        out = cnt.fetchone()

        sqliteConnector.close()
        json_data = []
        row_data = {}
        for i in range(len(columns)):
            row_data[columns[i]] = out[i]
        json_data.append(row_data)
        return json.dumps(json_data)

    def updateUserData(self, updates):
        # updates = (name, temp, van)
        sqliteConnector = sqlite3.connect("user_data.db")
        cursor = sqliteConnector.cursor()
        for field in range(1, len(self.fields)):
            newfield = field
            if field == (len(self.fields) - 1):
                continue
            #    cursor.execute(
            #   f"UPDATE user_data SET {self.fields[field]}='{time.time()}' WHERE NAME='{updates[0]}';"
            # )
            if field == 2:
                continue
            if field > 2:
                newfield -= 1
            if updates[newfield] == None:
                continue
            cursor.execute(
                f"UPDATE user_data SET {self.fields[field]}='{updates[newfield]}' WHERE NAME='{updates[0]}';"
            )
        sqliteConnector.commit()
        sqliteConnector.close()

    def id_exists(self, id):
        sqliteConnector = sqlite3.connect("user_data.db")
        cursor = sqliteConnector.cursor()
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM user_data WHERE NAME = ?)", (id,))
        exists = cursor.fetchone()[0]
        return bool(exists)

    def getUserVanity(self, name):

        sqliteConnector = sqlite3.connect("user_data.db")
        cursor = sqliteConnector.cursor()
        out = cursor.execute(
            f"SELECT VANITY from user_data WHERE NAME='{name}'"
        ).fetchone()
        sqliteConnector.close()
        return out[0]
