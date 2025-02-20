import sqlite3
from typing import Optional, List
from dto.student_dto import StudentDTO
from .base_dal import BaseDAL, logger

class StudentDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        try:
            self.open_connection()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS student (
                    student_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    score REAL DEFAULT 0
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error creating table student: {e}")
        finally:
            self.close_connection()
    
    def drop_table(self):
        try:
            self.open_connection()
            self.cursor.execute('''DROP TABLE IF EXISTS student''')
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error dropping table student: {e}")
        finally:
            self.close_connection()
            
    def clear_table(self):
        try:
            self.open_connection()
            self.cursor.execute('''DELETE FROM student''')
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error clearing table student: {e}")
        finally:
            self.close_connection()
                    
    def insert(self, student: StudentDTO) -> bool:
        try:
            self.open_connection()
            self.cursor.execute('''
                INSERT INTO student (student_id, name, score) VALUES (?, ?, ?)
            ''', (student.get_student_id(), student.get_name(), student.get_score()))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error inserting student: {e}")
            return False
        finally:
            self.close_connection()
            
    def update(self, student: StudentDTO) -> bool:
        try:
            self.open_connection()
            self.cursor.execute('''
                UPDATE student SET name = ?, score = ? WHERE student_id = ?
            ''', (student.get_name(), student.get_score(), student.get_student_id()))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error updating student: {e}")
            return False
        finally:
            self.close_connection()
            
    def reset_all_score(self) -> bool:
        try:
            self.open_connection()
            self.cursor.execute('''UPDATE student SET score = 0''')
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error reseting all students: {e}")
            return False
        finally:
            self.close_connection()
            
    def delete(self, student_id: int) -> bool:
        try:
            self.open_connection()
            self.cursor.execute('''DELETE FROM student WHERE student_id = ?''', (student_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting student: {e}")
            return False
        finally:
            self.close_connection()
        
    def get_all(self) -> List[StudentDTO]:
        try:
            self.open_connection()
            self.cursor.execute('''SELECT * FROM student''')
            return [StudentDTO(*student) for student in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error getting all students: {e}")
            return []
        finally:
            self.close_connection()
            
    def get_by_id(self, student_id: int) -> Optional[StudentDTO]:
        try:
            self.open_connection()
            self.cursor.execute('''SELECT * FROM student WHERE student_id = ?''', (student_id,))
            row = self.cursor.fetchone()
            return StudentDTO(*row) if row else None
        except sqlite3.Error as e:
            logger.error(f"Error getting student by id: {e}")
            return None
        finally:
            self.close_connection()
            
    def sort(self, by: str = "name", direction: str = "ASC") -> List["StudentDTO"]:
        try:
            self.open_connection()
            
            # Danh sách cột hợp lệ
            valid_columns = ["student_id", "name", "score", "last_name", "first_name"]
            if by not in valid_columns:
                by = "name"
            if direction not in ["ASC", "DESC"]:
                direction = "ASC"

            # Trường hợp đặc biệt: Sắp xếp theo họ hoặc tên chính
            if by == "last_name":
                order_clause = "SUBSTR(name, 1, INSTR(name || ' ', ' ') - 1)"
            elif by == "first_name":
                order_clause = "SUBSTR(name, LENGTH(name) - INSTR(REVERSE(name) || ' ', ' ') + 2)"
            else:
                order_clause = by  # student_id, score, name vẫn giữ nguyên

            # Thực thi truy vấn SQL
            self.cursor.execute(f'''SELECT * FROM student ORDER BY {order_clause} {direction}''')
            return [StudentDTO(*student) for student in self.cursor.fetchall()]

        except sqlite3.Error as e:
            logger.error(f"Error sorting students: {e}")
            return []
        finally:
            self.close_connection()
