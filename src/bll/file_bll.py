from .singleton import Singleton
from dal.file_dal import FileDAL
from dto.file_dto import FileDTO
from typing import Optional, List

class FileBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__file_dal = FileDAL()
            self._initialized = True
            
    def create_table(self):
        self.__file_dal.create_table()
        
    def drop_table(self):
        self.__file_dal.drop_table()
        
    def clear_table(self):
        self.__file_dal.clear_table()
        
    def insert(self, file: FileDTO) -> bool:
        return self.__file_dal.insert(file)
    
    def update(self, file: FileDTO) -> bool:
        return self.__file_dal.update(file)
    
    def delete(self, id: int) -> bool:
        return self.__file_dal.delete(id)
    
    def get_all(self) -> List[FileDTO]:
        return self.__file_dal.get_all()
    
    def get_by_id(self, id_: int) -> Optional[FileDTO]:
        return self.__file_dal.get_by_id(id_)