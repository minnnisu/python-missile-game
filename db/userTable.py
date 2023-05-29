import sqlite3
from enum import Enum

class UserField(Enum):
    ID = 0
    NAME = 1
    SCORE = 2
    TIMESTAMP = 3

class UserTable:
    def __init__(self):
        self.conn = sqlite3.connect('db/missileGame.db') 

    def createTable(self):
        self.conn.execute('''CREATE TABLE USER
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            NAME TEXT UNIQUE NOT NULL,
                            SCORE TEXT NOT NULL,
                            DATETIME DEFAULT CURRENT_TIMESTAMP);''') 
        print("Table created successfully")
        
    def insertUser(self, user):
        self.conn.execute(f"INSERT INTO USER (NAME,SCORE) VALUES ('{user.username}', '{str(user.fireCount)}')")
        self.conn.commit()
        print("Record created successfully")
        
    def updateUser(self, user):
        self.conn.execute(f"UPDATE USER set SCORE='{str(user.fireCount)}' where NAME = '{user.username}'")
        self.conn.commit()
        print("Record updated successfully")
        
    def selectUser(self, user=None, isOneUser=False):
        query = ""
        
        if(isOneUser): 
            query = f"SELECT ID,NAME,SCORE,DATETIME from USER where NAME = '{user.username}'" # query only specific user
        else:
            query = "SELECT ID,NAME,SCORE,DATETIME from USER" # qeury all users
            
        cursor = self.conn.execute(query)
        users = []
        for row in cursor:
            user = {"id": row[UserField['ID'].value], "name": row[UserField['NAME'].value], 
                    "score": row[UserField['SCORE'].value], "timestamp": row[UserField['TIMESTAMP'].value]}
            users.append(user)
        return users
            
# userTable = UserTable()
# userTable.createTable()