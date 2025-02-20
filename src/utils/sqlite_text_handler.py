import os
import sqlite3
from bll.file_bll import FileBLL
from .default import *

text = FileBLL().get_by_id(1)
if text:
    text_path = text.get_path()
else:
    text_path = default_text_path
    print("Text path not found in database. Using default text path.")

class SQLiteTextHandler:
    @staticmethod
    def import_from_text(text_path: str = text_path, mode: str = "replace"):
        try:
            conn = sqlite3.connect(default_db_path)
            cursor = conn.cursor()
            
            with open(text_path, "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip() and not line.startswith("#")]

            table_name, columns, data = None, [], []
            for line in lines:
                if line.startswith("$"):
                    table_name = line[1:].strip().lower()
                    if table_name != "student":
                        table_name = None
                    else:
                        columns, data = [], []
                elif table_name:
                    values = [val.strip() for val in line.split("|")]
                    if not columns:
                        columns = values
                    else:
                        data.append(values)
            
            if table_name == "student" and data:
                SQLiteTextHandler._upsert_student_data(cursor, columns, data, mode)
            
            conn.commit()
            print(f"🎉 Import completed: Data from {text_path} has been added to {default_db_path}")
        except Exception as e:
            print(f"❌ Error during import: {e}")
        finally:
            conn.close()

    @staticmethod
    def _upsert_student_data(cursor, columns, data, mode):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                score REAL DEFAULT 0
            )
        """)

        placeholders = ', '.join(['?' for _ in columns])
        update_clause = ', '.join([f"{col}=excluded.{col}" for col in columns if col != "student_id"])

        query = f"""
            INSERT INTO student ({', '.join(columns)}) VALUES ({placeholders})
            ON CONFLICT(student_id) DO UPDATE SET {update_clause}
        """

        cursor.executemany(query, data)

        if mode == "replace":
            student_ids = tuple(row[0] for row in data)
            cursor.execute(f"DELETE FROM student WHERE student_id NOT IN ({','.join('?' * len(student_ids))})", student_ids)

        print(f"✅ Successfully {'replaced' if mode == 'replace' else 'synchronized'} student data.")
