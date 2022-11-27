# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: excel_data.py
# @Time : 2022/11/27 11:15
import logging
import pytest
from openpyxl.reader.excel import load_workbook
from selenium import webdriver
from core.kdt import KeyWord

logger = logging.getLogger(__name__)


def filter_empty(old_l):
    """过滤空值"""
    new_l = []
    for i in old_l:
        if i:
            new_l.append(i)
    return new_l


def data_by_excel(file):
    """
    从excel中加载用例数据
    :param file:
    :return:
    """
    wb = load_workbook(file)
    suite_dict = {}  # 以套件名称为key,以用例为value
    for ws in wb.worksheets:
        case_dict = {}  # 以名称为key,以步骤为value的字典
        case_name = ""
        for line in ws.iter_rows(values_only=True):
            _id = line[0]
            if isinstance(_id, int):  # 步骤
                if _id == -1:
                    case_name = line[3]
                    case_dict[case_name] = []  # 以用例名称为Key，创建新的空用例
                elif _id > 0:  # 用例名称
                    case_dict[case_name].append(filter_empty(line))
        suite_dict[ws.title] = case_dict
    return suite_dict


def create_case(test_suite: dict):
    """
    接收从excel而来的多个测试套件的信息，并生成真正的测试用例
    :return:
    """
    for suite_name, case_dict in test_suite.items():
        class Test:
            @classmethod
            def setup_class(cls):
                cls.driver = webdriver.Chrome()

            @classmethod
            def teardown_class(cls):
                cls.driver.quit()

            @pytest.mark.parametrize('case', case_dict.items())
            def test_(self, case):
                name = (case[0])
                logger.info(f"----------------{case[0]}测试开始----------------")
                print(f"----------------{case[0]}测试开始----------------")
                step_list = case[1]
                kw = KeyWord(self.driver)
                for step in step_list:
                    key = step[2]  # 关键字
                    args = step[3:]  # 关键字参数
                    kw.get_kw_method(key)(*args)  # 调用关键字
                logger.info(f"----------------{case[0]}测开结束----------------")
                print(f"----------------{case[0]}测开结束----------------")

        yield Test
