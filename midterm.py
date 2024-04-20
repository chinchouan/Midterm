import os

from pack.modu import check_table, create_db, load_data

db_path = "./library.db"
users_data_path = "./users.csv"
books_data_path = "./books.json"
if __name__ == "__main__":
    # Database check
    db_exists = os.path.isfile(db_path)
    tables_exists = check_table(db_path)
    if not db_exists or tables_exists:
        print(create_db(db_path))
        print(load_data(db_path, users_data_path, books_data_path))
    # CURD
    try:
        pass
    except Exception as e:
        print('XXX作業發生錯誤')
        print(f'錯誤代碼為：{e.errno}')
        print(f'錯誤訊息為：{e.strerror}')
