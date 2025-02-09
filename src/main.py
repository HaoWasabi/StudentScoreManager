from bll import * 
from cli import *

def create_all_tables():
    student_bll = StudentBLL()
    student_bll.create_table()
        
if __name__ == '__main__':
    create_all_tables()
    StudentCLI()