import os

class FileDTO:
    def __init__(self, file_id: int, path: str):
        self.__file_id = file_id
        self.__path = path
        
    def __str__(self):
        return f"File id = {self.__file_id}, path = {self.__path}"
    
    def get_file_id(self):
        return self.__file_id
    
    def set_file_id(self, file_id):  
        self
        self.__file_id = file_id
    
    def get_path(self):
        return self.__path
    
    def set_path(self, path: str):
        self.__path = path