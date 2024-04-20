import json
import sqlite3


def create_db(db_path: str) -> bool:
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
        result = True
    except Exception as e:
        print("Error", e)
        result = False
    return result


def load_data(db_path, *data_path) -> bool:
    """_summary_

    Returns:
        bool: _description_
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Write users
        with open(data_path[0], 'r') as f:
            users = f.read()
            users_format = users.split('\n')
            print(users_format)
        for uf in users_format:
            print(uf)
            uf_split = uf.split(',')
            # # username and password not a user
            # if uf_split[0] == "username" and uf_split[1] == "password":
            #     continue
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
        result = True
    except FileNotFoundError:
        print('找不到檔案...')
        result = False
    except Exception as e:
        print('開檔發生錯誤...')
        print(f'錯誤代碼為：{e.errno}')
        print(f'錯誤訊息為：{e.strerror}')
        print(f'錯誤檔案為：{e.filename}')
        result = False
    return result


def check_table(db_path) -> bool:
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
    except Exception as e:
        print(e)
        return False
