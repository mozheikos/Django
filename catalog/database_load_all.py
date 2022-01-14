import csv
import os
import sqlite3

conn = sqlite3.connect("./db.sqlite3")
cursor = conn.cursor()


def data_load(table_name):
    with open(f"./catalog/{table_name}.csv", newline="") as f:
        reader = csv.DictReader(f)
        cursor.execute(f"delete from {table_name}")
        for row in reader:
            header = tuple(row.keys())
            content = tuple(row.values())
            sql = f"insert into {table_name} {header} values {content}"
            cursor.execute(sql)
            conn.commit()


def main():
    path = os.path.join(os.getcwd(), "catalog")
    directory_content = os.listdir(path)
    for i in directory_content:
        if i.split(".")[1] == "csv":
            data_load(i.split(".")[0])


if __name__ == "__main__":
    main()
