import habit
import checkin
from habit import Habit

from datetime import datetime
user_input = ""
while user_input != 'exit':
    user_input = input("Command : ")

    if  user_input == "create habit":
        name = input("Enter habit name: ")
        while True:
            periodicity = input("Enter periodicity (Daily/Weekly/Monthly): ")
            if periodicity in ["Daily", "Weekly", "Monthly"]:
                break
            else:
                print("Invalid input. Please enter 'Daily', 'Weekly', or 'Monthly'.")
        description = input("Enter habit description: ")
        
        habit = Habit(name, periodicity, description)
        habit.save_to_db()

    elif user_input == "get habit":
        habit_id = input("Enter a valid Habit ID : ")
        habit = Habit.get_by_id(habit_id)
        if habit:
            print(habit.to_string())

print("Goodbye!")