import datetime
import sqlite3


class SQLite:
    def __init__(self):
        self.conn = sqlite3.connect("data/backs.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_db(self) -> None:
        """创建数据库"""
        self.cursor.execute("""create table if not exists
            SMBC(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount VARCHAR(128),
            balance VARCHAR(128),
            comment VARCHAR(128),
            update_time TIMESTAMP)
            """
        )
        self.cursor.execute("""create table if not exists
            MUFG(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount VARCHAR(128),
            balance VARCHAR(128),
            comment VARCHAR(128),
            update_time TIMESTAMP)
            """
        )
        self.conn.commit()
    
    def insert(self, table: str, amount: str, balance: str, comment: str) -> None:
        """插入数据"""
        self.cursor.execute(f"INSERT INTO {table} (amount, balance, comment, update_time) VALUES (?, ?, ?, ?)",
                            (amount, balance, comment, int(datetime.datetime.now().timestamp())))
        self.conn.commit()

    def select(self, table: str) -> str:
        """查询最新余额"""
        data = self.cursor.execute(f"SELECT balance FROM {table} ORDER BY id DESC LIMIT 1").fetchone()
        if data:
            return data[0]
        return ""
    
    def close(self):
        self.conn.close()

sql = SQLite()