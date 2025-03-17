import sqlite3
from datetime import datetime

class Habit:
    """
    Habit Class

    Represents a habit to be tracked in the habit tracking application.
    Provides methods for creating, retrieving, updating, and deleting habits
    in the SQLite database.
    """

    def __init__(self, name, periodicity, description):
        """
        Initialize a new Habit with the current date as start date.
        
        Args:
            name (str): Name of the habit
            periodicity (str): Frequency of the habit (Daily/Weekly/Monthly)
            description (str): Description of the habit
        """
        self.name = name
        self.periodicity = periodicity
        self.description = description
        self.startDate = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self, name, periodicity, description, start_date):
        """
        Initialize a Habit with a specified start date.
        
        Args:
            name (str): Name of the habit
            periodicity (str): Frequency of the habit (Daily/Weekly/Monthly)
            description (str): Description of the habit
            start_date (str): Date when the habit was created
        """
        self.name = name
        self.periodicity = periodicity
        self.description = description
        self.startDate = start_date

    def to_string(self):
        """
        Returns a string representation of the habit.
        
        Returns:
            str: Formatted string with habit details
        """
        return f"Name : {self.name}\nDescription : {self.description} \nStart Date : {self.startDate} "

    @staticmethod
    def connect_db():
        """
        Establishes a connection to the SQLite database.
        Enables foreign key constraints.
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        db_name = "habits.db"
        conn = sqlite3.connect(db_name)
        conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints
        return conn


    def save_to_db(self):
        """
        Saves the current habit to the database.
        
        Creates a new habit record with the current object's attributes.
        Commits the transaction and closes the connection.
        """
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


    @staticmethod
    def get_by_id(habit_id):
        """
        Retrieves a habit by its ID from the database.
        
        Args:
            habit_id: The ID of the habit to retrieve
            
        Returns:
            Habit: A Habit object if found, None otherwise
        """
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
        
    @staticmethod
    def get_habits():
        """
        Retrieves all habits from the database.
        
        Returns:
            sqlite3.Cursor: A cursor containing all habits from the database
        """
        conn = Habit.connect_db()
        cursor = conn.cursor()
        habits = cursor.execute("""SELECT * FROM Habit""")
        return habits

    @staticmethod
    def update_habit(id, new_name=None, new_per=None, new_desc=None):
        """
        Updates a habit's details based on provided parameters.
        
        Updates only the fields that have been provided.
        
        Args:
            id: The ID of the habit to update
            new_name (str, optional): New name for the habit
            new_per (str, optional): New periodicity for the habit (Daily/Weekly/Monthly)
            new_desc (str, optional): New description for the habit
        """
        conn = Habit.connect_db()
        cursor = conn.cursor()

        # Update only provided fields
        if new_name:
            cursor.execute("""UPDATE Habit SET name = ? WHERE habitID = ?""", (new_name, id))
        if new_per and new_per in ["Daily", "Weekly", "Monthly"]:
            cursor.execute("""UPDATE Habit SET periodicity = ? WHERE habitID = ?""", (new_per, id))
        if new_desc:
            cursor.execute("""UPDATE Habit SET description = ? WHERE habitID = ?""", (new_desc, id))

        conn.commit()
        conn.close()

    @staticmethod
    def delete_habit(id):
        """
        Deletes a habit and its associated check-ins from the database.
        
        Args:
            id: The ID of the habit to delete
        """
        conn = Habit.connect_db()
        cursor = conn.cursor()

        habit = Habit.get_by_id(id)

        # Delete associated check-ins
        cursor.execute("""DELETE FROM CheckIn WHERE habitID = ?""", (id,))

        # Delete the habit
        cursor.execute("""DELETE FROM Habit WHERE habitID = ?""", (id,))

        conn.commit()
        conn.close()
        print(f"{habit.name} and its associated check-ins successfully deleted!")

    @staticmethod
    def is_valid_id(habit_id):
        """
        Checks if a habit ID is valid (exists in the database).
        
        Args:
            habit_id: The ID of the habit to check
            
        Returns:
            bool: True if the ID exists, False otherwise
        """
        conn = Habit.connect_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT 1 FROM Habit WHERE habitID = ?""", (habit_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists