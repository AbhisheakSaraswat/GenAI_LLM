import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Clear tables if they already exist
cursor.execute('DROP TABLE IF EXISTS students')
cursor.execute('DROP TABLE IF EXISTS courses')
cursor.execute('DROP TABLE IF EXISTS enrollments')

# Create 'students' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
 id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 age INTEGER NOT NULL,
 major TEXT NOT NULL
)
''')

# Create 'courses' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
 id INTEGER PRIMARY KEY,
 course_name TEXT NOT NULL,
 credits INTEGER NOT NULL
)
''')

# Create 'enrollments' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS enrollments (
 student_id INTEGER,
 course_id INTEGER,
 semester TEXT NOT NULL,
 FOREIGN KEY (student_id) REFERENCES students(id),
 FOREIGN KEY (course_id) REFERENCES courses(id)
)
''')

# Insert data into 'students' table
students = [
 (1, 'Vinay', 20, 'Computer Science'),
 (2, 'Abhishek', 22, 'Mathematics'),
 (3, 'Vivek', 23, 'Physics')
]

cursor.executemany('''
INSERT INTO students (id, name, age, major) VALUES (?, ?, ?, ?)
''', students)

# Insert data into 'courses' table
courses = [
 (1, 'Introduction to Computer Science', 4),
 (2, 'Calculus I', 3),
 (3, 'Physics I', 4)
]

cursor.executemany('''
INSERT INTO courses (id, course_name, credits) VALUES (?, ?, ?)
''', courses)

# Insert data into 'enrollments' table
enrollments = [
 (1, 1, 'Fall 2023'),
 (1, 2, 'Spring 2024'),
 (2, 2, 'Fall 2023'),
 (3, 3, 'Spring 2024')
]

cursor.executemany('''
INSERT INTO enrollments (student_id, course_id, semester) VALUES (?, ?, ?)
''', enrollments)

# Commit changes and close the connection
conn.commit()
conn.close()
