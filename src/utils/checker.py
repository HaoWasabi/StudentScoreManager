import re, os
from bll import *

class Checker:
    @staticmethod
    def is_exist_student(student_id):
        student_bll = StudentBLL()
        return student_bll.get_by_id(student_id) is not None

    @staticmethod
    def is_valid_excel_path(filepath: str) -> bool:
        """
        Kiểm tra xem đường dẫn file Excel có hợp lệ và có tồn tại không.
        """
        # Loại bỏ khoảng trắng ở đầu và cuối chuỗi
        filepath = filepath.strip()

        # Danh sách ký tự không hợp lệ cho đường dẫn/tên tệp trong Windows
        invalid_chars = r'[<>"/|?*]'

        # Kiểm tra điều kiện:
        # 1. Không được rỗng
        # 2. Không chứa ký tự không hợp lệ
        # 3. Phải có phần mở rộng .xls hoặc .xlsx
        # 4. File phải tồn tại trong hệ thống
        
        if not filepath:
            print("Excel path must not be empty.")
            return False
        
        elif re.search(invalid_chars, filepath):
            print("Excel path must not contain any of the following characters: < > \" / | ? *")
            return False
        
        elif not filepath.lower().endswith(('.xls', '.xlsx')):
            print("Excel path must have .xls or .xlsx extension.")
            return False
        
        elif not os.path.isfile(filepath):
            print("Excel file not found.")
            return False
        
        return True