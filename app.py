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
    studentID = IntegerField()
    name = TextField()
    nickname = TextField()
    age = IntegerField()
    school_class = TextField()
    registration_date = DatatTime()

class lessons(Model):
    name = TextField()
    lessonID = IntegerField()

class registered_lessons(Model):
    id = IntegerField()
    studentID = IntegerField()
    lessoneID = IntegerField()
# functiones ----------------------------------------------------------------------------------
def input_data(type_data, message):
    while True:
        try:
            data = input(message)
            if type_data == 'age':
                data = int(data)
                if data <= 120 and data > 0:
                    return data
            elif type_data == 'id':
                data = int(data)
                if data > 0:
                    return data
            elif type_data == 'name':
                if len(data) < 20 and data.isalpha():
                    return data.lower()
            elif type_data == 'text':
                if len(data) < 50 :
                    return data
        except ValueError: 
            pass
        print('Data is invalid')

def create_student():
    print("Enter the new student’s information:")
    
    # Take a unique ID
    while True:
        student_ID = input_data('id', 'student ID: ')
        if student.get('studentID', student_ID) == None:
            break
        print('The ID is reserved. Enter another ID')

    student_name = input_data('name', 'student name: ')
    student_nickname = input_data('name', 'student nickname: ')
    student_age = input_data('age', 'student age, any number of 1 to 120: ')
    student_school_class = input_data('text', 'student school class: ')
    student_lessons = input_data('text', '\nStudent lessons example: Lesson1-Lesson2-Lesson5 :')
    ok = input_data('text', 'Enter (y) to confirm or enter any button to cancel: ')

    if (ok == 'y' or ok == 'Y'):
        student.create(studentID=student_ID, name=student_name, nickname=student_nickname, age=student_age, school_class=student_school_class, registration_date=datetime.now())
        
        # Adding new lessons + lessons in which the student is registered
        lessons_arr = student_lessons.split('-')
        for item in lessons_arr:
            if lesson.get('name', item) == None:
                lesson.create(name=item)
                
            lesson_ID = lesson.get('name', item)['lessonID']
            if registered_lesson.find('studentID = ' + str(student_ID) + ' AND lessonID ', '=', lesson_ID) == None:
                registered_lesson.create(studentID=student_ID, lessonID=lesson_ID)
            
        print('\nThe operation was completed successfully')
    else:
        print('\nIt was rejected or the data entered is incorrect')

def show_student():
    student_ID = input_data('id', 'Enter student ID: ')
    student_info = student.get('studentID', student_ID)
    if (student_info == None):
        print('Student not found')
    else:
        print('\n-------------Student info-------------')
        print(student_info)
        
        print('\n-------------Student lessons-------------')
        student_lessons = registered_lesson.find('studentID', '=', student_ID)
        count = 0
        for item in student_lessons:
            record = lesson.get('lessonID', item['lessonID'])
            count += 1
            print(count, '- ', record['name'])

def delete_student():
    student_ID = input_data('id', 'Enter student ID: ')
    student_info = student.get('studentID', student_ID)
    if (student_info == None):
        print('Student not found')
    else:
        print(student_info)
        ok = input_data('text', 'Enter (y) to confirm or enter any button to cancel: ')
        if (ok == 'y' or ok == 'Y'):
            registered_lesson._findAndDelete('studentID', '=', student_ID)
            student._deleteByID('studentID', student_ID)
            print('\nThe operation was completed successfully')
        else:
            print('\nIt was rejected')

def update_student():
    student_ID = input_data('id', 'Enter student ID: ')
    student_info = student.get('studentID', student_ID)
    if (student_info == None):
        print('Student not found')
    else:
        print(student_info)
        print('\nEnter the student\'s new information: ')

        student_name = input_data('name', 'student name: ')
        student_nickname = input_data('name', 'student nickname: ')
        student_age = input_data('age', 'student age, any number of 1 to 120: ')
        student_school_class = input_data('text', 'student school class: ')
        student_lessons = input_data('text', '\nStudent lessons example: Lesson1-Lesson2-Lesson5 :')

        ok = input_data('text', 'Enter (y) to confirm or enter any button to cancel: ')
        if (ok == 'y' or ok == 'Y'):
            student.name = student_name
            student.nickname = student_nickname
            student.age = student_age
            student.school_class = student_school_class

            registered_lesson._findAndDelete('studentID', '=', student_ID)
            student._update("studentID", student_ID)

            # Adding new lessons + lessons in which the student is registered
            lessons_arr = student_lessons.split('-')
            for item in lessons_arr:
                if lesson.get('name', item) == None:
                    lesson.create(name=item)
                    
                lesson_ID = lesson.get('name', item)['lessonID']
                if registered_lesson.find('studentID = ' + str(student_ID) + ' AND lessonID ', '=', lesson_ID) == None:
                    registered_lesson.create(studentID=student_ID, lessonID=lesson_ID)

            print('\nThe operation was completed successfully')
        else:
            print('\nIt was rejected or the data entered is incorrect')

# ----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    student = students()
    lesson = lessons()
    registered_lesson = registered_lessons()
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
