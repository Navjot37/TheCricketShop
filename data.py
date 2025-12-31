import sqlite3
import json

con = sqlite3.connect("shopping.db")
cur = con.cursor()

cur.execute("SELECT id, product_title, price, img1 FROM products;")
col = [desc[0] for desc in cur.description]
rows = cur.fetchall()

data = [dict(zip(col, row)) for row in rows ]

with open("ProductsAll.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

con.close()
print("done")
