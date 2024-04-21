import json
import sqlite3


def create_db(db_path: str) -> None:
    """This function will create database(library.db)

    Args:
        db_path (str): Database path

    Returns:
        bool: Create success or failed
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cmd = """Create table if not exists users(
            user_id integer primary key autoincrement,
            username text not null,
            password text not null
            );"""
        cursor.execute(cmd)
        cmd = """Create table if not exists books(
            book_id integer primary key autoincrement,
            title text not null,
            author text not null,
            publisher text not null,
            year integer not null
            );"""
        cursor.execute(cmd)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print('創建資料庫作業發生錯誤')
        print(f'錯誤代碼為：{e.errno}')
        print(f'錯誤訊息為：{e.strerror}')


def load_data(db_path: str, *data_path: tuple) -> None:
    """Import data into database

    Args:
        db_path (str): Database path
        *data_path(list): All need to import data file path
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Write users
        with open(data_path[0], 'r') as f:
            users = f.read()
            users_format = users.split('\n')
        for uf in users_format:
            uf_split = uf.split(',')
            # username and password not a user
            if uf_split[0] == "username" and uf_split[1] == "password":
                continue
            cmd = "Insert into users (username, password) values(?,?)"
            cursor.execute(cmd, (uf_split[0], uf_split[1]))
        # Write books
        with open(data_path[1], 'r', encoding='utf-8') as f:
            books = json.load(f)
        for b in books:
            title = b["title"]
            author = b["author"]
            publisher = b["publisher"]
            year = b["year"]
            cmd = "Insert into books(title, author, publisher, year) values(?,?,?,?)"
            cursor.execute(cmd, (title, author, publisher, year))
        conn.commit()
        cursor.close()
        conn.close()
    except FileNotFoundError:
        print('找不到檔案...')
    except Exception as e:
        print('開檔發生錯誤...')
        print(f'錯誤代碼為：{e.errno}')
        print(f'錯誤訊息為：{e.strerror}')
        print(f'錯誤檔案為：{e.filename}')


def check_table(db_path: str) -> bool:
    """Check that the data table in the database exists

    Args:
        db_path (str): Database path

    Returns:
        bool: tables exists or unexists
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        tables = ("users", "books")
        for t in tables:
            cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name = ?", (t,))
            result = cursor.fetchone()
            assert result is not None, f"Table {t} is not exists, Database has not corret exists."
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except AssertionError as ae:
        print(ae)
        return False
    except Exception as e:
        print('檢查表格作業發生錯誤')
        print(f'錯誤代碼為：{e.errno}')
        print(f'錯誤訊息為：{e.strerror}')
        return False


def login(db_path: str, account: str, password: str) -> bool:
    """Login to the Data tables CRUD system

    Args:
        account (str): username
        password (str): password

    Returns:
        bool: Login success or failed
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("Select username, password from users")
        ac_table = cursor.fetchall()
        ac_exists = False
        pwd_correct = False
        for data in ac_table:
            ac, pwd = data
            if account == ac:
                ac_exists = True
                if password == pwd:
                    pwd_correct = True
        if ac_exists and pwd_correct:
            login_status = True
        else:
            login_status = False
            if not ac_exists and not pwd_correct:
                print("帳密錯誤")
            elif not ac_exists:
                print("帳號錯誤")
            elif not pwd_correct:
                print("密碼錯誤")

        conn.commit()
        cursor.close()
        conn.close()
        return login_status
    except Exception as e:
        print('登入作業發生錯誤')
        print(f'錯誤代碼為：{e.errno}')
        print(f'錯誤訊息為：{e.strerror}')
        return False


def menu_builder() -> None:
    """Print data tables CRUD menu"""
    print("-" * 19)
    print("", "資料表 CRUD", sep="    ")
    print("-" * 19)
    print("", "1. 增加記錄", sep="    ")
    print("", "2. 刪除記錄", sep="    ")
    print("", "3. 修改記錄", sep="    ")
    print("", "4. 查詢記錄", sep="    ")
    print("", "5. 資料清單", sep="    ")
    print("-" * 19)
