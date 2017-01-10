from db import DB
db = DB()
cursor=db.conn.cursor()

print cursor.execute("SELECT password FROM players where name='netease'")
print cursor.fetchone()
