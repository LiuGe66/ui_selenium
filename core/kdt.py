# -*- coding: utf-8 -*-
# Author:liu_ge
# @FileName: pom.py
# @Time : 2022/11/24 21:07
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)


class KeyWord:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, *args):
        # 封装过的元素定位方法，自动使用显示等待
        logger.info(f"正在定位元素{args}")
        el = self.wait.until(lambda _: self.driver.find_element(*args))
        logger.info("元素定位成功")
        return el

    def key_input(self, loc, content=None):
        ele = self.find_element(By.XPATH, loc)
        self.wait.until(lambda _: ele.is_enabled())
        try:
            ele.clear()
        except:
            print("清除元素文本失败")
        if content is not None:
            ele.send_keys(content)

    def key_js_code(self, loc, code):
        ele = self.find_element(By.XPATH, loc)
        self.driver.execute_script(code, ele)

    def key_click(self, loc):
        ele = self.find_element(By.XPATH, loc)
        self.wait.until(lambda _: ele.is_enabled())
        ele.click()

    def get_page(self, url):
        self.driver.get(url)

    def key_assert_text(self, loc, expect_text):
        ele_text = self.wait.until(
            lambda _: self.driver.find_element(By.XPATH, loc).text
        )
        ele_text = ele_text.strip()
        expect_text = expect_text.strip()
        logger.info(f'实际结果:{ele_text}')
        logger.info(f"期望结果:{expect_text}")
        assert ele_text == expect_text, logger.warning("断言失败,'{}'不等于'{}'".format(ele_text, expect_text))
