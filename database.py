import os
import psycopg2


DATABASE_URL = os.getenv("DATABASE_URL")


def connect():
    return psycopg2.connect(
        DATABASE_URL
    )



def init_db():

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS challenges (

        id SERIAL PRIMARY KEY,

        creator_id BIGINT NOT NULL,

        original_photo TEXT NOT NULL,

        challenger_id BIGINT,

        reply_photo TEXT,

        status TEXT DEFAULT 'waiting'

    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS gallery (

        id SERIAL PRIMARY KEY,

        collage_photo TEXT NOT NULL

    )
    """)



    conn.commit()
    cur.close()
    conn.close()





def add_challenge(user_id, photo):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO challenges
        (
            creator_id,
            original_photo
        )

        VALUES (%s,%s)
        """,
        (
            user_id,
            photo
        )
    )

    conn.commit()
    cur.close()
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
        AND creator_id != %s

        ORDER BY RANDOM()

        LIMIT 1
        """,
        (user_id,)
    )


    result = cur.fetchone()

    cur.close()
    conn.close()

    return result





def assign_challenge(challenge_id,user_id):

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        UPDATE challenges

        SET challenger_id=%s,
            status='playing'

        WHERE id=%s
        """,
        (
            user_id,
            challenge_id
        )
    )


    conn.commit()

    cur.close()
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

        WHERE challenger_id=%s
        AND status='playing'

        LIMIT 1
        """,
        (user_id,)
    )


    result = cur.fetchone()

    cur.close()
    conn.close()

    return result





def save_reply(challenge_id,photo):

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        UPDATE challenges

        SET reply_photo=%s,
            status='completed'

        WHERE id=%s
        """,
        (
            photo,
            challenge_id
        )
    )


    conn.commit()

    cur.close()
    conn.close()





def add_to_gallery(photo):

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        INSERT INTO gallery
        (
        collage_photo
        )

        VALUES (%s)
        """,
        (photo,)
    )


    conn.commit()

    cur.close()
    conn.close()





def get_gallery():

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        SELECT collage_photo

        FROM gallery

        ORDER BY id DESC

        LIMIT 10
        """
    )


    result = cur.fetchall()


    cur.close()
    conn.close()

    return result
