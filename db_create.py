import sqlite3

db_name = "habits.db"
conn = sqlite3.connect(db_name)

conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

cursor.executescript("""
-- Create Habit table
CREATE TABLE IF NOT EXISTS Habit (
    habitID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    periodicity TEXT NOT NULL,
    description TEXT,
    streakactive BOOLEAN NOT NULL CHECK (streakactive IN (0, 1)),
    longeststreak INTEGER DEFAULT 0,
    start_date DATE NOT NULL,
    completion_date DATE
);

-- Create CheckIn table
CREATE TABLE IF NOT EXISTS CheckIn (
    checkinID INTEGER PRIMARY KEY AUTOINCREMENT,
    habitID INTEGER NOT NULL,
    date DATE NOT NULL,
    previouscheckin DATE,
    FOREIGN KEY (habitID) REFERENCES Habit(habitID) ON DELETE CASCADE
);

-- Create HabitStreaks table
CREATE TABLE IF NOT EXISTS HabitStreaks (
    streakID INTEGER PRIMARY KEY AUTOINCREMENT,
    habitID INTEGER NOT NULL,
    lastcheckin INTEGER,
    streaklength INTEGER NOT NULL DEFAULT 0,
    currentstreak BOOLEAN NOT NULL CHECK (currentstreak IN (0, 1)),
    streakstart DATE NOT NULL,
    streakend DATE,
    FOREIGN KEY (habitID) REFERENCES Habit(habitID) ON DELETE CASCADE,
    FOREIGN KEY (lastcheckin) REFERENCES CheckIn(checkinID) ON DELETE SET NULL
);
""")

conn.commit()
conn.close()

print(f"Database '{db_name}' and tables created successfully!")