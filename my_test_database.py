"""
Модуль Работы с Базой Данных
"""
import sqlite3 as sq


DATABASE = 'DATABASE.db'
NAME_BOT = 'Trades'
USERNAME_BOT = 'Trades_mm_bot'

def get_token():
    with sq.connect(DATABASE) as connect:
        # connect.row_factory = sq.Row
        curs = connect.cursor()
        curs.execute(f"SELECT token FROM Tokens WHERE username IS '{USERNAME_BOT}'")
        return curs.fetchone()[0]


if __name__ == '__main__':

    print(get_token())

