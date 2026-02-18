from db.database import get_connection
import random

def get_zikr(time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT text FROM azkar WHERE type=?", (time,))
    rows = cur.fetchall()
    conn.close()
    return random.choice(rows)["text"]