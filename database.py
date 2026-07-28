import sqlite3


DB = "photos.db"


def init_db():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        photo TEXT NOT NULL,
        lang TEXT DEFAULT 'en'
    )
    """)

    conn.commit()
    conn.close()



def add_photo(user_id, photo, lang):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO photos(user_id, photo, lang)
        VALUES (?, ?, ?)
        """,
        (user_id, photo, lang)
    )

    conn.commit()
    conn.close()



def get_match(user_id):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, user_id, photo, lang
        FROM photos
        WHERE user_id != ?
        ORDER BY RANDOM()
        LIMIT 1
        """,
        (user_id,)
    )

    result = cur.fetchone()

    conn.close()

    return result



def delete_photo(photo_id):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM photos WHERE id=?",
        (photo_id,)
    )

    conn.commit()
    conn.close()
