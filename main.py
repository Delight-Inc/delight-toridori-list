import taberogu_search
import sys
import const
import spreadsheet

AREA = 1
GENRE = 2

def define_genre(genre: str) -> str:
    if genre == "all":
        return const.ALL
    elif genre == "bar":
        return const.BAR
    elif genre == "ramen":
        return const.RAMEN
    elif genre == "cafe":
        return const.CAFE
    elif genre == "restaurant":
        return const.RESTAURANT
    elif genre == "inn":
        return const.INN
    elif genre == "other":
        return const.OTHER
    else:
        return ""

def main():
    area = sys.argv[AREA]
    genre = sys.argv[GENRE]
    
    taberogu = taberogu_search.Taberogu(area, define_genre(genre=genre))
    taberogu.specify_search_info()
    print(taberogu.page_length())

    taberogu_list = []
    for i in range(1, 50):
        taberogu_list.append(taberogu.get_shop_name_list(current_page=i))

    result = []
    for i in range(len(taberogu_list)):
        for info in taberogu.get_shop_info(shop_link_list=taberogu_list[i]):
            result.append(info)

    for info in result:
        print(info)

    s = spreadsheet.Spreadsheet(tabegoru_list=result)
    s.write_spreadsheet()

if __name__ == "__main__":
    main()
