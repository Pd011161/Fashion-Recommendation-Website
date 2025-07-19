import sqlite3


# def db_query(sql, params):
#     conn = sqlite3.connect("/Users/Aksorn_AI/Desktop/RECOMENTATION_SYSTEM/backend/database/database.db")
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     cur.execute(sql, params)
#     row = cur.fetchone()
#     conn.close()
#     if row:
#         return dict(row)
#     return None


def db_query(sql, params=()):
    conn = sqlite3.connect("/Users/Aksorn_AI/Desktop/RECOMENTATION_SYSTEM/backend/database/database.db")
    conn.row_factory = sqlite3.Row   # <<<< สำคัญมาก!
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    return [dict(row) for row in rows]
