## Проверка на Число (только на целое если float - то через try:)
# data = '3456.dd'
# num = data.split('.')[0]
# print(num.isnumeric())
# print(num.isdigit())
# print(num.isdecimal())
# print(float(data).isdecimal())

## Открыть JSON Файл -------------------
# import json
# path_file_cenz = r'common/cenz.json'
# # cenzored_words = set(json.load(open(path_file_cenz)))
# cenzored_words = set(json.load(open(path_file_cenz))).intersection()
# print(cenzored_words)

## Свой вариант пробовал через БД ------------------
# import sqlite3 as sq
# DATABASE = 'DATABASE.db'
# NAME_BOT = 'Trades'
# USERNAME_BOT = 'Trades_mm_bot'#
# def get_token():
#     with sq.connect(DATABASE) as connect:
#         # connect.row_factory = sq.Row
#         curs = connect.cursor()
#         curs.execute(f"SELECT token FROM Tokens WHERE username IS '{USERNAME_BOT}'")
#         return curs.fetchone()[0]
# if __name__ == '__main__':#
#     print(get_token())



