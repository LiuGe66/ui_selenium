# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: conftest.py
# @Time : 2022/11/24 16:15
import json
import logging
from pathlib import Path
import pytest
from selenium import webdriver
from core import pom

logger = logging.getLogger(__name__)
huace = 'http://shop-xo.hctestedu.com/'
mashang = 'http://101.34.221.219:8010/'

@pytest.fixture(scope="class")
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    yield d
    d.quit()


def set_cookies(driver):

    cookies = []
    path = Path('temp/cookies/cookies.json')
    if path.exists():
        cookies = json.loads(path.read_text())

    logger.info(f"加载cookies{cookies}")
    for cookie in cookies:
        driver.add_cookie(cookie)
        logger.info(f"设置cookie:{cookie}")

    driver.get(huace)


def is_login(driver):
    return "退出" in driver.page_source


@pytest.fixture(scope='session')
def user_driver():
    """
    返回已登录状态的浏览器
    :return:
    """
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome()
    # driver.maximize_window()
    driver.get(huace)
    set_cookies(driver)  # 加载登录状态
    # driver.refresh()

    if not is_login(driver):
        page = pom.HomePage(driver)
        page = page.to_login()  # 跳转到登录页面
        page.login('liuge002', 'liuge666')
        msg = page.get_msg()
        assert '登录成功' == msg
        # 保存cookies到临时文件
        cookies = driver.get_cookies()
        with open("temp/cookies/cookies.json", "w") as f:
            f.write(json.dumps(cookies))

    yield driver
    driver.quit()


@pytest.fixture()
def clear_favor(user_driver):
    user_driver.get('http://shop-xo.hctestedu.com/index.php?s=/index/usergoodsfavor/index.html')
    page = pom.UserGoodsFavor(user_driver)
    if page.ele_btn_check_all.is_enabled():
        page.delete_all()
        msg = page.get_msg()
        assert msg == "删除成功"
    else:
        pass
