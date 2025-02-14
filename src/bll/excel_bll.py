from .singleton import Singleton
from dal.excel_dal import ExcelDAL
from dto.excel_dto import ExcelDTO
from typing import Optional, List

class ExcelBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__excel_dal = ExcelDAL()
            self._initialized = True
            
    def create_table(self):
        self.__excel_dal.create_table()
        
    def drop_table(self):
        self.__excel_dal.drop_table()
        
    def clear_table(self):
        self.__excel_dal.clear_table()
        
    def insert(self, excel: ExcelDTO) -> bool:
        return self.__excel_dal.insert(excel)
    
    def delete(self, path: int) -> bool:
        return self.__excel_dal.delete(path)
    
    def get_all(self) -> List[ExcelDTO]:
        return self.__excel_dal.get_all()
    
    def get_by_path(self, path: int) -> Optional[ExcelDTO]:
        return self.__excel_dal.get_by_path(path)
    