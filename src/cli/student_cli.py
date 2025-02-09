from bll.student_bll import StudentBLL
from dto.student_dto import StudentDTO
from utils.checker import Checker
from utils.terminal_handler import TerminalHandler
from utils.sqlite_excel_handler import SQLiteExcelHandler
from utils.sqlite_text_handler import SQLiteTextHandler
import sys
import signal

class StudentCLI:
    def __init__(self):
        self.__student_bll = StudentBLL()
        TerminalHandler.clear()
        signal.signal(signal.SIGINT, self.signal_handler)
        self.run()
        
    def signal_handler(self, signum, frame):
        print("Goodbye!")
        sys.exit(0)
        
    def run(self):
        while True:
            print('''\n
            Student menu:
                1. List students
                2. Find Student
                3. Insert student
                4. Update database by text
                5. Update database by excel
                6. Export to excel
                7. Reset score of all students
                8. Back
            ''')
            choice = input("Enter your choice: ")
            TerminalHandler.clear()
            
            if choice == '1':
                self.get_all()
            elif choice == '2':
                self.get_by_id()
            elif choice == '3':
                self.insert()
            elif choice == '4':
                SQLiteTextHandler().import_from_text()
            elif choice == '5':
                SQLiteExcelHandler().import_from_excel()
            elif choice == '6':
                SQLiteExcelHandler().export_to_excel()
            elif choice == '7':
                self.reset_all_score()
            elif choice == '8':
                break
            else:
                print("Invalid choice. Please try again.")
                
    def mini_menu(self, student_id: int):
        while True:
            print('''\n
            Teacher menu:
                1. Update student
                2. Delete student
                3. Back
            ''')
            choice = input("Enter your choice: ")
            TerminalHandler.clear()
            
            if choice == '1':
                self.update(student_id)
                break
            elif choice == '2':
                self.delete(student_id)
                break
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
            
    def get_all(self):
        TerminalHandler.clear()
        students = self.__student_bll.get_all()
        
        if students:
            for student in students:
                print(student)
        else:
            print("No student found.")
            
    def get_by_id(self):
        student_id = input("Enter student ID:")
        TerminalHandler.clear()
        
        if student_id and student_id.isdigit():
            student = self.__student_bll.get_by_id(int(student_id))
            if student:
                print(student)
                self.mini_menu(student_id)
                
            else:
                print("No student found.")
        else:
            print("Student ID must be a number.")
            
    def insert(self):
        student_id = input("Enter student ID:")
        name = input("Enter student name: ")
        TerminalHandler.clear()
        
        if self.is_valid_insert(student_id, name):
            student = StudentDTO(int(student_id), name)
            if self.__student_bll.insert(student) is True:
                print(f"Student {name} has been created.")
            else:
                print("Create student failed.")

    def update(self, student_id: int):
        name = input("Enter student name (enter '-' if no change): ")
        score = input("Enter score (enter '-' if no change): ")
        TerminalHandler.clear()
        
        student = self.__student_bll.get_by_id(student_id)
        if name == '-': name = student.get_name()
        if score == '-': score = student.get_score()
        
        if self.is_valid_update(name, score):
            student = StudentDTO(student_id, name, int(score))
            if self.__student_bll.update(student) is True:
                print(f"Student {student_id} has been updated.")
                print(student)
            else:
                print("Update student failed.")
    
    def delete(self, student_id: int):
        if self.__student_bll.delete(student_id):
            print(f"Student {student_id} has been deleted.")
        else:
            print("Delete student failed.")
            
    def reset_all_score(self):
        if self.__student_bll.reset_all_score():
            print("All score has been reseted.")
        else:
            print("Reset all scores failed.")
    
    def is_valid_insert(self, student_id, name):
        try:
            if not student_id or not name:
                print("Student ID, name mustn't be emty.")
                return False
            elif not student_id.isdigit():
                print("Student ID must be a number.")
                return False
            return True 
        except Exception as e:
            print(e)
            return False
    
    def is_valid_update(self, name, score='0'):
        try:
            if not name or not score:
                print("Student name mustn't be emty.")
                return False
            elif not score.isdigit():
                print("Student score must be a number.")
                return False
            return True
        except Exception as e:
            print(e)
            return False
