import sqlite3
import csv

conn = sqlite3.connect("./db.sqlite3")
cursor = conn.cursor()


def data_dump(table_name):
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


def main():
    cursor.execute(
        'select name from sqlite_master where type = "table" and name like "mainapp_%" or name = "authnapp_shopuser"')
    table_list = cursor.fetchall()
    for table in table_list:
        table = table[0]
        data_dump(table)


if __name__ == '__main__':
    main()
