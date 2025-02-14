import os
import sqlite3
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Lấy thư mục gốc của dự án
db_path = os.path.join(base_dir, "db.sqlite3")
default_excel_path = os.path.join(base_dir, "ClassManager.xlsx")

class SQLiteExcelHandler:
    @staticmethod
    def export_to_excel(excel_path: str = default_excel_path):
        """
        Xuất dữ liệu từ SQLite ra file Excel.
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student';")
            table = cursor.fetchone()

            if not table:
                print("⚠ Table 'student' not found in the database.")
                return

            with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
                df = pd.read_sql_query("SELECT * FROM student", conn)
                if df.empty:
                    print("⚠ Skipping table 'student' (No data found).")
                else:
                    df.to_excel(writer, sheet_name='student', index=False)
                    print("✅ Successfully exported table 'student' to sheet 'student'.")

            print(f"🎉 Export completed: Data from {db_path} has been saved to {excel_path}")
        except Exception as e:
            print(f"❌ Error during export: {e}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def import_from_excel(excel_path: str = default_excel_path, mode: str = "replace"):
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