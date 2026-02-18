import random
from db.database import get_connection

def get_random_ayah():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM ayat WHERE used=0")
    rows = cur.fetchall()

    if not rows:
        cur.execute("UPDATE ayat SET used=0")
        conn.commit()
        cur.execute("SELECT * FROM ayat")
        rows = cur.fetchall()

    ayah = random.choice(rows)
    cur.execute("UPDATE ayat SET used=1 WHERE id=?", (ayah["id"],))
    conn.commit()
    conn.close()

    return dict(ayah)