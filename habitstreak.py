import sqlite3
from datetime import datetime, timedelta

def get_streaks():
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    # Get all habits with periodicity
    cursor.execute("""
        SELECT DISTINCT Habit.habitID, Habit.periodicity
        FROM Habit
        INNER JOIN CheckIn ON Habit.habitID = CheckIn.habitID;
    """)
    habits = cursor.fetchall()

    streaks = {}

    for habit_id, periodicity in habits:
        # Get check-ins ordered by date (newest first)
        cursor.execute("""
            SELECT date, previouscheckin FROM CheckIn
            WHERE habitID = ?
            ORDER BY date DESC;
        """, (habit_id,))

        checkins = cursor.fetchall()
        if not checkins:
            continue

        # Convert check-in dates to datetime objects
        checkin_dates = [datetime.strptime(str(c[0]), "%Y-%m-%d %H:%M:%S") for c in checkins]

        # Determine allowed gap for streaks
        if periodicity.lower() == "daily":
            max_gap = timedelta(days=1)
        elif periodicity.lower() == "weekly":
            max_gap = timedelta(days=7)
        elif periodicity.lower() == "monthly":
            max_gap = timedelta(days=31)
        else:
            continue  # Skip if periodicity is invalid

        # Calculate the streak based on previous check-in
        streak_count = 1
        for i in range(len(checkin_dates) - 1):
            prev_checkin_time = checkin_dates[i + 1]  # The previous check-in
            current_checkin_time = checkin_dates[i]  # The latest check-in

            # If within the allowed gap, continue the streak
            if (current_checkin_time - prev_checkin_time) <= max_gap:
                streak_count += 1
            else:
                break  # Streak is broken

        streaks[habit_id] = (streak_count, periodicity)

    conn.close()

    # Print streak results
    print("Current Streaks:")
    for habit_id, (streak, periodicity) in streaks.items():
        print(f"Habit ID {habit_id}: {streak} {periodicity.lower()} streak(s)")

    return streaks

def get_longest_streaks():
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    # Get all habits with periodicity
    cursor.execute("""
        SELECT DISTINCT Habit.habitID, Habit.name, Habit.periodicity
        FROM Habit
        INNER JOIN CheckIn ON Habit.habitID = CheckIn.habitID;
    """)
    habits = cursor.fetchall()

    longest_streaks = {}

    for habit_id, habit_name, periodicity in habits:
        # Get check-ins ordered by date
        cursor.execute("""
            SELECT date FROM CheckIn
            WHERE habitID = ?
            ORDER BY date ASC;
        """, (habit_id,))

        checkins = cursor.fetchall()
        if not checkins:
            continue

        # Convert check-in dates to datetime objects
        checkin_dates = []
        for c in checkins:
            try:
                # Try different date formats
                date_str = str(c[0])
                if " " in date_str:  # Has time component
                    checkin_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                else:  # Just date
                    checkin_date = datetime.strptime(date_str, "%Y-%m-%d")
                checkin_dates.append(checkin_date)
            except ValueError:
                # Skip invalid dates
                continue

        # Sort dates in case they aren't already sorted
        checkin_dates.sort()

        # Determine allowed gap for streaks
        if periodicity.lower() == "daily":
            max_gap = timedelta(days=1)
        elif periodicity.lower() == "weekly":
            max_gap = timedelta(days=7)
        elif periodicity.lower() == "monthly":
            max_gap = timedelta(days=31)
        else:
            continue  # Skip if periodicity is invalid

        # Calculate streaks
        current_streak = 1
        longest_streak = 1
        
        for i in range(1, len(checkin_dates)):
            current_date = checkin_dates[i]
            prev_date = checkin_dates[i-1]
            
            # If within the allowed gap, continue the streak
            if (current_date - prev_date) <= max_gap:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                # Streak is broken
                current_streak = 1

        longest_streaks[habit_id] = (longest_streak, habit_name, periodicity)

    conn.close()

    # Print longest streak results
    print("Longest Streaks:")
    for habit_id, (streak, name, periodicity) in longest_streaks.items():
        print(f"Habit: {name} (ID {habit_id}): {streak} {periodicity.lower()} streak(s)")

    return longest_streaks

