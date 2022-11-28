import os
import pytest

if __name__ == '__main__':
    pytest.main()
    os.system('allure generate temp/allure -o report --clean')
    os.system('allure open report -p 8099')
