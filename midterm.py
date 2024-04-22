import os

from pack.modu import (
    add_books,
    check_table,
    create_db,
    load_data,
    login,
    menu_builder,
    search_books_data,
    show_books,
)

db_path = "./library.db"
users_data_path = "./users.csv"
books_data_path = "./books.json"
if __name__ == "__main__":
    # Database check
    db_exists = os.path.isfile(db_path)
    login_status = False
    if not db_exists:
        create_db(db_path)
        load_data(db_path, users_data_path, books_data_path)
    # Tables check
    # In this area try except include in the modu function
    tables_exists = check_table(db_path)
    if not tables_exists:
        create_db(db_path)
        load_data(db_path, users_data_path, books_data_path)
    # login
    while not login_status:
        account = input("請輸入帳號：")
        password = input("請輸入密碼：")
        login_status = login(db_path, account, password)

    # CURD
    # In this area try except include in choice
    active = True
    while active:
        menu_builder()
        choice = input("選擇要執行的功能(Enter離開)：")
        if choice == "":
            active = False
            continue
        elif choice == "1":
            try:
                title = input("請輸入要新增的標題：")
                author = input("請輸入要新增的作者：")
                publisher = input("請輸入要新增的出版社：")
                year = input("請輸入要新增的年份：")
                datas = (title, author, publisher, year)
                has_null_data = False
                for data in datas:
                    if data == "":
                        has_null_data = True

                if has_null_data:
                    print("=>給定的條件不足，無法進行修改作業")
                else:
                    add_books(db_path, datas)
            except ValueError:
                print("年份請輸入整數")
            except Exception as e:
                print('資料新增作業發生錯誤')
                print(f'錯誤代碼為：{e.errno}')
                print(f'錯誤訊息為：{e.strerror}')
        elif choice == "2":
            pass
        elif choice == "3":
            try:
                show_books(db_path)
                edit_index = input("請問要修改哪一本書的標題？：")

            except Exception as e:
                print('資料表顯示作業發生錯誤')
                print(f'錯誤代碼為：{e.errno}')
                print(f'錯誤訊息為：{e.strerror}')
        elif choice == "4":
            try:
                select_index = input("請輸入想查詢的關鍵字：")
                search_books_data(db_path, select_index)
            except Exception as e:
                print('特定資料表顯示作業發生錯誤')
                print(f'錯誤代碼為：{e.errno}')
                print(f'錯誤訊息為：{e.strerror}')
        elif choice == "5":
            try:
                show_books(db_path)
            except Exception as e:
                print('資料表顯示作業發生錯誤')
                print(f'錯誤代碼為：{e.errno}')
                print(f'錯誤訊息為：{e.strerror}')
        else:
            print("=>無效的選擇")
