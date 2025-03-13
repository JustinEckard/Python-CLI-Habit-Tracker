import sqlite3
import habit
import datetime

# Connect to the database
db_name = "habits.db"
conn = sqlite3.connect(db_name)

conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()


def create_checkin():
    print(habit.get_habits())

    habit_id = input("Enter a Valid Habit ID : ")

    if get_checkins() == None:
        cursor.execute(
            """
        INSERT INTO CheckIn (habitId, date, previouscheckin)
        VALUES (?,?,?);
        """, (habit_id, datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.today().strftime('%Y-%m-%d'))
        )
        conn.commit()
        print(cursor.lastrowid)

def get_checkins():
    cursor.execute(
        """
    SELECT * FROM CheckIn;
    """
    )
    checkins =  cursor.fetchall()
    for checkin in checkins:
        print(checkin)

def get_checkin(habit_id):
    cursor.execute(
        """
    SELECT * FROM CheckIn WHERE habitID = ?;
    """,(habit_id,)
    )
    checkins =  cursor.fetchall()
    for checkin in checkins:
        print(checkin)

