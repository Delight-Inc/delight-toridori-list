import gspread
import os
import taberogu_list

class Spreadsheet:
    def __init__(self, tabegoru_list: list[taberogu_list.TaberoguList]) -> None:
        self.tabegoru_list = tabegoru_list

    def write_spreadsheet(self) -> None:
        dir_path = os.path.dirname(__file__)
        gc = gspread.oauth(
            credentials_filename=os.path.join(dir_path, 'client_secret.json'),
            authorized_user_filename=os.path.join(dir_path, 'authorized_user.json'),
        )
        wb = gc.create('Toridori list')
        print(wb.id)

        wb = gc.open_by_key(wb.id)
        ws = wb.get_worksheet(0)

        data = [['店名', '電話番号', '住所', 'Instagram', 'ジャンル', '営業時間', '開店日']]
        for taberogu in self.tabegoru_list:
            data.append(
                [
                    taberogu.shop_name,
                    taberogu.tel_number,
                    taberogu.address,
                    taberogu.instagram_link,
                    taberogu.genre,
                    taberogu.business_hours,
                    taberogu.opened_date
                ]
            )

        ws.append_rows(data)
