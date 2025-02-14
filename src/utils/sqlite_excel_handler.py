import os
import sqlite3
import pandas as pd
from bll.excel_bll import ExcelBLL
from dto.student_dto import StudentDTO
from typing import List

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Lấy thư mục gốc của dự án
db_path = os.path.join(base_dir, "db.sqlite3")
if ExcelBLL().get_all():
    excel_path = ExcelBLL().get_all()[0].get_path()  
else:
    excel_path = os.path.join(base_dir, "ClassManager.xlsx")
    print("Excel path not found in database. Using default path.")

class SQLiteExcelHandler:
    @staticmethod
    def export_to_excel(students: List[StudentDTO], excel_path: str = excel_path):
        """
        Xuất danh sách sinh viên ra file Excel:
        - Nếu file Excel chưa tồn tại: Ghi toàn bộ danh sách vào file mới.
        - Nếu file đã tồn tại: Cập nhật sinh viên có `student_id` trùng hoặc thêm mới nếu chưa có.
        """
        try:
            if not students:
                print("⚠ No data to export.")
                return

            # Chuyển danh sách StudentDTO thành DataFrame
            new_data = pd.DataFrame({
                "student_id": [s.get_student_id() for s in students],
                "name": [s.get_name() for s in students],
                "score": [s.get_score() for s in students],
            })

            # Kiểm tra nếu file Excel đã tồn tại
            if os.path.exists(excel_path):
                existing_data = pd.read_excel(excel_path, sheet_name="student")
                
                # Đảm bảo cột student_id là kiểu số để tránh lỗi merge
                existing_data["student_id"] = existing_data["student_id"].astype(int)
                
                # Hợp nhất dữ liệu, ưu tiên thông tin mới nhất
                merged_data = pd.concat([existing_data, new_data]).drop_duplicates(subset=["student_id"], keep="last")
            else:
                merged_data = new_data  # Nếu chưa có file, dùng dữ liệu mới

            # Xuất dữ liệu ra file Excel
            with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
                merged_data.to_excel(writer, sheet_name="student", index=False)
                print("✅ Successfully updated student data in Excel.")

            print(f"🎉 Export completed: Data has been saved to {excel_path}")
        except Exception as e:
            print(f"❌ Error during export: {e}")

    @staticmethod
    def import_from_excel(excel_path: str = excel_path, mode: str = "replace"):
        """
        Nhập dữ liệu từ file Excel vào SQLite và xóa các student_id không tồn tại trong file Excel.
        """
        try:
            conn = sqlite3.connect(db_path)
            xls = pd.ExcelFile(excel_path)
            if 'student' not in xls.sheet_names:
                print("⚠ Sheet 'student' not found in the Excel file.")
                return

            df = pd.read_excel(xls, sheet_name='student')
            if df.empty:
                print("⚠ Skipping sheet 'student' (No data found).")
                return

            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student (
                    student_id TEXT PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    class TEXT
                )
            """)
            placeholders = ', '.join(['?' for _ in df.columns])
            update_clause = ', '.join([f'{col}=excluded.{col}' for col in df.columns[1:]])
            query = f"""
                INSERT INTO student ({', '.join(df.columns)})
                VALUES ({placeholders})
                ON CONFLICT(student_id) DO UPDATE SET {update_clause}
            """
            cursor.executemany(query, df.values.tolist())
            
            if mode == "replace":
                # Xóa các student_id trong database không tồn tại trong file Excel
                student_ids_in_excel = tuple(df['student_id'].tolist())
                if student_ids_in_excel:
                    cursor.execute(f"DELETE FROM student WHERE student_id NOT IN ({', '.join(['?'] * len(student_ids_in_excel))})", student_ids_in_excel)
                    print("✅ Removed students not found in Excel.")

            conn.commit()
            print("✅ Successfully imported sheet 'student' into table 'student'.")
        
        except Exception as e:
            print(f"❌ Error during import: {e}")
        
        finally:
            if conn:
                conn.close()