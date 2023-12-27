import taberogu_search
import spreadsheet

def main():
    taberogu = taberogu_search.Taberogu()
    # taberogu_page_length = taberogu.page_length()
    # range(1, taberogu_page_length)
    taberogu_list = []
    for i in range(1, 4):
        taberogu_list.append(taberogu.search(i))
    # s = spreadsheet.Spreadsheet(tabegoru_list=taberogu_list)
    # s.write_spreadsheet()
    for t in taberogu_list:
        print('-------------------')
        print(t)
        print('-------------------')

if __name__ == "__main__":
    main()
