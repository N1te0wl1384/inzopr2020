import sqlite3


def create_db():
    conn = sqlite3.connect('resources/library.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE readers (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        first_name text,
        last_name text,
        address text,
        city text,
        login text,
        password text,
        FOREIGN KEY(ID) REFERENCES lendings(reader_id)
        )""")

    c.execute("""CREATE TABLE specimens (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        edition text,
        is_lend text,
        FOREIGN KEY(book_id) REFERENCES books(ID)
        )""")

    c.execute("""CREATE TABLE books (
        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        author text,
        title text,
        resource_path text
        )""")

    c.execute("""CREATE TABLE lendings (
           ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
           specimen_id INTEGER,
           reader_id INTEGER,
           FOREIGN KEY(specimen_id) REFERENCES specimens(ID),
           FOREIGN KEY(reader_id) REFERENCES readers(ID)
           )""")

    conn.commit()
    conn.close()


def add_book(author, title, pic):
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()

    c.execute("INSERT INTO books(author, title, resource_path) VALUES (:author, :title, :resource_path)",
              {
                  'author': author,
                  'title': title,
                  'resource_path': pic
              })
    conn.commit()
    conn.close()


def add_specimens(book_id, edition, is_lend):
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    c.execute("INSERT INTO specimens(book_id, edition, is_lend) VALUES (:book_id, :edition, :is_lend)",
              {
                  'book_id': book_id,
                  'edition': edition,
                  'is_lend': is_lend
              })
    conn.commit()
    conn.close()


def get_books():
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    book_list = c.fetchall()

    conn.commit()
    conn.close()

    return book_list


def get_book_key(author, title):
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    c.execute("SELECT ID FROM books WHERE title=:title",
              {
                  "title": title
              })
    key = c.fetchone()
    conn.commit()
    conn.close()
    return int(key[0])


def get_speciments():
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    c.execute("""SELECT author, title, count(book_id) FROM specimens JOIN books ON specimens.book_id = books.ID "
              WHERE is_lend = false GROUP BY book_id""")
    speciments_list = c.fetchall()
    conn.commit()
    conn.close()
    return speciments_list


def fetch_user(login, password):
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    c.execute("SELECT ID, first_name, last_name FROM readers WHERE login=:login AND password=:password",
              {
                  "login": login,
                  "password": password
              })
    user = c.fetchone()
    conn.commit()
    conn.close()
    return user


def register_user(first_name, last_name, address, city, login, password):
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    c.execute("""INSERT INTO readers(first_name, last_name, address, city, login, password) 
                VALUES (:first_name, :last_name, :address, :city, :login, :password)""",
              {
                  'first_name': first_name,
                  'last_name': last_name,
                  'address': address,
                  'city': city,
                  'login': login,
                  'password': password
              })
    conn.commit()
    conn.close()


def check_login(login):
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    c.execute("SELECT ID, first_name, last_name FROM readers WHERE login=:login",
              {
                  "login": login
              })
    user = c.fetchone()
    if user is None:
        return False
    else:
        return True
    conn.commit()
    conn.close()

def lend_book(book, user):
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    c.execute("""SELECT specimens.ID FROM specimens JOIN books ON books.ID = specimens.book_id
                WHERE author=:author AND title=:title AND is_lend=:is_lend""",
              {
                  "author": book[1],
                  "title": book[2],
                  "is_lend": "false"
              })
    book_to_lend = c.fetchone()
    c.execute("""INSERT INTO lendings(specimen_id, reader_id) VALUES (:specimen_id, :user_id)""",
              {
                  "specimen_id": book_to_lend[0],
                  "user_id": user[0]
              })
    c.execute(""" UPDATE  specimens SET is_lend=true
                WHERE ID=:id """,
              {
                  "id": book_to_lend[0]
              })
    conn.commit()
    conn.close()

def return_book(book, user):
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    c.execute(""" SELECT * FROM lendings WHERE reader_id=:rd_id AND specimen_id=:sp_id""",
              {
               "rd_id": user[0],
               "sp_id": book
              })
    returned_book = c.fetchone()
    c.execute(""" UPDATE specimens SET is_lend='false'
                   WHERE ID=:id """,
              {
                  "id": returned_book[1]
              })
    c.execute(""" DELETE FROM lendings WHERE reader_id=:rd_id AND specimen_id=:sp_id""",
              {
                  "rd_id": user[0],
                  "sp_id": book
              }
              )
    conn.commit()
    conn.close()


def check_lendings(id):
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    c.execute("""
                    SELECT  books.ID, books.author, books.title, specimens.ID FROM lendings
                    JOIN specimens ON lendings.specimen_id = specimens.ID
                    JOIN books ON specimens.book_id = books.ID 
                    WHERE lendings.reader_id=:id""",
              {
                  "id": id
              })
    borrowed_books = c.fetchall()
    conn.commit()
    conn.close()
    return borrowed_books


def get_free_specs():
    conn = sqlite3.connect('resources/library.db')
    c = conn.cursor()
    # wolne egzemplarze
    c.execute("""SELECT books.ID ,author, title, resource_path FROM specimens
                    JOIN books ON specimens.book_id=books.ID
                    WHERE is_lend = "false" 
                    """)
    free_spec = c.fetchall()
    free_spec = list(dict.fromkeys(free_spec))
    return free_spec
#create_db()