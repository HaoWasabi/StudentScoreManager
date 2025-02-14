from bll.excel_bll import ExcelBLL
from dto.excel_dto import ExcelDTO
from utils.checker import Checker
from utils.terminal_handler import TerminalHandler
from .base_cli import BaseCLI

class ExcelCLI(BaseCLI):
    def __init__(self):
        self.__excel_bll = ExcelBLL() 
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
                
                if self.__excel_bll.get_all():
                    old_path = self.__excel_bll.get_all()[0].get_path()
                
                if choice == '1':
                    self.update(old_path)
                elif choice == '2':
                    self.set_to_default(old_path)
                elif choice == '3':
                    print(f"Excel path: {old_path}")
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
            
    def update(self, old_path: str):
        new_path = input("Enter path (enter '-' if no change): ")
        TerminalHandler.clear()
        
        if new_path == "-": new_path = old_path
        if not Checker.is_valid_excel_path(new_path):
            return
        
        excel = ExcelDTO(new_path)
        if self.__excel_bll.delete(old_path) and self.__excel_bll.insert(excel):
            print("Excel updated successfully.")
        else:
            print("Error updating excel.")
            
    def set_to_default(self, old_path: str):
        excel = ExcelDTO()
        if self.__excel_bll.delete(old_path) and self.__excel_bll.insert(excel):
            print("Excel updated successfully.")
        else:
            print("Error updating excel.")
            
    def is_valid(self, path: str) -> bool:
        return Checker.is_valid_excel_path(path)