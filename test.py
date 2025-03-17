import unittest
import os
import sqlite3
from datetime import datetime, timedelta
import tempfile
import sys
import gc

# Import modules to test
from habit import Habit
import checkin
import habitstreak

class HabitTrackerTests(unittest.TestCase):
    """Test cases for the Habit Tracker application."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a test database
        self.db_fd, self.db_path = tempfile.mkstemp()
        os.environ["TEST_DB"] = "1"
        
        # Store original connections to restore later
        self.original_connect = sqlite3.connect
        
        # Track database connections to ensure they're closed
        self.connections = []
        
        def mock_connect(database):
            if database == "habits.db":
                conn = sqlite3.connect(self.db_path)
                self.connections.append(conn)
                return conn
            return self.original_connect(database)
        
        sqlite3.connect = mock_connect
        
        # Create test database schema
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create Habit table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Habit (
            habitID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            description TEXT,
            start_date TEXT
        )
        ''')
        
        # Create CheckIn table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS CheckIn (
            checkInID INTEGER PRIMARY KEY AUTOINCREMENT,
            habitID INTEGER,
            date TEXT,
            previouscheckin TEXT,
            FOREIGN KEY (habitID) REFERENCES Habit(habitID) ON DELETE CASCADE
        )
        ''')
        
        conn.commit()
        conn.close()
        
        # Patch Habit.connect_db to use test database
        self.original_connect_db = Habit.connect_db
        
        @staticmethod
        def mock_connect_db():
            conn = sqlite3.connect(self.db_path)
            return conn
        
        Habit.connect_db = mock_connect_db

    def tearDown(self):
        """Clean up test environment after each test."""
        # Close all tracked connections
        for conn in self.connections:
            try:
                conn.close()
            except:
                pass
        
        # Close checkin module connection if it exists
        if hasattr(checkin, 'conn') and checkin.conn:
            try:
                checkin.conn.close()
            except:
                pass
        
        # Force garbage collection to release file handles
        gc.collect()
        
        # Close the file descriptor
        try:
            os.close(self.db_fd)
        except:
            pass
        
        # On Windows, sometimes we need to retry file deletion
        retry_count = 5
        while retry_count > 0:
            try:
                os.unlink(self.db_path)
                break
            except PermissionError:
                retry_count -= 1
                gc.collect()
                import time
                time.sleep(0.1)  # Small delay to allow OS to release the file
        
        # Restore original connect functions
        sqlite3.connect = self.original_connect
        Habit.connect_db = self.original_connect_db
        
        # Restore environment
        if "TEST_DB" in os.environ:
            del os.environ["TEST_DB"]

    def create_test_habit(self):
        """Helper method to create a test habit."""
        habit = Habit("Test Habit", "Daily", "Test Description", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        habit.save_to_db()
        
        # Get the ID of the created habit
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT habitID FROM Habit WHERE name = 'Test Habit'")
        habit_id = cursor.fetchone()[0]
        conn.close()
        
        return habit_id

    def test_habit_creation(self):
        """Test creating a new habit."""
        # Create a habit
        habit = Habit("Test Habit", "Daily", "Test Description", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        habit.save_to_db()
        
        # Verify it was saved to the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Habit WHERE name = 'Test Habit'")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Test Habit")
        self.assertEqual(result[2], "Daily")
        self.assertEqual(result[3], "Test Description")

    def test_get_habit_by_id(self):
        """Test retrieving a habit by ID."""
        # Create a habit
        habit_id = self.create_test_habit()
        
        # Get the habit
        habit = Habit.get_by_id(habit_id)
        
        # Verify habit properties
        self.assertIsNotNone(habit)
        self.assertEqual(habit.name, "Test Habit")
        self.assertEqual(habit.periodicity, "Daily")
        self.assertEqual(habit.description, "Test Description")

    def test_get_all_habits(self):
        """Test retrieving all habits."""
        # Create multiple habits
        for i in range(3):
            habit = Habit(f"Test Habit {i}", "Daily", f"Description {i}", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            habit.save_to_db()
        
        # Get all habits
        habits = Habit.get_habits()
        
        # Convert cursor to list to ensure it's fully consumed
        habits_list = list(habits)
        
        # Count habits
        self.assertEqual(len(habits_list), 3)

    def test_update_habit(self):
        """Test updating a habit."""
        # Create a habit
        habit_id = self.create_test_habit()
        
        # Update the habit
        Habit.update_habit(habit_id, "Updated Habit", "Weekly", "Updated Description")
        
        # Get the updated habit
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Habit WHERE habitID = ?", (habit_id,))
        result = cursor.fetchone()
        conn.close()
        
        # Verify updates
        self.assertEqual(result[1], "Updated Habit")
        self.assertEqual(result[2], "Weekly")
        self.assertEqual(result[3], "Updated Description")

    def test_delete_habit(self):
        """Test deleting a habit."""
        # Create a habit
        habit_id = self.create_test_habit()
        
        # Delete the habit
        Habit.delete_habit(habit_id)
        
        # Verify it was deleted
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Habit WHERE habitID = ?", (habit_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNone(result)

    def test_valid_id_check(self):
        """Test checking if a habit ID is valid."""
        # Create a habit
        habit_id = self.create_test_habit()
        
        # Check valid ID
        self.assertTrue(Habit.is_valid_id(habit_id))
        
        # Check invalid ID
        self.assertFalse(Habit.is_valid_id(9999))

    def test_create_checkin(self):
        """Test creating a check-in for a habit."""
        # Create a habit
        habit_id = self.create_test_habit()
        
        # Create a check-in
        checkin.create_checkin(habit_id)
        
        # Verify check-in was created
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CheckIn WHERE habitID = ?", (habit_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[1], habit_id)

    def test_get_checkins_for_habit(self):
        """Test retrieving check-ins for a specific habit."""
        # Create a habit
        habit_id = self.create_test_habit()
        
        # Create multiple check-ins
        for _ in range(3):
            checkin.create_checkin(habit_id)
        
        # Verify check-ins were created
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM CheckIn WHERE habitID = ?", (habit_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 3)

    def test_streaks_calculation(self):
        """Test calculating streaks for habits."""
        # Create a habit
        habit_id = self.create_test_habit()
        
        # Create check-ins with appropriate dates for a streak
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create 3 check-ins one day apart
        today = datetime.today()
        
        for i in range(3):
            check_date = (today - timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
            prev_date = (today - timedelta(days=i+1)).strftime('%Y-%m-%d %H:%M:%S') if i < 2 else None
            
            cursor.execute(
                "INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES (?, ?, ?)",
                (habit_id, check_date, prev_date)
            )
        
        conn.commit()
        conn.close()
        
        # Test streak calculation
        streaks = habitstreak.get_streaks()
        
        # A daily habit with 3 check-ins one day apart should have a streak of 3
        self.assertIn(habit_id, streaks)
        self.assertEqual(streaks[habit_id][0], 3)  # First element is streak count

    def test_longest_streaks(self):
        """Test calculating longest streaks for habits."""
        # Create a habit
        habit_id = self.create_test_habit()
        
        # Create check-ins with a broken streak pattern
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.today()
        
        # First streak: 3 consecutive days
        for i in range(3):
            check_date = (today - timedelta(days=i+10)).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES (?, ?, ?)",
                (habit_id, check_date, None)
            )
        
        # Gap of 3 days (break streak)
        
        # Second streak: 5 consecutive days
        for i in range(5):
            check_date = (today - timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES (?, ?, ?)",
                (habit_id, check_date, None)
            )
        
        conn.commit()
        conn.close()
        
        # Test longest streak calculation
        longest_streaks = habitstreak.get_longest_streaks()
        
        # The longest streak should be 5
        self.assertIn(habit_id, longest_streaks)
        self.assertEqual(longest_streaks[habit_id][0], 5)  # First element is streak count

    def test_multiple_habit_streaks(self):
        """Test calculating streaks for multiple habits."""
        # Create two habits with different periodicities
        habit1 = Habit("Daily Habit", "Daily", "Test daily habit", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        habit1.save_to_db()
        
        habit2 = Habit("Weekly Habit", "Weekly", "Test weekly habit", datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        habit2.save_to_db()
        
        # Get habit IDs
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT habitID FROM Habit WHERE name = 'Daily Habit'")
        habit1_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT habitID FROM Habit WHERE name = 'Weekly Habit'")
        habit2_id = cursor.fetchone()[0]
        
        # Create check-ins for daily habit (4 consecutive days)
        today = datetime.today()
        for i in range(4):
            check_date = (today - timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES (?, ?, ?)",
                (habit1_id, check_date, None)
            )
        
        # Create check-ins for weekly habit (3 weeks, one week apart)
        for i in range(3):
            check_date = (today - timedelta(weeks=i)).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES (?, ?, ?)",
                (habit2_id, check_date, None)
            )
        
        conn.commit()
        conn.close()
        
        # Test streak calculations
        streaks = habitstreak.get_streaks()
        
        # Verify both habits have correct streaks
        self.assertIn(habit1_id, streaks)
        self.assertEqual(streaks[habit1_id][0], 4)  # Daily habit has 4-day streak
        
        self.assertIn(habit2_id, streaks)
        self.assertEqual(streaks[habit2_id][0], 3)  # Weekly habit has 3-week streak

if __name__ == '__main__':
    unittest.main()