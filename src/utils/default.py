import os
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Lấy thư mục gốc của dự án
db_path = os.path.join(base_dir, "db.sqlite3")
                       
default_excel_path = os.path.join(base_dir, "ClassManager.xlsx")
default_text_path = os.path.join(base_dir, "ClassManager.txt")
default_db_path = os.path.join(base_dir, "db.sqlite3")