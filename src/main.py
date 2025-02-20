import os
from bll import * 
from cli import *
from dto import *
from utils.default import *

def create_all_tables():
    arr_table =  [StudentBLL(), FileBLL()]
    for table in arr_table:
        table.create_table()
    FileBLL().insert(FileDTO(1, default_text_path))
    FileBLL().insert(FileDTO(2, default_excel_path))
        
if __name__ == '__main__':
    create_all_tables()
    MainCLI()