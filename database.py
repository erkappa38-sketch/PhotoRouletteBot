import sqlite3


DB = "photos.db"


def connect():
    return sqlite3.connect(DB)



def init_db():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS challenges (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        creator_id INTEGER NOT NULL,

        original_photo TEXT NOT NULL,

        challenger_id INTEGER,

        reply_photo TEXT,

        status TEXT DEFAULT 'waiting'

    )
    """)

    conn.commit()
    conn.close()



# salva la foto iniziale della sfida

def add_challenge(
    creator_id,
    photo_id
):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO challenges
        (
            creator_id,
            original_photo
        )

        VALUES (?,?)
        """,
        (
            creator_id,
            photo_id
        )
    )

    conn.commit()
    conn.close()



# cerca una sfida disponibile

def find_challenge(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            creator_id,
            original_photo

        FROM challenges

        WHERE status='waiting'
        AND creator_id != ?

        ORDER BY RANDOM()

        LIMIT 1
        """,
        (user_id,)
    )


    result = cur.fetchone()

    conn.close()

    return result



# assegna la sfida a un utente

def assign_challenge(
    challenge_id,
    challenger_id
):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE challenges

        SET challenger_id=?,
            status='playing'

        WHERE id=?

        """,
        (
            challenger_id,
            challenge_id
        )
    )

    conn.commit()
    conn.close()



# salva la foto risposta

def save_reply(
    user_id,
    photo_id
):

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        UPDATE challenges

        SET reply_photo=?,
            status='completed'

        WHERE challenger_id=?

        """,
        (
            photo_id,
            user_id
        )
    )


    conn.commit()
    conn.close()



# recupera la sfida completa

def get_completed(
    user_id
):

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        SELECT

        creator_id,
        original_photo,
        reply_photo

        FROM challenges

        WHERE challenger_id=?

        AND status='completed'

        ORDER BY id DESC

        LIMIT 1

        """,
        (user_id,)
    )


    result = cur.fetchone()

    conn.close()

    return result
