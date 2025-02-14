class ExcelDTO:
    def __init__(self, path: str):
        self.__path = path
    
    def __str__(self):
        return f"Excel path = {self.__path}"
    
    def get_path(self):
        return self.__path
    
    def set_path(self, path: str):
        self.__path = path