# Habit Tracker

A command-line application for tracking and analyzing personal habits.

## Overview

This Habit Tracker helps you create, manage, and analyze habits with different periodicities (daily, weekly, monthly). It allows you to record check-ins when you complete habits and provides powerful streak analysis to keep you motivated.

## Features

- **Habit Management**: Create, view, update, and delete personal habits
- **Check-in System**: Record your progress when you complete habits
- **Streak Analysis**: Track your current and longest streaks for each habit
- **Periodicity Support**: Set habits as daily, weekly, or monthly
- **Persistence**: All data is stored in a SQLite database

## Requirements

- Python 3.13
- SQLite3

No external dependencies are required beyond the Python standard library.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/habit-tracker.git
   cd habit-tracker
   ```

2. Ensure you have a compatible version of Python installed:
   ```
   python --version
   ```

3. The application will automatically create the database on first run.

## Usage

Run the application:
```
python main.py
```

### Available Commands

- `create habit`: Create a new habit with name, periodicity, and description
- `get habit`: View details about a specific habit
- `get habits`: List all habits
- `update habit`: Modify an existing habit's details
- `delete habit`: Remove a habit from the system
- `check in`: Record completion of a habit
- `get checkin`: View check-ins for a specific habit
- `get checkins`: View all check-ins
- `get streaks`: Calculate and display current streaks
- `get longest streaks`: Calculate and display longest historical streaks
- `exit`: Quit the application

## Application Structure

- `main.py`: Entry point and command-line interface
- `habit.py`: Habit class definition and management functions
- `checkin.py`: Check-in functionality
- `habitstreak.py`: Streak calculation algorithms

## Database Schema

The application uses two main tables:

### Habit
- `habitID`: Primary key
- `name`: Habit name
- `periodicity`: Frequency (Daily/Weekly/Monthly)
- `description`: Habit description
- `start_date`: Creation date

### CheckIn
- `checkinID`: Primary key
- `habitID`: Foreign key referencing Habit
- `date`: Check-in date and time
- `previouscheckin`: Reference to previous check-in date

## Example Usage

```
Command: create habit
Enter habit name: Morning Meditation
Enter periodicity (Daily/Weekly/Monthly): Daily
Enter habit description: 10 minutes of mindfulness practice each morning
Habit 'Morning Meditation' successfully created!

Command: check in
1 | Morning Meditation | Daily | 10 minutes of mindfulness practice each morning | 2025-03-15 08:30:12
Select a valid habit ID: 1
Check-in recorded for Habit ID 1.

Command: get streaks
Current Streaks:
Habit ID 1: 1 daily streak(s)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

