from bll.student_bll import StudentBLL
from dto.student_dto import StudentDTO
from utils.terminal_handler import TerminalHandler
from utils.sqlite_excel_handler import SQLiteExcelHandler
from utils.sqlite_text_handler import SQLiteTextHandler
from .base_cli import BaseCLI

class StudentCLI(BaseCLI):
    def __init__(self):
        self.__student_bll = StudentBLL()
        super().__init__()
        
    def run(self):
        while True:
            print('''\n
            Students manager menu:
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
                self.update_database_by_text()
            elif choice == '5':
                self.update_database_by_excel()
            elif choice == '6':
                students = self.__student_bll.get_all()
                SQLiteExcelHandler().export_to_excel(students=students)
            elif choice == '7':
                self.reset_all_score()
            elif choice == '8':
                break
            else:
                print("Invalid choice. Please try again.")
                
    def mini_menu(self, student_id: int):
        while True:
            print(f'''\n
            Student info menu:
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
            
    def update_database_by_text(self):
        while True:
            print('''\n
            Updating database by text menu:
                1. Replace by text
                2. Squash by text
                3. Back
            ''')
            choice = input("Enter your choice: ")
            TerminalHandler.clear()
            
            if choice == '1':
                SQLiteTextHandler().import_from_text(mode="replace")
                break
            elif choice == '2':
                SQLiteTextHandler().import_from_text(mode="squash")
                break
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
                
    def update_database_by_excel(self):
        while True:
            print('''\n
            Updating database by excel menu:
                1. Replace by excel
                2. Squash by excel
                3. Back
            ''')
            choice = input("Enter your choice: ")
            TerminalHandler.clear()
            
            if choice == '1':
                SQLiteExcelHandler().import_from_excel(mode="replace")
                break
            elif choice == '2':
                SQLiteExcelHandler().import_from_excel(mode="squash")
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
                
            while True:
                choice = input("\nDo you want to sort this list? (y/n): ")
                if choice == 'y':
                    while True:
                        print('''
                            Sorting menu:
                                    1. Sort by name
                                    2. Sort by score
                                    3. Sort by last name
                                    4. Sort by first name
                                    5. Back
                            ''')
                        choice = input("Enter your choice: ")
                        TerminalHandler.clear()
                        
                        if choice == '1':
                            by = "name"
                        elif choice == '2':
                            by = "score"
                        elif choice == '3':
                            by = "last_name"
                        elif choice == '4':
                            by = "first_name"
                        elif choice == '5':
                            break
                        else:
                            print("Invalid choice. Please try again.")
                            continue
                        
                        choice = input("Enter number to sort ASC (1) or DESC (2): ")                        
                        while choice not in ['1', '2']:
                            choice = input("Invalid choice. Enter number to sort ASC (1) or DESC (2): ")
                        TerminalHandler.clear()
                        
                        direction = "ASC" if choice == '1' else "DESC"
                        students = self.__student_bll.sort(by, direction)
                        for student in students:
                            print(student)
                        
                        while True:
                            choice = input("Do you want to save this list to Excel? (y/n): ")
                            if choice == 'y':
                                SQLiteExcelHandler().export_to_excel(students=students)
                                break
                            elif choice == 'n':
                                break
                        
                        break    
                        
                elif choice == 'n':
                    break
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
        if score == '-': score = str(student.get_score())
        
        if self.is_valid_update(name, score):
            student = StudentDTO(student_id, name, float(score))
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
            elif not isinstance(score, float) and float(score) < 0:
                print("Score must be a number and greater than 0.")
                return False
            return True
        except Exception as e:
            print(e)
            return False
