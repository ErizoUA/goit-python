teachers = """
CREATE TABLE teachers (
    id SERIAL,
    name VARCHAR(30) UNIQUE NOT NULL
    )
"""

subjects = """
CREATE TABLE subjects (
    id SERIAL,
    name VARCHAR(30) UNIQUE NOT NULL,
    teacher_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY fk_subjects_teachers (teacher_id) REFERENCES teachers (id)
    )
"""

students = """
CREATE TABLE students (
    id SERIAL,
    name VARCHAR(30) UNIQUE NOT NULL,
    group_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY fk_students_groups (group_id) REFERENCES groups (id)
    )
"""

groups = """
CREATE TABLE groups (
    id SERIAL,
    name VARCHAR(4) UNIQUE
    )
"""

grades = """
CREATE TABLE grades (
    id SERIAL,
    student_id BIGINT UNSIGNED NOT NULL,
    subject_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY fk_grades_students (student_id) REFERENCES students (id),
    FOREIGN KEY fk_grades_subjects (subject_id) REFERENCES subjects (id),
    date_of DATE NOT NULL,
    grade INT UNSIGNED NOT NULL
    )
"""
