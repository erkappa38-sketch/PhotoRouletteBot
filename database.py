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




def add_challenge(
    user_id,
    photo
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
            user_id,
            photo
        )
    )


    conn.commit()
    conn.close()




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





def assign_challenge(
    challenge_id,
    user_id
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
            user_id,
            challenge_id
        )
    )


    conn.commit()
    conn.close()




def get_active_challenge(user_id):

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        SELECT
            id,
            creator_id,
            original_photo

        FROM challenges

        WHERE challenger_id=?
        AND status='playing'

        ORDER BY id DESC

        LIMIT 1

        """,
        (user_id,)
    )


    result = cur.fetchone()


    conn.close()

    return result





def save_reply(
    challenge_id,
    photo
):

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        UPDATE challenges

        SET reply_photo=?,
            status='completed'

        WHERE id=?

        """,
        (
            photo,
            challenge_id
        )
    )


    conn.commit()
    conn.close()
