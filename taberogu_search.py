from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Taberogu:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get('https://tabelog.com/tokyo')
        assert '食べログ' in self.driver.title

    def search(self) -> list[str]:
        shop_list = self.driver.find_elements(By.CLASS_NAME, "list-rst__rst-name-target")

        shop_link_list = []
        for shop in shop_list:
            shop_link_list.append(shop.get_attribute('href'))

        return shop_link_list
    