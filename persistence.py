# file: persistence.py

import sqlite3
import atexit


# Data Transfer Objects:
class Student(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Assignment(object):
    def __init__(self, num, expected_output):
        self.num = num
        self.expected_output = expected_output


class Grade(object):
    def __init__(self, student_id, assignment_num, grade):
        self.student_id = student_id
        self.assignment_num = assignment_num
        self.grade = grade


# Data Access Objects:
# All of these are meant to be singletons
class _Students:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, student):
        self._conn.execute("""
               INSERT INTO students (id, name) VALUES (?, ?)
           """, [student.id, student.name])

    def find(self, student_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name FROM students WHERE id = ?
        """, [student_id])

        return Student(*c.fetchone())


class _Assignments:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, assignment):
        self._conn.execute("""
                INSERT INTO assignments (num, expected_output) VALUES (?, ?)
        """, [assignment.num, assignment.expected_output])

    def find(self, num):
        c = self._conn.cursor()
        c.execute("""
                SELECT num,expected_output FROM assignments WHERE num = ?
            """, [num])

        return Assignment(*c.fetchone())


class _Grades:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, grade):
        self._conn.execute("""
            INSERT INTO grades (student_id, assignment_num, grade) VALUES (?, ?, ?)
        """, [grade.student_id, grade.assignment_num, grade.grade])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT student_id, assignment_num, grade FROM grades
        """).fetchall()

        return [Grade(*row) for row in all]


# The Repository
class _Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('grades.db')
        self.students = _Students(self._conn)
        self.assignments = _Assignments(self._conn)
        self.grades = _Grades(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE students (
                id      INT         PRIMARY KEY,
                name    TEXT        NOT NULL
            );

            CREATE TABLE assignments (
                num                 INT     PRIMARY KEY,
                expected_output     TEXT    NOT NULL
            );

            CREATE TABLE grades (
                student_id      INT     NOT NULL,
                assignment_num  INT     NOT NULL,
                grade           INT     NOT NULL,

                FOREIGN KEY(student_id)     REFERENCES students(id),
                FOREIGN KEY(assignment_num) REFERENCES assignments(num),

                PRIMARY KEY (student_id, assignment_num)
            );
        """)


# see code in previous version...

# the repository singleton
repo = _Repository()
atexit.register(repo._close)