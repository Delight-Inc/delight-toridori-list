import gspread
import os
import taberogu_list
import sys

class Spreadsheet:
    def __init__(self, tabegoru_list: list[taberogu_list.TaberoguList]) -> None:
        self.tabegoru_list = tabegoru_list

    def write_spreadsheet(self) -> None:
        dir_path = os.path.dirname(__file__)
        gc = gspread.oauth(
            credentials_filename=os.path.join(dir_path, 'client_secret.json'),
            authorized_user_filename=os.path.join(dir_path, 'authorized_user.json'),
        )
        area = sys.argv[1]
        genre = sys.argv[2]
        title = 'Toridori list' + ' ' + area + ' ' + genre
        wb = gc.create(title=title)
        print(wb.id)

        wb = gc.open_by_key(wb.id)
        ws = wb.get_worksheet(0)

        data = [['電話番号', '店名', 'Instagram', '住所', '営業時間', 'ジャンル', '開店日']]
        for taberogu in self.tabegoru_list:
            print(taberogu)
            data.append(
                [
                    taberogu.tel_number,
                    taberogu.shop_name,
                    taberogu.instagram_link,
                    taberogu.address,
                    taberogu.business_hours,
                    taberogu.genre,
                    taberogu.opened_date
                ]
            )
        print(data)

        ws.append_rows(data)
