# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: test_excel.py
# @Time : 2022/11/27 11:48
import sys
from pathlib import Path
from core.excel_kdt import data_by_excel, create_case

test_dir = Path(__file__).parent.parent / 'excel_data/'
_case_count = 0  # 用例数量
file_list = test_dir.glob('test_*.xlsx')  # 自动收集excel文件

for file in file_list:
    data = data_by_excel(file)

    for case in create_case(data):
        print('case99999999999999999999999',case)
        _case_count += 1
        globals()[f"Test_{_case_count}"] = case
