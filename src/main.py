from bll import * 
from cli import *
from dto import *

def create_all_tables():
    arr_table =  [StudentBLL(), ExcelBLL()]
    for table in arr_table:
        table.create_table()
        
if __name__ == '__main__':
    create_all_tables()
    MainCLI()