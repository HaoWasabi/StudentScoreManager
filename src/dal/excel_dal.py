import sqlite3
from typing import Optional, List
from dto.excel_dto import ExcelDTO
from .base_dal import BaseDAL, logger

class ExcelDAL:
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        try:
            self.open_connection()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS excel (
                    path TEXT PRIMARY KEY
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error creating table excel: {e}")
        finally:
            self.close_connection()
            
    def drop_table(self):
        try:
            self.open_connection()
            self.cursor.execute('''DROP TABLE IF EXISTS excel''')
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error dropping table excel: {e}")
        finally:
            self.close_connection()
    
    def clear_table(self):
        try:
            self.open_connection()
            self.cursor.execute('''DELETE FROM excel''')
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error clearing table excel: {e}")
        finally:
            self.close_connection()
            
    def insert(self, excel: ExcelDTO) -> bool:
        try:
            self.open_connection()
            self.cursor.execute('''
                INSERT INTO excel (path) VALUES (?)
            ''', (excel.get_path(),))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error inserting excel: {e}")
            return False
        finally:
            self.close_connection()
            
    def update(self, excel: ExcelDTO) -> bool:
        try:
            self.open_connection()
            self.cursor.execute('''
                UPDATE excel SET path = ?
            ''', (excel.get_path(),))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error updating excel: {e}")
            return False
        finally:
            self.close_connection()
            
    def delete(self, path: str) -> bool:
        try:
            self.open_connection()
            self.cursor.execute('''
                DELETE from excel WHERE path = ?
            ''', (path,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting excel: {e}")
            return False
        finally:
            self.close_connection()
            
    def get_all(self) -> List[ExcelDTO]:
        try:
            self.open_connection()
            self.cursor.execute('''SELECT * FROM excel''')
            return [ExcelDTO(*excel) for excel in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error getting all excels: {e}")
            return []
        finally:
            self.close_connection()
    
    def get_by_path(self, path: str) -> Optional[ExcelDTO]:
        try:
            self.open_connection()
            self.cursor.execute('''SELECT * FROM excel WHERE path = ?''', (path,))
            row = self.cursor.fetchone()
            return ExcelDTO(*row) if row else None
        except sqlite3.Error as e:
            logger.error(f"Error getting excel by path: {e}")
            return None
        finally:
            self.close_connection()