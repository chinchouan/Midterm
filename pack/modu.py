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
        # Create table users
        cmd = """Create table if not exists users(
            user_id integer primary key autoincrement,
            username text not null,
            password text not null
            );"""
        cursor.execute(cmd)
        # Create table books
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
        # Check talbe in database
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
        # Get user information
        cursor.execute("Select username, password from users")
        ac_table = cursor.fetchall()
        ac_exists = False
        pwd_correct = False
        # Check the login information is correct
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


def show_books(db_path: str) -> None:
    """Show the books information

    Args:
        db_path (str): Database path
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Get data
    cursor.execute("Select title,author,publisher,year from books")
    result = cursor.fetchall()
    print("|  title  |   author   |  publisher  |   year  |")
    # Show data
    for book in result:
        title, author, publisher, year = book
        print(f"|{title:6s}|{author:9s}|{publisher:8s}|{year:<8d}|")
    conn.commit()
    cursor.close()
    conn.close()


def search_books_data(db_path: str, index: str) -> None:
    """Show the search books information

    Args:
        db_path (str): _description_
        index (str): _description_
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Get specific information
    cmd = f"""select title,author,publisher,year from books
    where title like '{index}' or author like '{index}' """
    cursor.execute(cmd)
    result = cursor.fetchall()
    print("|  title  |   author   |  publisher  |   year  |")
    for book in result:
        title, author, publisher, year = book
        print(f"|{title:6s}|{author:9s}|{publisher:8s}|{year:<8d}|")
    conn.commit()
    cursor.close()
    conn.close()


def add_books(db_path: str, datas: tuple) -> None:
    """Add new books information to database

    Args:
        db_path (str): Database path
        datas (tuple): Data with books information
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Data split
    title: str
    author: str
    publisher: str
    year: str
    title, author, publisher, year = datas
    year: int = int(year)
    # Check the book exists or exists, if not exists append it
    cursor.execute(f"Select title from books where title like '{title}'")
    result = cursor.fetchall()
    if result != []:
        print("新增失敗：書籍資料已經存在")
    else:
        cmd = "Insert into books(title, author, publisher, year) values(?, ?, ?, ?)"
        cursor.execute(cmd, (title, author, publisher, year))
        print("異動 1 記錄")
        conn.commit()
        show_books(db_path)
    cursor.close()
    conn.close()


def edit_books(db_path: str, datas: tuple) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Data split
    index: str
    title: str
    author: str
    publisher: str
    year: str
    index, title, author, publisher, year = datas
    year: int = int(year)
    # Search data
    cmd = f"""select title,author,publisher,year from books
    where title like '{title}' """
    book_exists = cursor.execute(cmd)
    if book_exists is None:
        print("欲修改書籍資料不存在")
    else:
        cmd = """Update books set title = ?, author = ?, publisher = ?, year = ?
        where title like ?"""
        cursor.execute(cmd, (title, author, publisher, year, index))
        print("異動 1 記錄")
        conn.commit()
        # Show changed data
        show_books(db_path)
    cursor.close()
    conn.close()


def delete_books(db_path: str, title: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cmd = f"""select title,author,publisher,year from books
    where title like '{title}' """
    book_exists = cursor.execute(cmd)
    if book_exists is None:
        print("欲刪除書籍資料不存在")
    else:
        cursor.execute(f"Delete from books where title like '{title}'")
        print("異動 1 記錄")
        conn.commit()
        # Show changed data
        show_books(db_path)
    cursor.close()
    conn.close()
