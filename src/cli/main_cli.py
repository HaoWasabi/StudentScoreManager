from .student_cli import StudentCLI
from .excel_cli import ExcelCLI
from .base_cli import BaseCLI
from utils.terminal_handler import TerminalHandler

class MainCLI(BaseCLI):
    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            print('''\n
            Main menu:
                1. Manage students
                2. Manage excel
                3. Exit
            ''')
            choice = input("Enter your choice: ")
            TerminalHandler.clear()
            
            if choice == '1':
                StudentCLI()
            elif choice == '2':
                ExcelCLI()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")