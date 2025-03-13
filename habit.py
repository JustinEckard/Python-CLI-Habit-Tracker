import sqlite3
from datetime import datetime

class Habit:
    def __init__(self, name, periodicity, description):
        self.name = name
        self.periodicity = periodicity
        self.description = description
        self.startDate = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self, name, periodicity, description, start_date):
        self.name = name
        self.periodicity = periodicity
        self.description = description
        self.startDate = start_date

    def to_string(self):
        return f"Name : {self.name}\nDescription : {self.description} \nStart Date : {self.startDate} "

    @staticmethod
    def connect_db():
        db_name = "habits.db"
        conn = sqlite3.connect(db_name)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    
    
    def save_to_db(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Habit (name, periodicity, description, start_date)
               VALUES (?, ?, ?, ?)""",
            (self.name, self.periodicity, self.description, self.startDate)
        )
        conn.commit()
        conn.close()
        print(f"Habit '{self.name} successfully created!")


    def get_by_id(habit_id):
        conn = Habit.connect_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Habit WHERE habitID = ?""",(habit_id,))
        habit_data = cursor.fetchone()
        conn.close()

        if habit_data:
            return Habit(habit_data[1], habit_data[2], habit_data[3], habit_data[4])
        else:
            print("Habit not Found")
            return None

