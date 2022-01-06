import sqlite3
import csv
import os

# conn = sqlite3.connect("./db.sqlite3")
# cursor = conn.cursor()
import sys

DB_PATH = './db.sqlite3'


class DatabaseConnection:

    def __init__(self, db_path):
        self.db_path = db_path

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        return isinstance(exc_val, TypeError)


def data_load(table_name):
    with open(f'./catalog/{table_name}.csv', newline='') as f:
        reader = csv.DictReader(f)
        with DatabaseConnection(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(f'delete from {table_name}')
            for row in reader:
                header = tuple(row.keys())
                content = tuple(row.values())
                sql = f"insert into {table_name} {header} values {content}"
                cursor.execute(sql)
                connection.commit()


def data_dump(table_name):
    with DatabaseConnection(DB_PATH) as connection:
        cursor = connection.cursor()
        sql = f'select * from {table_name}'
        cursor.execute(sql)
        headers = list(cursor.description)
        for i in range(len(headers)):
            headers[i] = headers[i][0]
        data_set = cursor.fetchall()
        with open(f'catalog/{table_name}.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for item in data_set:
                dictionary = dict(zip(headers, item))
                writer.writerow(dictionary)


def load():
    path = os.path.join(os.getcwd(), 'catalog')
    directory_content = os.listdir(path)
    for i in directory_content:
        if i.split('.')[1] == 'csv':
            data_load(i.split('.')[0])


def dump():
    with DatabaseConnection(DB_PATH) as connection:
        cursor = connection.cursor()
        sql = 'select name from sqlite_master where type = "table" and name like "mainapp_%" or ' \
              'name = "authnapp_shopuser"'
        cursor.execute(sql)
        table_list = cursor.fetchall()
        for table in table_list:
            table = table[0]
            data_dump(table)


__name__ = sys.argv[0]
command = sys.argv[1]

if command == 'dump':
    dump()
elif command == 'load':
    load()


if __name__ == '__main__':
    while True:
        user_choose = input('Выберите действие (1 - выгрузить базу в файлы, 2 - загрузить в базу из файлов,'
                            ' 0 - выход): ')
        if user_choose == '1':
            dump()

        elif user_choose == '2':
            load()

        elif user_choose == '0':
            exit(0)

        else:
            print('Неправильный аргумент')