import sqlite3

class Database(sqlite3.connect):
    
    def __init__(self):
        super.__init__("scheduler.db")
        self.cur = self.cursor()
        self.cur.execute("CREATE TABLE leagues(league id, name, time slots, group)")