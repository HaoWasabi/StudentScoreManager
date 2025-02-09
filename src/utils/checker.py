from bll import *

class Checker:
    @staticmethod
    def is_exist_student(student_id):
        student_bll = StudentBLL()
        return student_bll.get_by_id(student_id) is not None
