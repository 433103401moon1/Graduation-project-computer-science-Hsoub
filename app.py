# support for print by arabic language
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import datetime
from Model import Model
from Field import *
from Database import Database

# variables ----------------------------------------------------------------------------------
student_ID = 0
student_name = ''
student_nickname = ''
student_age = 0
student_school_class = ''
student_lessons = ''
ok = ''

# ----------------------------------------------------------------------------------------------
Model.db = Database('school.db')
Model.connection = Model.db.connect()

class students(Model):
    id = IntegerField()
    name = TextField()
    nickname = TextField()
    age = IntegerField()
    school_class = TextField()
    registration_date = DatatTime()

class lessons(Model):
    name = TextField()
    studentID = IntegerField()
    lessonsID = IntegerField()

# functiones ----------------------------------------------------------------------------------
def create_student():
    print("Enter the new student’s information:")
    
    student_ID = int(input('student ID: '))
    student_name = input('student name: ')
    student_nickname = input('student nickname: ')
    student_age = int(input('student age: '))
    student_school_class = input('student school class: ')
    student_lessons = input('\nStudent lessons example: Lesson1-Lesson2-Lesson5 :')
    ok = input('Enter (y) to confirm or enter any button to cancel: ')

    if (ok == 'y' or ok == 'Y'):
        student.create(id=student_ID, name=student_name, nickname=student_nickname, age=student_age, school_class=student_school_class, registration_date=datetime.now())
        
        arr = student_lessons.split('-')
        for item in arr:
            lesson.create(name=item, studentID=student_ID)

        print('\nThe operation was completed successfully')
    else:
        print('\nIt was rejected or the data entered is incorrect')

def show_student():
    student_ID = int(input('Enter student ID: '))
    student_info = student.get(student_ID)
    if (student_info == None):
        print('Student not found')
    else:
        print('\n-------------Student info-------------')
        print(student_info)
        
        print('\n-------------Student lessons-------------')
        student_lessons = lesson.find('studentID', '=', student_ID)
        for item in student_lessons:
            print(item['name'])

def delete_student():
    student_ID = int(input('Enter student ID: '))
    student_info = student.get(student_ID)
    if (student_info == None):
        print('Student not found')
    else:
        print(student_info)
        ok = input('If you want to delete the student, enter (y) or any key to cancel: ')
        if (ok == 'y' or ok == 'Y'):
            lesson._findAndDelete('studentID', '=', student_ID)
            student._deleteByID(student_ID)
            print('\nThe operation was completed successfully')
        else:
            print('\nIt was rejected')

def update_student():
    student_ID = int(input('Enter student ID: '))
    student_info = student.get(student_ID)
    if (student_info == None):
        print('Student not found')
    else:
        print(student_info)
        print('\nEnter the student\'s new information: ')

        student_name = input('student name: ')
        student_nickname = input('student nickname: ')
        student_age = int(input('student age: '))
        student_school_class = input('student school class: ')
        student_lessons = input('\nStudent lessons example: Lesson1-Lesson2-Lesson5 :')

        ok = input('Enter (y) to confirm or enter any button to cancel: ')
        if (ok == 'y' or ok == 'Y'):
            student.name = student_name
            student.nickname = student_nickname
            student.age = student_age
            student.school_class = student_school_class
            student._update(student_ID)

            lesson._findAndDelete('studentID', '=', student_ID)
            arr = student_lessons.split('-')
            for item in arr:
                lesson.create(name=item, studentID=student_ID)

            print('\nThe operation was completed successfully')
        else:
            print('\nIt was rejected or the data entered is incorrect')

# ----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    student = students()
    lesson = lessons()
    
    play = True
    while play:
        chosen = input("""
=================================================================
Please choose the operation you want to perform:
* To add a student, click on the letter:----------------- a
* To delete a student, click on the letter:-------------- d
* To modify a student’s information, click on the letter: u
* To view student information, click on the letter:------ s
* To exit the program, click on the letter:-------------- e 
===================================================================\n
""")
        if (chosen == 'a' or chosen == 'A'):
            create_student()
            
        elif (chosen == 'd' or chosen == 'D'):
            delete_student()

        elif (chosen == 'u' or chosen == 'U'):
            update_student()

        elif (chosen == 's' or chosen == 'S'):
            show_student()

        elif (chosen == 'e' or chosen == 'E'):
            print('\nThe program has ended')
            play = False