import taberogu_search

def main():
    taberogu = taberogu_search.Taberogu()
    for shop_name in taberogu.search():
        print(shop_name)

if __name__ == "__main__":
    main()
