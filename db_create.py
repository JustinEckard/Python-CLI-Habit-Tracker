import sqlite3

db_name = "habits.db"
conn = sqlite3.connect(db_name)

conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

cursor.executescript("""
-- Clear existing data for fresh test dataset
DELETE FROM CheckIn;
DELETE FROM Habit;
DELETE FROM sqlite_sequence WHERE name IN ('Habit', 'CheckIn');

-- Create test habits with different periodicities
INSERT INTO Habit (name, periodicity, description, start_date) VALUES
('Daily Meditation', 'Daily', 'Meditate for 10 minutes each morning', '2025-02-15 08:00:00'),
('Weekly Jogging', 'Weekly', 'Go for a 5k jog', '2025-02-15 09:00:00'),
('Bi-Weekly Gym', 'Weekly', 'Full body workout at the gym', '2025-02-15 10:00:00'),
('Daily Reading', 'Daily', 'Read at least 20 pages', '2025-02-15 20:00:00'),
('Monthly Cleaning', 'Monthly', 'Deep clean the apartment', '2025-02-15 14:00:00'),
('Daily Coding', 'Daily', 'Work on personal coding projects', '2025-02-15 19:00:00'),
('Daily Walking', 'Daily', 'Walk for at least 30 minutes', '2025-02-15 17:00:00'),
('Daily Journaling', 'Daily', 'Write in journal before bed', '2025-02-15 22:00:00');

-- 4 weeks of check-ins with more active daily streaks
-- Most habits have strong streaks with minimal breaks

-- Daily Meditation (habitID 1)
-- Near perfect streak with only one missed day
INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES
-- Week 1 (perfect)
(1, '2025-02-15 08:15:00', NULL),
(1, '2025-02-16 08:30:00', '2025-02-15 08:15:00'),
(1, '2025-02-17 08:10:00', '2025-02-16 08:30:00'),
(1, '2025-02-18 08:05:00', '2025-02-17 08:10:00'),
(1, '2025-02-19 08:20:00', '2025-02-18 08:05:00'),
(1, '2025-02-20 08:15:00', '2025-02-19 08:20:00'),
(1, '2025-02-21 08:30:00', '2025-02-20 08:15:00'),
-- Week 2 (perfect)
(1, '2025-02-22 08:20:00', '2025-02-21 08:30:00'),
(1, '2025-02-23 08:15:00', '2025-02-22 08:20:00'),
(1, '2025-02-24 08:25:00', '2025-02-23 08:15:00'),
(1, '2025-02-25 08:15:00', '2025-02-24 08:25:00'),
(1, '2025-02-26 08:05:00', '2025-02-25 08:15:00'),
(1, '2025-02-27 08:10:00', '2025-02-26 08:05:00'),
(1, '2025-02-28 08:30:00', '2025-02-27 08:10:00'),
-- Week 3 (perfect)
(1, '2025-03-01 08:15:00', '2025-02-28 08:30:00'),
(1, '2025-03-02 08:10:00', '2025-03-01 08:15:00'),
(1, '2025-03-03 08:05:00', '2025-03-02 08:10:00'),
(1, '2025-03-04 08:20:00', '2025-03-03 08:05:00'),
(1, '2025-03-05 08:15:00', '2025-03-04 08:20:00'),
(1, '2025-03-06 08:25:00', '2025-03-05 08:15:00'),
(1, '2025-03-07 08:10:00', '2025-03-06 08:25:00'),
-- Week 4 (missing only Mar 10)
(1, '2025-03-08 08:15:00', '2025-03-07 08:10:00'),
(1, '2025-03-09 08:30:00', '2025-03-08 08:15:00'),
(1, '2025-03-11 08:20:00', '2025-03-09 08:30:00'), -- Break in streak
(1, '2025-03-12 08:10:00', '2025-03-11 08:20:00'),
(1, '2025-03-13 08:05:00', '2025-03-12 08:10:00'),
(1, '2025-03-14 08:15:00', '2025-03-13 08:05:00');

-- Weekly Jogging (habitID 2) 
-- Now consistent every week, with some twice-weekly occurrences
INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES
(2, '2025-02-16 09:30:00', NULL),           -- Week 1
(2, '2025-02-19 17:30:00', '2025-02-16 09:30:00'), -- Extra session
(2, '2025-02-23 09:45:00', '2025-02-19 17:30:00'), -- Week 2
(2, '2025-03-02 09:30:00', '2025-02-23 09:45:00'), -- Week 3
(2, '2025-03-05 17:45:00', '2025-03-02 09:30:00'), -- Extra session
(2, '2025-03-09 09:15:00', '2025-03-05 17:45:00'), -- Week 4
(2, '2025-03-13 17:30:00', '2025-03-09 09:15:00'); -- Extra session

-- Bi-Weekly Gym (habitID 3)
-- Consistently twice a week with extra sessions
INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES
-- Week 1
(3, '2025-02-17 18:00:00', NULL),
(3, '2025-02-20 17:30:00', '2025-02-17 18:00:00'),
(3, '2025-02-21 18:15:00', '2025-02-20 17:30:00'), -- Extra session
-- Week 2
(3, '2025-02-24 18:15:00', '2025-02-21 18:15:00'),
(3, '2025-02-27 17:45:00', '2025-02-24 18:15:00'),
-- Week 3
(3, '2025-03-03 18:00:00', '2025-02-27 17:45:00'),
(3, '2025-03-06 18:00:00', '2025-03-03 18:00:00'),
-- Week 4
(3, '2025-03-10 17:30:00', '2025-03-06 18:00:00'),
(3, '2025-03-13 18:15:00', '2025-03-10 17:30:00'),
(3, '2025-03-14 18:00:00', '2025-03-13 18:15:00'); -- Extra session

-- Daily Reading (habitID 4)
-- Strong streak with just one brief break
INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES
-- Week 1 (perfect)
(4, '2025-02-15 21:15:00', NULL),
(4, '2025-02-16 21:30:00', '2025-02-15 21:15:00'),
(4, '2025-02-17 21:00:00', '2025-02-16 21:30:00'),
(4, '2025-02-18 21:45:00', '2025-02-17 21:00:00'),
(4, '2025-02-19 21:20:00', '2025-02-18 21:45:00'),
(4, '2025-02-20 21:10:00', '2025-02-19 21:20:00'),
(4, '2025-02-21 21:35:00', '2025-02-20 21:10:00'),
-- Week 2 (perfect)
(4, '2025-02-22 21:15:00', '2025-02-21 21:35:00'),
(4, '2025-02-23 21:30:00', '2025-02-22 21:15:00'),
(4, '2025-02-24 21:20:00', '2025-02-23 21:30:00'),
(4, '2025-02-25 21:40:00', '2025-02-24 21:20:00'),
(4, '2025-02-26 21:20:00', '2025-02-25 21:40:00'),
(4, '2025-02-27 21:30:00', '2025-02-26 21:20:00'),
(4, '2025-02-28 21:05:00', '2025-02-27 21:30:00'),
-- Week 3 (one day break)
(4, '2025-03-01 21:25:00', '2025-02-28 21:05:00'),
-- Mar 2 missing
(4, '2025-03-03 21:40:00', '2025-03-01 21:25:00'), -- Break in streak
(4, '2025-03-04 21:10:00', '2025-03-03 21:40:00'),
(4, '2025-03-05 21:30:00', '2025-03-04 21:10:00'),
(4, '2025-03-06 21:20:00', '2025-03-05 21:30:00'),
(4, '2025-03-07 21:15:00', '2025-03-06 21:20:00'),
-- Week 4 (perfect)
(4, '2025-03-08 21:25:00', '2025-03-07 21:15:00'),
(4, '2025-03-09 21:20:00', '2025-03-08 21:25:00'),
(4, '2025-03-10 21:40:00', '2025-03-09 21:20:00'),
(4, '2025-03-11 21:15:00', '2025-03-10 21:40:00'),
(4, '2025-03-12 21:30:00', '2025-03-11 21:15:00'),
(4, '2025-03-13 21:10:00', '2025-03-12 21:30:00'),
(4, '2025-03-14 21:25:00', '2025-03-13 21:10:00');

-- Monthly Cleaning (habitID 5)
-- Additional weekly minor cleaning sessions
INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES
(5, '2025-02-15 14:30:00', NULL),         -- Major February cleaning
(5, '2025-02-22 10:15:00', '2025-02-15 14:30:00'), -- Week 2 minor cleaning
(5, '2025-03-01 11:30:00', '2025-02-22 10:15:00'), -- Week 3 minor cleaning
(5, '2025-03-08 10:45:00', '2025-03-01 11:30:00'), -- Week 4 minor cleaning
(5, '2025-03-14 15:15:00', '2025-03-08 10:45:00'); -- Major March cleaning

-- Daily Coding (habitID 6)
-- Very consistent with just one break
INSERT INTO CheckIn (habitID, date, previouscheckin) VALUES
-- Week 1
(6, '2025-02-15 19:30:00', NULL),
(6, '2025-02-16 20:15:00', '2025-02-15 19:30:00'),
(6, '2025-02-17 19:45:00', '2025-02-16 20:15:00'),
(6, '2025-02-18 20:00:00', '2025-02-17 19:45:00'),
(6, '2025-02-19 19:15:00', '2025-02-18 20:00:00'),
(6, '2025-02-20 20:30:00', '2025-02-19 19:15:00'),
(6, '2025-02-21 19:45:00', '2025-02-20 20:30:00'),
-- Week 2
(6, '2025-02-22 20:00:00', '2025-02-21 19:45:00'),
(6, '2025-02-23 19:30:00', '2025-02-22 20:00:00'),
(6, '2025-02-24 20:15:00', '2025-02-23 19:30:00'),
(6, '2025-02-25 19:45:00', '2025-02-24 20:15:00'),
(6, '2025-02-26 20:00:00', '2025-02-25 19:45:00'),
-- Feb 27-28 missing (brief break)
-- Week 3
(6, '2025-03-01 19:30:00', '2025-02-26 20:00:00'), -- Break in streak
(6, '2025-03-02 20:15:00', '2025-03-01 19:30:00'),
(6, '2025-03-03 19:45:00', '2025-03-02 20:15:00'),
(6, '2025-03-04 20:00:00', '2025-03-03 19:45:00'),
(6, '2025-03-05 19:30:00', '2025-03-04 20:00:00'),
(6, '2025-03-06 20:15:00', '2025-03-05 19:30:00'),
(6, '2025-03-07 19:45:00', '2025-03-06 20:15:00'),
-- Week 4 (perfect)
(6, '2025-03-08 20:00:00', '2025-03-07 19:45:00'),
(6, '2025-03-09 19:30:00', '2025-03-08 20:00:00'),
(6, '2025-03-10 20:15:00', '2025-03-09 19:30:00'),
(6, '2025-03-11 19:45:00', '2025-03-10 20:15:00'),
(6, '2025-03-12 20:00:00', '2025-03-11 19:45:00'),
(6, '2025-03-13 19:30:00', '2025-03-12 20:00:00'),
(6, '2025-03-14 20:15:00', '2025-03-13 19:30:00');

-- Daily Walking (habitID 7)
-- Perfect streak for the
""")

conn.commit()
conn.close()

print(f"Database '{db_name}' and tables created successfully!")