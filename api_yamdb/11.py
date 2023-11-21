import sqlite3

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
cur.execute("DROP TABLE reviews_title;")

con.commit()
con.close()