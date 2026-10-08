import sqlite3


DATABASE = "deutschly.db"


def get_connection():

    return sqlite3.connect(
        DATABASE
    )


def init_db():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            chapter_id INTEGER UNIQUE,

            chapter_name TEXT,

            score INTEGER DEFAULT 0,

            xp INTEGER DEFAULT 0,

            completed INTEGER DEFAULT 0
        )
    """)

    connection.commit()

    connection.close()


def save_quiz_result(
    chapter_id,
    chapter_name,
    score,
    xp,
    completed
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO progress
        (
            chapter_id,
            chapter_name,
            score,
            xp,
            completed
        )

        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(chapter_id)

        DO UPDATE SET

            score = excluded.score,

            xp = excluded.xp,

            completed = excluded.completed
        """,

        (
            chapter_id,
            chapter_name,
            score,
            xp,
            int(completed)
        )
    )

    connection.commit()

    connection.close()


def get_progress():

    connection = get_connection()

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            chapter_id,
            chapter_name,
            score,
            xp,
            completed

        FROM progress

        ORDER BY chapter_id
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]
