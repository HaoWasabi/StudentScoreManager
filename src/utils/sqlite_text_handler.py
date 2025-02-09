import os
import sqlite3

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path = os.path.join(base_dir, "db.sqlite3")
default_text_path = os.path.join(base_dir, "ClassManager.txt")

class SQLiteTextHandler:
    @staticmethod
    def import_from_text(text_path: str = default_text_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            with open(text_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                
            table_name = None
            columns = []
            data = []
            student_ids = set()
            
            for line in lines:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                
                if line.startswith("$"):
                    table_name = line[1:].strip()
                    if table_name.lower() != "student":
                        table_name = None
                    else:
                        columns = []
                        data = []
                        student_ids = set()
                elif table_name:
                    values = line.split("|")
                    if not columns:
                        columns = [col.strip() for col in values]
                    else:
                        student_ids.add(values[0].strip())  # Lấy student_id
                        data.append([val.strip() for val in values])
            
            if table_name == "student" and data:
                SQLiteTextHandler._upsert_student_data(cursor, columns, data, student_ids)
            
            conn.commit()
            print(f"🎉 Import completed: Data from {text_path} has been added to {db_path}")
        except Exception as e:
            print(f"❌ Error during import: {e}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def _upsert_student_data(cursor, columns, data, student_ids):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                score INTEGER DEFAULT 0
            )
        """)
        
        placeholders = ', '.join(['?' for _ in columns])
        update_clause = ', '.join([f'{col}=excluded.{col}' for col in columns if col != "student_id"])
        
        query = f"""
            INSERT INTO student ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT(student_id) DO UPDATE SET {update_clause}
        """
        
        cursor.executemany(query, data)
        
        # Xóa các sinh viên không có trong file text
        cursor.execute("DELETE FROM student WHERE student_id NOT IN ({})".format(
            ','.join('?' * len(student_ids))
        ), tuple(student_ids))
        
        print(f"✅ Successfully upserted data into table 'student' and removed missing records.")
