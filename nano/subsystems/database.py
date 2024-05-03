import sqlite3
import sys
import json
import time


class DB:
    # Database class initializer
    def __init__(self):
        try:
            # creating or opening database file and connecting to it 
            self.sqliteConnector = sqlite3.connect("user_data.db")
            self.cursor = self.sqliteConnector.cursor()

            # creating table if it doesn't exist in our database file keyed on Name
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
            INDOORTEMP REAL,
            LASTUPDATE REAL

            );"""
            )
            # Creating a default user that has defailt vanity light strength value
            self.cursor.execute("SELECT * FROM user_data WHERE NAME = 'Default'")
            existing_entry = self.cursor.fetchone()

            if existing_entry is None:
                new_entry = (
                    "Default",
                    75,
                )  
                self.cursor.execute(
                    "INSERT INTO user_data(NAME,VANITY) VALUES (?, ?)",
                    new_entry,
                )

            # saving current status
            self.sqliteConnector.commit()
            self.fields = [
                "NAME",
                "TEMP",
                "CONDITION",
                "UV_INDEX",
                "HUMIDITY",
                "CALORIES",
                "STEPS",
                "DISTANCE_WALKED",
                "HEART",
                "VANITY",
                "INDOORTEMP",
            ]
        except sqlite3.Error as error:
            print(f"Error occured: {error}")
            sys.exit(1)

    # adds a user to database
    def addUser(self, name):
        sqliteConnector = sqlite3.connect("user_data.db")
        cursor = sqliteConnector.cursor()
        cursor.execute(
            "INSERT INTO user_data(NAME) VALUES (?)",
           ( name,)
        )

        sqliteConnector.commit()

    # pulls userdata of user from database and returns as jsonstring and json object
    def getUserData(self, name):

        sqliteConnector = sqlite3.connect("user_data.db")
        cursor = sqliteConnector.cursor()
        cnt = cursor.execute(f"SELECT * from user_data WHERE NAME='{name}'")
        columns = [column[0] for column in cnt.description]
        out = cnt.fetchone()

        sqliteConnector.close()
        json_data = []
        row_data = {}
        print(columns)
        print(out)
        if out is not None:
            for i in range(len(columns)):
                row_data[columns[i]] = out[i]
            json_data.append(row_data)
            return json.dumps(json_data),row_data

    # updates user in database for each of the fields if the field has a value to update
    def updateUserData(self, updates):
        sqliteConnector = sqlite3.connect("user_data.db")
        cursor = sqliteConnector.cursor()
        for field in range(1, len(self.fields)):
          
            if updates[field] == None:
                continue
            cursor.execute(
                f"UPDATE user_data SET {self.fields[field]}='{updates[field]}' WHERE NAME='{updates[0]}';"
            )
        sqliteConnector.commit() #saves database
        sqliteConnector.close()

    # checks to see if an user exists
    def id_exists(self, id):
        sqliteConnector = sqlite3.connect("user_data.db")
        cursor = sqliteConnector.cursor()
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM user_data WHERE NAME = ?)", (id,))
        exists = cursor.fetchone()[0]
        return bool(exists)

    # get the vanity strength of a specific user
    def getUserVanity(self, name):

        sqliteConnector = sqlite3.connect("user_data.db")
        cursor = sqliteConnector.cursor()
        out = cursor.execute(
            f"SELECT VANITY from user_data WHERE NAME='{name}'"
        ).fetchone()
        sqliteConnector.close()
        return out[0]
