import sqlite3

conn = sqlite3.connect("/home/stanislav/djangoBasics/geekshop/db.sqlite3")
cursor = conn.cursor()
cursor.execute("DELETE FROM mainapp_category")
with open("categorys.txt", "r") as f:
    while True:
        row = f.readline().rstrip()
        insert = tuple(row.split(","))
        if row != "":
            sql = f"INSERT INTO mainapp_category (id, title, description) VALUES {insert}"
            cursor.execute(sql)
            conn.commit()
        else:
            break

cursor.execute("DELETE FROM mainapp_product")
with open("items.txt", "r") as f:
    while True:
        row = f.readline().rstrip()
        insert = tuple(row.split(","))
        if row != "":
            sql = (
                f"INSERT INTO mainapp_product (id, name, image, short_desc, description, price, count, category_id)"
                f" VALUES {insert}"
            )
            cursor.execute(sql)
            conn.commit()
        else:
            break
