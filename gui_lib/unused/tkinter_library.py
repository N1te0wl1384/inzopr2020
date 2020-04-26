from tkinter import *
import gui_lib.unused.library as bib
from tkinter import messagebox
import gui_lib.db_operations as db
from tkinter import filedialog
import shutil
from PIL import ImageTk, Image



root = Tk()
root.title("biblioteka")

b = bib.Biblioteka(3)

def add_book(val):
    tit = title.get()
    aut = author.get()
    ed = edition.get()
    pic = pic_path.get()
    res_path = 'resources/'+str(tit)+"_"+str(aut)+"."+pic[-3:]
    shutil.copyfile(pic, res_path)
    b.dodaj_egz_ksiazki(tit, aut, ed, res_path)
    title.delete(0, END)
    author.delete(0, END)
    edition.delete(0, END)
    pic_path.delete(0, END)
    messagebox.showinfo(title="Info", message="Dodano egzemplarz")

def dodaj():
    global author
    global title
    global edition
    global pic_path

    adding_window = Tk()
    adding_window.geometry("350x150")

    title = Entry(adding_window, width=30)
    title.grid(row=0, column=1)
    title_label = Label(adding_window, text="Tytuł")
    title_label.grid(row=0, column=0, padx=20)
    author = Entry(adding_window, width=30)
    author.grid(row=1, column=1)
    author_label = Label(adding_window, text="Autor")
    author_label.grid(row=1, column=0, padx=20)
    edition = Entry(adding_window, width=30)
    edition.grid(row=2, column=1)
    edition_label = Label(adding_window, text="Rok Wydania")
    edition_label.grid(row=2, column=0, padx=20)
    pic_path_button = Button(adding_window, text="Zdjecie", command=get_pic_path)
    pic_path_button.grid(row=3, column=1, padx=20)
    pic_path = Entry(adding_window, width=30)
    pic_path.grid(row=3, column=0)

    add = Button(adding_window, text="Dodaj", command=lambda: add_book(True), padx=30)
    add.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky=W+E+S+N)


def get_pic_path():
    path = filedialog.askopenfilename(title="Select a file",
                                               filetypes=(("png", ".png"), ("jpg", ".jpg"), ("ico", ".ico")))
    pic_path.insert(0, path)


def show():
    show_window = Tk()
    show_window.geometry("350x150")
    books = db.get_speciments()
    books_text = ""
    for book in books:
        books_text += "\tTytul: "+book[0]+", Autor: "+book[1]+", Dostepne Egzemplarze: "+str(book[2])+"\n"
    books_list = Label(show_window, text=books_text)
    books_list.pack()


def show_my_books():
    show_window = Tk()
    show_window.geometry("350x150")
    books = db.get_user_books(logged_user[4])
    books_text = ""
    for book in books:
        books_text += "\tTytul: "+book[0]+", Autor: "+book[1]+"\n"
    books_list = Label(show_window, text=books_text)
    books_list.pack()

def after_login():
    global after_login_window

    root.destroy()
    after_login_window = Tk()
    add_button = Button(after_login_window, text = "Dodaj Ksiazke", command=dodaj, padx=91, pady=20)
    add_button.grid(row=0, column=0)
    borrow_button = Button(after_login_window, text="Wypozycz Ksiazke", command=browser_main_window, padx=80, pady=20)
    borrow_button.grid(row=1, column=0)
    show_button = Button(after_login_window, text="Moje Ksiazki", command=show, padx=93, pady=20)
    show_button.grid(row=2, column=0)
    logout_button = Button(after_login_window, text="Wyloguj sie", command=logout, padx=93, pady=20)
    logout_button.grid(row=3, column=0)
    current_user = Label(after_login_window, text="Zalogowany jako "+logged_user[1]+" " +logged_user[2],
                         bd=1, relief=SUNKEN)
    current_user.grid(row=4, column=0)

def logout():
    after_login_window.destroy()
    rebuild_root()

def log():
    global main_login
    global main_password
    global logged_user

    main_log = main_login.get()
    main_passwd = main_password.get()
    logged_user = db.fetch_user(main_log, main_passwd)

    if logged_user is None :
        messagebox.showerror(title="Error", message="Użytkownik nie jest zarejestrowany" )
    else:
        messagebox.showinfo(title="Zalogowano", message="Witaj " + logged_user[1] + " " + logged_user[2] + "!")
        after_login()

def register():
    global first_name
    global last_name
    global address
    global city
    global login
    global password
    global register_window

    register_window = Tk()
    register_window.geometry("300x300")

    first_name = Entry(register_window, width=30)
    first_name.grid(row=0, column=1)
    first_name_label = Label(register_window, text="Imie")
    first_name_label.grid(row=0, column=0, padx=20)
    last_name = Entry(register_window, width=30)
    last_name.grid(row=1, column=1)
    last_name_label = Label(register_window, text="Nazwisko")
    last_name_label.grid(row=1, column=0, padx=20)
    address = Entry(register_window, width=30)
    address.grid(row=2, column=1)
    address_label = Label(register_window, text="Adres")
    address_label.grid(row=2, column=0, padx=20)
    city = Entry(register_window, width=30)
    city.grid(row=3, column=1)
    city_label = Label(register_window, text="Miasto")
    city_label.grid(row=3, column=0, padx=20)
    login = Entry(register_window, width=30)
    login.grid(row=4, column=1)
    login_label = Label(register_window, text="Login")
    login_label.grid(row=4, column=0, padx=20)
    password = Entry(register_window, show="*", width=30)
    password.grid(row=5, column=1)
    password_label = Label(register_window, text="Haslo")
    password_label.grid(row=5, column=0, padx=20)
    register_button = Button(register_window, text="Zarejestruj się", command=add_user, padx=30)
    register_button.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky=W + E + S + N)

def add_user():

    fn = first_name.get()
    ln = last_name.get()
    ad = address.get()
    ct = city.get()
    lg = login.get()
    pwd = password.get()
    check = db.check_login(lg)

    if check is False:
        db.register_user(fn, ln, ad, ct, lg, pwd)
        messagebox.showinfo(title="Register", message="Użytkownik zarejestrowany!")
        register_window.destroy()
    elif check:
        messagebox.showerror(title="Error", message="Login już zajęty!")

def browser_main_window():
    global image_list
    global book_browser
    global book_list
    global book_display
    global status

    after_login_window.destroy()

    book_browser = Tk()
    book_browser.title("books")

    book_list = db.get_books()
    image_list = []
    for book in book_list:
        image_list.append(book[3])

    status = Label(book_browser, text="Image 1 out of " + str(len(image_list)), bd=1, relief=SUNKEN, anchor=E)
    test = Frame(book_browser)
    test.grid(column=0, row=0)
    img = ImageTk.PhotoImage(Image.open(image_list[0]))
    book_display = Label(book_browser ,image=img)
    book_display.grid(row=0, column=0, columnspan=3)

    button_back = Button(book_browser, text="<<", command= lambda: back(2, len(image_list)))
    button_forward = Button(book_browser, text=">>", command = lambda: forward(2, len(image_list)))
    button_quit = Button(book_browser, text="Wypozycz", command=lambda: wyp(book_list[0]))
    f = Frame(book_browser, pady=10, bd=10)
    book_title = Label(f, text="Autor: " +book[1])
    book_title.grid(row=0, column=0, sticky=W)
    book_title.config(font=("Times New Roman", 14))
    book_author = Label(f, text="Tytul: " +book[2])
    book_author.grid(row=1, column=0, sticky=W)
    book_author.config(font=("Times New Roman", 14))
    f.grid(row=1, column=0, sticky=W)
    button_back.grid(row=2, column=0)
    button_quit.grid(row=2, column=1)
    button_forward.grid(row=2, column=2, pady=10)
    status.grid(row=3, column=0, columnspan=3, sticky=W+E)
    book_browser.protocol("WM_DELETE_WINDOW", on_browser_close())

def on_browser_close():
    book_browser.destroy()
    after_login()

def wyp(book):
    db.lend_book(logged_user)
    messagebox.showinfo(title="Info", message="Wypozyczono książkę")

def forward(img_no, list_size):
    global book_display
    global button_forward
    global button_back
    global status

    book_display.grid_forget()
    status.grid_forget()
    book_display = Label(image=image_list[img_no - 1])
    button_forward = Button(book_browser, text=">>", command=lambda: forward(img_no + 1, list_size))
    button_back= Button(book_browser, text="<<", command=lambda: back(img_no - 1, list_size))
    button_quit = Button(book_browser, text="Wypozycz", command=lambda: wyp(book_list[img_no - 1]))

    book_title = Label(book_browser, text="Autor: " + book_list[img_no-1][1])
    book_title.grid(row=0, column=0, sticky=W)
    book_title.config(font=("Times New Roman", 14))
    book_author = Label(book_browser, text="Tytul: " + book_list[img_no-1][2])
    book_author.grid(row=1, column=0, sticky=W)
    book_author.config(font=("Times New Roman", 14))

    book_display.grid(row=0, column=0, columnspan=3)
    status = Label(book_browser, text="Image " + str(img_no) + " out of " + str(list_size), bd=1, relief=SUNKEN, anchor=E)

    if img_no == list_size:
        button_forward = Button(book_browser, text=">>", state=DISABLED)

    button_forward.grid(row=2, column=2)
    button_back.grid(row=2, column=0)
    button_quit(row=2, column=1)
    status.grid(row=3, column=0, columnspan=3, sticky=W+E)

def back(img_no, list_size):
    global book_display
    global button_forward
    global button_back
    global status

    book_display.grid_forget()
    status.grid_forget()
    book_display = Label(image=image_list[img_no - 1])
    button_forward = Button(book_browser, text=">>", command=lambda: forward(img_no + 1, list_size))
    button_back = Button(book_browser, text="<<", command=lambda: back(img_no - 1, list_size))
    button_quit = Button(book_browser, text="Wypozycz", command=lambda: wyp(book_list[img_no-1]))
    f = Frame(book_browser, pady=10, bd=10)
    book_title = Label(f, text="Autor: " + book_list[img_no-1][1])
    book_title.grid(row=0, column=0, sticky=W)
    book_title.config(font=("Times New Roman", 14))
    book_author = Label(f, text="Tytul: " + book_list[img_no-1][2])
    book_author.grid(row=1, column=0, sticky=W)
    book_author.config(font=("Times New Roman", 14))
    f.grid(row=1, column=0)

    book_display.grid(row=0, column=0, columnspan=3)
    status = Label(book_browser, text="Image " + str(img_no) + " out of " + str(list_size), bd=1, relief=SUNKEN, anchor=E)

    if img_no == 1 :
        button_back = Button(book_browser, text="<<", state=DISABLED)

    button_forward.grid(row=2, column=2)
    button_back.grid(row=2, column=0)
    button_quit(row=2, column=1)
    status.grid(row=3, column=0, columnspan=3, sticky=W+E)


def rebuild_root():
    root = Tk()
    root.title("biblioteka")
    main_login = Entry(root, width=30)
    main_login.grid(row=0, column=1)
    main_login_label = Label(root, text="Login")
    main_login_label.grid(row=0, column=0, padx=20)
    main_password = Entry(root, show="*", width=30)
    main_password.grid(row=1, column=1)
    main_password_label = Label(root, text="Haslo")
    main_password_label.grid(row=1, column=0, padx=20)
    login_button = Button(root, text="Zaloguj", command=log, padx=30)
    login_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky=W + E + S + N)
    status = Button(root, text="Nie masz konta? Załóż je tutaj", bd=0, relief=SUNKEN, command=register)
    status.grid(row=4, column=0)

main_login = Entry(root, width=30)
main_login.grid(row=0, column=1)
main_login_label = Label(root, text="Login")
main_login_label.grid(row=0, column=0, padx=20)
main_password = Entry(root, show="*", width=30)
main_password.grid(row=1, column=1)
main_password_label = Label(root, text="Haslo")
main_password_label.grid(row=1, column=0, padx=20)
login_button = Button(root, text="Zaloguj", command=log, padx=30)
login_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky=W + E + S + N)
status = Button(root, text="Nie masz konta? Załóż je tutaj", bd=0, relief=SUNKEN, command=register)
status.grid(row=4, column=0)
root.mainloop()