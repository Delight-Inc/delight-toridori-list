from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import taberogu_list

class Taberogu:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get('https://tabelog.com/tokyo')
        assert '食べログ' in self.driver.title

    def page_length(self) -> int:
        return len(self.driver.find_elements(By.CLASS_NAME, "c-pagination__item"))

    def search(self, page: int) -> list[taberogu_list.TaberoguList]:
        if page != 1:
            self.driver.get(f'https://tabelog.com/tokyo/rstLst/{page}')

        shop_list = self.driver.find_elements(By.CLASS_NAME, "list-rst__rst-name-target")

        shop_link_list = []
        for shop in shop_list:
            shop_link_list.append(shop.get_attribute('href'))

        instagram_link_list = []
        for link in shop_link_list:
            self.driver.get(link)
            instagram_link = self.driver.find_elements(By.CLASS_NAME, "rstinfo-sns-link")
            if len(instagram_link) > 0 and 'instagram' in instagram_link[0].get_attribute('href'):
                try:
                    shop_name = self.driver.find_element(By.CLASS_NAME, "rstinfo-table__name-wrap").text
                    tel_number = self.driver.find_element(By.CLASS_NAME, "rstinfo-table__tel-num").text
                    address = self.driver.find_element(By.CLASS_NAME, "rstinfo-table__address").text
                    genre = self.driver.find_element(By.CLASS_NAME, "rdheader-subinfo__item-text").text
                    business_hours = self.driver.find_element(By.CLASS_NAME, "rstinfo-table__subject-text").text
                    opened_date = self.driver.find_element(By.CLASS_NAME, "rstinfo-opened-date").text

                    instagram_link_list.append(
                        taberogu_list.TaberoguList(
                            shop_name,
                            tel_number,
                            address,
                            instagram_link[0].get_attribute('href'),
                            genre,
                            business_hours,
                            opened_date
                        )
                    )
                except:
                    pass

        return instagram_link_list
