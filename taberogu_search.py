from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import taberogu_list
import const

class Taberogu:
    def __init__(self, area: str, genre: str) -> None:
        self.area = area
        self.genre = genre
        self.driver = webdriver.Chrome()
        self.driver.get('https://tabelog.com/tokyo')
        assert '食べログ' in self.driver.title

    def page_length(self) -> int:
        print(self.driver.current_url)
        return len(self.driver.find_elements(By.CLASS_NAME, "c-pagination__item"))
    
    def define_area(area: str) -> str:
        if area == "tokyo":
            return const.TOKYO
        elif area == "osaka":
            return const.OSAKA
        elif area == "nagoya":
            return const.NAGOYA
        elif area == "sapporo":
            return const.SAPPORO
        elif area == "kanagawa":
            return const.KANAGAWA
        elif area == "hyogo":
            return const.HYOGO
        else:
            return ""
    
    def specify_search_info(self) -> None:
        print(self.area)
        print(self.genre)
        if self.area == "tokyo" and self.genre == const.ALL:
            return

        self.driver.find_element(By.CLASS_NAME, "sc-fLcnxK").click()

        self.driver.find_element(By.ID, "detailedSearchModalPrefecture").click()
        prefecture_list = self.driver.find_element(By.ID, "detailedSearchModalPrefecture")
        select = Select(prefecture_list)
        select.select_by_visible_text(Taberogu.define_area(self.area))

        self.driver.find_element(By.ID, "detailedSearchModalCategory0").click()
        genre_list = self.driver.find_element(By.ID, "detailedSearchModalCategory0")
        select = Select(genre_list)
        select.select_by_visible_text(self.genre)

        self.driver.find_element(By.CLASS_NAME, "sc-kDvujY").click()

    def get_page_url(self, current_page: int) -> str:
        page_url = self.driver.find_elements(By.CLASS_NAME, "c-pagination__num")
        for url in page_url:
            if url.text == str(current_page + 1):
                return url.get_attribute('href')
        return ""
    
    def get_shop_name_list(self, page_url: str) -> list[str]:
        if page_url != "1":
            self.driver.get(page_url) 

        shop_list = self.driver.find_elements(By.CLASS_NAME, "list-rst__rst-name-target")
        shop_link_list = []
        for shop in shop_list:
            shop_link_list.append(shop.get_attribute('href'))
        
        return shop_link_list

    def get_shop_info(self, shop_link_list: list[str]) -> list[taberogu_list.TaberoguList]:
        instagram_link_list = []
        for link in shop_link_list:
            self.driver.get(link)
            instagram_link = self.driver.find_elements(By.CLASS_NAME, "rstinfo-sns-link")
            if len(instagram_link) > 0 and 'instagram' in instagram_link[0].get_attribute('href'):
                try:
                    shop_name = self.driver.find_element(By.CLASS_NAME, "rstinfo-table__name-wrap").text
                    tel_number = self.driver.find_element(By.CLASS_NAME, "rstinfo-table__tel-num").text
                    address = self.driver.find_element(By.CLASS_NAME, "rstinfo-table__address").text
                    genre = self.driver.find_elements(By.CLASS_NAME, "rdheader-subinfo__item")[2].text.split('ジャンル：')
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
