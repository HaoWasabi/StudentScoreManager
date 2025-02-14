import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Lấy thư mục gốc của dự án
default_excel_path = os.path.join(base_dir, "ClassManager.xlsx")

class ExcelDTO:
    def __init__(self, path: str = default_excel_path):
        self.__path = path
    
    def __str__(self):
        return f"Excel path = {self.__path}"
    
    def get_path(self):
        return self.__path
    
    def set_path(self, path: str):
        self.__path = path