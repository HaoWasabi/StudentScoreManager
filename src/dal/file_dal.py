import sqlite3, os
from typing import Optional, List
from dto.file_dto import FileDTO
from .base_dal import BaseDAL, logger

class FileDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        try:
            self.open_connection()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS file (
                    file_id INTEGER PRIMARY KEY,
                    path TEXT NOT NULL
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error creating table file: {e}")
        finally:
            self.close_connection()
            
    def drop_table(self):
        try:
            self.open_connection()
            self.cursor.execute('''DROP TABLE IF EXISTS file''')
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error dropping table file: {e}")
        finally:
            self.close_connection()
            
    def clear_table(self):
        try:
            self.open_connection()
            self.cursor.execute('''DELETE FROM file''')
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Error clearing table file: {e}")
        finally:
            self.close_connection()
            
    def insert(self, file: FileDTO) -> bool:
        try:
            self.open_connection()
            self.cursor.execute('''
                INSERT INTO file (file_id, path) VALUES (?, ?)
            ''', (file.get_file_id(), file.get_path(),))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error inserting file: {e}")
            return False
        finally:
            self.close_connection()
        
    def update(self, file: FileDTO) -> bool:
        try:
            self.open_connection()
            self.cursor.execute('''
                UPDATE file SET path = ? WHERE file_id = ?
            ''', (file.get_path(), file.get_file_id()))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error updating file: {e}")
            return False
        finally:
            self.close_connection()
            
    def delete(self, file_id: int) -> bool:
        try:
            self.open_connection()
            self.cursor.execute('''
                DELETE FROM file WHERE file_id = ?
            ''', (file_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting file: {e}")
            return False
        finally:
            self.close_connection()
            
    def get_all(self) -> Optional[List[FileDTO]]:
        try:
            self.open_connection()
            self.cursor.execute('''
                SELECT * FROM file
            ''')
            rows = self.cursor.fetchall()
            return [FileDTO(*row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Error getting all files: {e}")
            return None
        finally:
            self.close_connection()
            
    def get_by_id(self, file_id: int) -> Optional[FileDTO]:
        try:
            self.open_connection()
            self.cursor.execute('''
                SELECT * FROM file WHERE file_id = ?
            ''', (file_id,))
            row = self.cursor.fetchone()
            return FileDTO(*row) if row else None
        except sqlite3.Error as e:
            logger.error(f"Error getting file by id: {e}")
            return None
        finally:
            self.close_connection()