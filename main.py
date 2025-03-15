# Import necessary modules
import habit
import checkin
import habitstreak
from habit import Habit
from datetime import datetime

"""
Habit Tracker Application Main Module

This is the main entry point for the Habit Tracker application.
It provides a command-line interface for users to interact with their habits,
record check-ins, and analyze streak data.
"""

# Initialize user input
user_input = ""

# Main application loop
while user_input != 'exit':
    # Get command from user
    user_input = input("Command : ")

    # Handle habit creation
    if user_input == "create habit":
        # Collect habit information from user
        name = input("Enter habit name: ")
        
        # Validate periodicity input
        while True:
            periodicity = input("Enter periodicity (Daily/Weekly/Monthly): ")
            if periodicity in ["Daily", "Weekly", "Monthly"]:
                break
            else:
                print("Invalid input. Please enter 'Daily', 'Weekly', or 'Monthly'.")
        
        description = input("Enter habit description: ")
        
        # Create and save the new habit
        habit = Habit(name, periodicity, description,datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        habit.save_to_db()

    # Handle retrieving a specific habit
    elif user_input == "get habit":
        habit_id = input("Enter a valid Habit ID : ")
        habit = Habit.get_by_id(habit_id)
        if habit:
            print(habit.to_string())

    # Handle displaying all habits
    elif user_input == "get habits":
        habits = Habit.get_habits()
        if habits == None:
            print("No saved Habits, create one using 'create habit'")
        else:
            # Display each habit
            for x in habits:
                print(x)
    
    # Handle updating a habit
    elif user_input == "update habit":
        # Display available habits
        habits = Habit.get_habits()
        if habits == None:
            print("No saved Habits, create one using 'create habit'")
        else:
            for x in habits:
                print(x)
        # Get habit to update
        selected_id = input("Select a valid habit ID : ")
        Habit.update_habit(selected_id)

    # Handle deleting a habit
    elif user_input == "delete habit":
        # Display available habits
        habits = Habit.get_habits()
        if habits == None:
            print("No saved Habits, create one using 'create habit'")
        else:
            for x in habits:
                print(x)
        # Get habit to delete
        selected_id = input("Select a valid habit ID : ")
        Habit.delete_habit(selected_id)

    # Check-in related commands
    # Handle creating a new check-in
    elif user_input == "check in":
        # Display available habits
        habits = Habit.get_habits()
        if habits == None:
            print("No saved Habits, create one using 'create habit'")
        else:
            for x in habits:
                print(x)
        # Get habit to check in for
        selected_id = input("Select a valid habit ID : ")
        checkin.create_checkin(selected_id)

    # Handle viewing check-ins for a specific habit
    elif user_input == "get checkin":
        # Display available habits
        habits = Habit.get_habits()
        if habits == None:
            print("No saved Habits, create one using 'create habit'")
        else:
            for x in habits:
                print(x)
        # Get habit to view check-ins for
        selected_id = input("Select a valid habit ID : ")
        checkin.get_checkin(selected_id)
        
    # Handle viewing all check-ins
    elif user_input == "get checkins":
        checkin.get_checkins()

    # Streak analysis commands
    # Handle viewing current streaks
    elif user_input == "get streaks":
        habitstreak.get_streaks()

    # Handle viewing longest streaks
    elif user_input == "get longest streaks":
        habitstreak.get_longest_streaks()

        
# Exit message
print("Goodbye!")