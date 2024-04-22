import os

from pack.modu import (
    check_table,
    create_db,
    load_data,
    login,
    menu_builder,
    select_book,
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
    active = True
    while active:
        menu_builder()
        choice = input("選擇要執行的功能(Enter離開)：")
        if choice == "":
            active = False
            continue
        elif choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            try:
                select_data = input("請輸入想查詢的關鍵字：")
                select_book(select_data)
            except Exception as e:
                print('資料表顯示作業發生錯誤')
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
