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
        logger.warning(f"设置cookie:{cookie}")

    driver.get("http://101.34.221.219:8010")


def is_login(driver):
    return "退出" in driver.page_source


@pytest.fixture(scope='session')
def user_driver():
    """
    返回已登录状态的浏览器
    :return:
    """

    driver = webdriver.Chrome()
    # driver.maximize_window()
    driver.get("http://101.34.221.219:8010")
    set_cookies(driver)  # 加载登录状态
    # driver.refresh()
    logger.info('设置完成了。。。')

    a = is_login(driver)
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',a)
    if not is_login(driver):
        logger.info("如果能看到我，就说明没有获得有效的cookies")
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
    user_driver.get('http://101.34.221.219:8010/?s=usergoodsfavor/index.html')
    # user_driver.get('http://shop-xo.hctestedu.com/index.php?s=/index/usergoodsfavor/index.html')
    page = pom.UserGoodsFavor(user_driver)
    if page.ele_btn_check_all.is_enabled():
        page.delete_all()
        msg = page.get_msg()
        assert msg == "删除成功"
    else:
        pass
