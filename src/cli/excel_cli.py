import os
from bll.file_bll import FileBLL
from dto.file_dto import FileDTO
from utils.checker import Checker
from utils.terminal_handler import TerminalHandler
from .base_cli import BaseCLI
from utils.default import *

class ExcelCLI(BaseCLI):
    def __init__(self):
        self.__file_bll = FileBLL()
        super().__init__()
        
    def run(self):
        try:    
            while True:
                print('''\n
                Excel manager menu:
                    1. Update excel path
                    2. Set back to default
                    3. Print excel path
                    4. Back
                ''')
                choice = input("Enter your choice: ")
                TerminalHandler.clear()
                
                if choice == '1':
                    self.update()
                elif choice == '2':
                    self.set_to_default()
                elif choice == '3':
                    print(f"Excel path: {self.__file_bll.get_by_id(2).get_path()}")
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
            
    def update(self):
        new_path = input("Enter path (enter '-' if no change): ")
        TerminalHandler.clear()
        
        if new_path == "-": new_path = self.__file_bll.get_by_id(2).get_path()
        if not Checker.is_valid_excel_path(new_path):
            return
        
        excel = FileDTO(2, new_path)
        if self.__file_bll.update(excel):
            print("Excel updated successfully.")
        else:
            print("Error updating excel.")
            
    def set_to_default(self):
        excel = FileDTO(2, default_excel_path)
        if self.__file_bll.update(excel):
            print("Excel updated successfully.")
        else:
            print("Error updating excel.")
            
    def is_valid(self, path: str) -> bool:
        return Checker.is_valid_excel_path(path)