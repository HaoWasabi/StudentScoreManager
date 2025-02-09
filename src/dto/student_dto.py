class StudentDTO:
    def __init__(self, student_id: int, name: str, score: int = 0):
        self.__student_id = student_id
        self.__name = name
        self.__score = score
        
    def __str__(self):
        return f"Student_id:{self.__student_id}, name={self.__name}, score={self.__score}"
    
    def get_student_id(self):
        return self.__student_id
    
    def get_name(self):
        return self.__name
    
    def get_score(self):
        return self.__score
    
    def set_student_id(self, student_id: int):
        self.__student_id = student_id
        
    def set_name(self, name: str):
        self.__name = name
        
    def set_score(self, score: int):
        self.__score = score