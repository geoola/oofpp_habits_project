import sqlite3
from datetime import datetime


def get_db(name="main.db"):
    """
    establishes the connection to the sqlite3 database.
    name: database's title
    return: creates a sqlite3 database and establishes a connection to it.
    """

    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Create tables in the database if they don't exist
    """

    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habits (
        name TEXT PRIMARY KEY,
        description TEXT,
        period TEXT,
        created TEXT,
        current_streak INTEGER,
        longest_streak INTEGER,
        broken INTEGER)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        habitName TEXT,
        check_off_date DATETIME,
        FOREIGN KEY (habitName) REFERENCES habits(name)
        )""")

    db.commit()


def add_habit(db, name, description, period, created=None, current_streak=0, longest_streak=0, broken=0):
    """
    Adds a new habit into the database
    :param db: initialized sqlite3 database connection
    :param name: name of the habit
    :param description: description of the habit
    :param period: periodicity of the habit
    :param created: date when the habit was created
    :param current_streak: current streak of the habit
    :param longest_streak: longest streak of the habit
    :param broken: number of times the habit was broken
    """

    cur = db.cursor()
    cur.execute("SELECT name FROM habits WHERE name=?", (name,))
    search = cur.fetchone()
    # if habit already exists
    if search:
        return False
    # if there is no such name in database - add habit
    else:
        if created is None:
            created = datetime.now().strftime("%d-%m-%Y %H:%M")
        cur.execute("INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (name, description, period, created, current_streak, longest_streak, broken))
        db.commit()
        return True


def delete_a_habit(db, name):
    """
    Delete the habit from both tables in database
    :param db: initialized sqlite3 database connection
    :param name: name of a habit that should be deleted
    """

    cur = db.cursor()
    cur.execute("DELETE FROM habits WHERE name=?", (name,))
    cur.execute("DELETE FROM tracker WHERE habitName=?", (name,))
    db.commit()


def update_current_streak(db, name, current_streak):
    """
    Updates the streak value in the habits table.
    db: initialized sqlite3 database connection
    name: name of the habit
    current_streak: current streak of the habit to update
    """

    cur = db.cursor()
    cur.execute("UPDATE habits SET current_streak=? WHERE name=?", (current_streak, name))
    db.commit()


def get_current_streak(db, name):
    """
    Return the current streak of a given habit
    :param db: initialized sqlite3 database connection
    :param name: name of the habit
    """

    cur = db.cursor()
    cur.execute("SELECT current_streak FROM habits WHERE name=?", (name,))
    result = cur.fetchone()
    if result is not None:
        return result[0]  # returning the first element of tuple
    else:
        raise ValueError(f"No habit found with name '{name}'")


def update_longest_streak(db, name, longest_streak):
    """
    Updates the longest streak value in the habits table.
    :param db: initialized sqlite3 database connection
    :param name: name of the habit
    :param longest_streak: longest streak of the habit to update
    """

    cur = db.cursor()
    cur.execute("UPDATE habits SET longest_streak=? WHERE name=?", (longest_streak, name))
    db.commit()


def get_longest_streak(db, name):
    """
    Return the longest streak of a given habit
    :param db: initialized sqlite3 database connection
    :param name: name of the habit
    """

    cur = db.cursor()
    cur.execute("SELECT longest_streak FROM habits WHERE name=?", (name,))
    result = cur.fetchone()
    if result is not None:
        return result[0]  # returning the first element of tuple
    else:
        raise ValueError(f"No habit found with name '{name}'")


def update_broken(db, name, broken):
    """
    Updates the streak value in the habits table.
    db: initialized sqlite3 database connection
    name: name of the habit
    broken: broken habit to update
    """

    cur = db.cursor()
    cur.execute("UPDATE habits SET broken=? WHERE name=?", (broken, name))
    db.commit()


def get_broken(db, name):
    """
    Return the current streak of a given habit
    :param db: connection to a sqlite3 database
    :param name: name of the habit
    """

    cur = db.cursor()
    cur.execute("SELECT broken FROM habits WHERE name=?", (name,))
    result = cur.fetchone()
    if result is not None:
        return result[0]  # returning the first element of tuple
    else:
        raise ValueError(f"No habit found with name '{name}'")


def get_period(db, name):
    """
    Return the period of a given habit
    :param db: a connection to a sqlite3 database
    :param name: name of the habit
    """

    cur = db.cursor()
    cur.execute("SELECT period FROM habits WHERE name=?", (name,))
    return cur.fetchone()[0]  # returning the first element of tuple


def get_habits(db):
    """
    Select all records from the habits table
    :param db: initialized sqlite3 database connection
    """

    cur = db.cursor()
    cur.execute("SELECT * from habits")
    return cur.fetchall()


def get_habit_tracker(db, name):
    """
    Select all records of a given habit from the tracker table
    :param db: initialized sqlite3 database connection
    :param name: name of the habit
    """

    cur = db.cursor()
    cur.execute("SELECT * from tracker WHERE habitName=?", (name,))
    return cur.fetchall()


def get_tracker_names(db):
    """
    Select all records of a given habit from the tracker table
    :param db: initialized sqlite3 database connection
    """

    cur = db.cursor()
    cur.execute("SELECT habitName from tracker")
    return cur.fetchall()


def increment_check_off(db, name, check_off_date=None):
    """
    Store check-off in the tracker table
    :param db: initialized sqlite3 database connection
    :param name: name of the habit
    :param check_off_date: check-off time and date
    """

    cur = db.cursor()
    if not check_off_date:
        check_off_date = datetime.now().strftime("%d-%m-%Y %H:%M")
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (name, check_off_date))
    db.commit()


def get_last_check_off_date(db, name):
    """
    Returns the last check-off date of a habit.
    :param db: initialized sqlite3 database connection
    :param name: name of the habit
    """

    cur = db.cursor()
    cur.execute("SELECT check_off from tracker WHERE habitName=?", (name,))
    return cur.fetchone()[-1]  # returning the last element of tuple
