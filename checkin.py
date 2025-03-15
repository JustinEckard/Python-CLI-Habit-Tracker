import sqlite3
from datetime import datetime
from habit import Habit

"""
Check-in Module

This module handles all functionality related to check-ins for habits.
It provides functions to create new check-ins, retrieve all check-ins,
and retrieve check-ins for a specific habit.
"""

# Connect to the database
db_name = "habits.db"
conn = sqlite3.connect(db_name)

# Enable foreign key constraints
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()


def create_checkin(habit_id):
    """
    Creates a new check-in for a habit.

    Records the current date and time as a check-in for the specified habit.
    Stores a reference to the previous check-in to support streak calculations.

    Args:
        habit_id: The ID of the habit to check in for
    """
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    # Fetch the last check-in date
    cursor.execute(
        """
        SELECT date FROM CheckIn 
        WHERE habitID = ? 
        ORDER BY date DESC 
        LIMIT 1;
        """, 
        (habit_id,)
    )
    last_checkin = cursor.fetchone()

    # Determine previous check-in value
    previous_checkin = last_checkin[0] if last_checkin else None

    # Insert new check-in
    cursor.execute(
        """
        INSERT INTO CheckIn (habitID, date, previouscheckin)
        VALUES (?, ?, ?);
        """, 
        (habit_id, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), previous_checkin)
    )

    conn.commit()
    conn.close()

    print(f"Check-in recorded for Habit ID {habit_id}.")


def get_checkins():
    """
    Retrieves and displays all check-ins from the database.

    Prints each check-in record to the console.
    """
    cursor.execute(
        """
    SELECT * FROM CheckIn;
    """
    )
    checkins = cursor.fetchall()
    for checkin in checkins:
        print(checkin)


def get_checkin(habit_id):
    """
    Retrieves and displays check-ins for a specific habit.

    Prints the habit details followed by all check-in records
    for that habit.

    Args:
        habit_id: The ID of the habit to retrieve check-ins for
    """
    cursor.execute(
        """
    SELECT * FROM CheckIn WHERE habitID = ?;
    """,(habit_id,)
    )
    checkins = cursor.fetchall()
    print(f"Check Ins for :\n {Habit.get_by_id(habit_id).to_string()}")
    for checkin in checkins:
        print(checkin)