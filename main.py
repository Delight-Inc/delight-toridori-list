import taberogu_search
import sys
import const

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
    # # taberogu_page_length = taberogu.page_length()
    # # range(1, taberogu_page_length)
    # taberogu_list = []
    # for i in range(1, 3):
    #     taberogu_list.append(taberogu.get_shop_name_list(i))
    
    # result = []
    # for i in range(len(taberogu_list)):
    #     result.append(taberogu.get_shop_info(taberogu_list[i]))
    # # s = spreadsheet.Spreadsheet(tabegoru_list=taberogu_list)
    # # s.write_spreadsheet()
    # for t in result:
    #     print('-------------------')
    #     print(t)
    #     print('-------------------')

if __name__ == "__main__":
    main()
