from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import taberogu_list
import const

class Taberogu:
    def __init__(self, area: str, genre: str) -> None:
        options = Options()
        options.add_argument('--headless')
        self.area = area
        self.genre = genre
        self.driver = webdriver.Chrome(options=options)
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
        elif area == "kyoto":
            return const.KYOTO
        elif area == "sendai":
            return const.SENDAI
        elif area == "fukuoka":
            return const.FUKUOKA
        elif area == "hiroshima":
            return const.HIROSHIMA
        elif area == "saitama":
            return const.SAITAMA
        elif area == "chiba":
            return const.CHIBA
        elif area == "shizuoka":
            return const.SHIZUOKA
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
        self.driver.implicitly_wait(10)
        select.select_by_visible_text(Taberogu.define_area(self.area))

        self.driver.find_element(By.ID, "detailedSearchModalCategory0").click()
        genre_list = self.driver.find_element(By.ID, "detailedSearchModalCategory0")
        select = Select(genre_list)
        self.driver.implicitly_wait(10)
        select.select_by_visible_text(self.genre)

        self.driver.find_element(By.CLASS_NAME, "sc-kDvujY").click()

    def get_page_url(self) -> list[str]:
        res = requests.get(self.driver.current_url)
        soup = BeautifulSoup(res.text, "html.parser")
        page_url = soup.find_all("a", class_="c-pagination__num")
        base_url, params = page_url[0].get("href").split("?", 1)
        base_url_parts = base_url.rstrip("/").split("/")[:-1]
        base_url = "/".join(base_url_parts) + "/"
        url_list = []
        for page_number in range(2, 51):
            page_url = f"{base_url}{page_number}/?{params}"
            url_list.append(page_url)
            print(f"Fetching page {page_number}: {page_url}")
        return url_list
    
    def get_shop_name_list(self, current_page_url: str) -> list[str]:
        res = requests.get(current_page_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        shop_list = soup.find_all("a", class_="list-rst__rst-name-target")

        shop_link_list = []
        for shop in shop_list:
            try:
                shop_link_list.append(shop.get("href"))
            except TimeoutException:
                print("get_shop_name_list TimeoutException")
                continue
            except:
                print("get_shop_info except")
                pass
        
        return shop_link_list

    def get_shop_info(self, shop_link_list: list[str]) -> list[taberogu_list.TaberoguList]:
        instagram_link_list = []
        i = 0
        for link in shop_link_list:
            i += 1
            print(i)
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(10)
            res = requests.get(link)
            soup = BeautifulSoup(res.text, 'html.parser')
            try:
                instagram_link = soup.find('a', href=lambda value: value and value.startswith("https://www.instagram.com/")).get_text()
                tel_number = soup.find_all('strong', class_='rstinfo-table__tel-num')[1].text
                opened_date = soup.find('p', class_='rstinfo-opened-date').text
                address = soup.find('p', class_='rstinfo-table__address').text
                shop_name = soup.find('div', class_='rstinfo-table__name-wrap').text
                business_hours = soup.find('p', class_='rstinfo-table__subject-text').text

                instagram_link_list.append(
                    taberogu_list.TaberoguList(
                        shop_name.strip(),
                        tel_number.strip(),
                        address.strip(),
                        instagram_link.strip(),
                        "",
                        business_hours.strip(),
                        opened_date.strip(),
                    )
                )
            except TimeoutException:
                print("get_shop_info TimeoutException")
                continue
            except:
                print("get_shop_info except")
                pass

        return instagram_link_list
