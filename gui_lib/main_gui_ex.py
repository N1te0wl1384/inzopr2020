import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image

import gui_lib.db_operations as db


class LoginPage:

    def __init__(self):
        self.root = tk.Tk()
        self.main_login = tk.Entry(self.root, width=30)
        self.main_login.grid(row=0, column=1)
        main_login_label = tk.Label(self.root, text="Login")
        main_login_label.grid(row=0, column=0, padx=20)
        self.main_password = tk.Entry(self.root, show="*", width=30)
        self.main_password.grid(row=1, column=1)
        main_password_label = tk.Label(self.root, text="Haslo")
        main_password_label.grid(row=1, column=0, padx=20)
        login_button = tk.Button(self.root, text="Zaloguj", padx=30, command=self.log)
        login_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky=tk.W + tk.E + tk.S + tk.N)
        status = tk.Button(self.root, text="Nie masz konta? Załóż je tutaj", bd=0, relief=tk.SUNKEN,
                           command=self.register)
        status.grid(row=4, column=0)
        self.root.mainloop()

    def log(self):
        global logged_user
        main_log = self.main_login.get()
        main_passwd = self.main_password.get()
        logged_user = db.fetch_user(main_log, main_passwd)

        if logged_user is None:
            messagebox.showerror(title="Error", message="Użytkownik nie jest zarejestrowany")
        else:
            messagebox.showinfo(title="Zalogowano", message="Witaj " + logged_user[1] + " " + logged_user[2] + "!")
            self.root.destroy()
            AfterLogin()

    def register(self):
        self.root.destroy()
        Register()


class AfterLogin:

    def __init__(self):
        self.root = tk.Tk()

        add_button = tk.Button(self.root, text="Dodaj Ksiazke", command=self._add_book_window, padx=91, pady=20)
        add_button.grid(row=0, column=0)
        borrow_button = tk.Button(self.root, text="Wypozycz Ksiazke", command=self.browser_main_window, padx=80,
                                  pady=20)
        borrow_button.grid(row=1, column=0)
        show_button = tk.Button(self.root, text="Moje Ksiazki", command=self.return_books, padx=93, pady=20)
        show_button.grid(row=2, column=0)
        logout_button = tk.Button(self.root, text="Wyloguj sie", command=self.logout, padx=93, pady=20)
        logout_button.grid(row=3, column=0)
        current_user = tk.Label(self.root, text="Zalogowany jako " + logged_user[1] + " " + logged_user[2], bd=1,
                                relief=tk.SUNKEN)
        current_user.grid(row=4, column=0)
        self.root.mainloop()

    def _add_book_window(self):
        self.root.destroy()
        AddBook()

    def browser_main_window(self):
        self.root.destroy()
        BookBrowser()

    def return_books(self):
        self.my_window = tk.Tk()
        titles = []
        numbers = []
        authors = []
        borrowed_books = db.check_lendings(logged_user[0])
        for book in borrowed_books:
            titles.append(book[2])
            numbers.append(book[3])
            authors.append(book[1])
        for i, n in enumerate(titles):
            ReturnBook(self.my_window, n, numbers[i], authors[i]).pack(expand=True, fill="x")

    def logout(self):
        self.root.destroy()
        LoginPage()


def checkbook(author, title, edition, pic_path):
    book_list = db.get_books()
    current_book = None
    for book in book_list:
        if book[1] == author and book[2] == title:
            current_book = book
    if current_book is None:
        db.add_book(author, title, pic_path)
    key = db.get_book_key(author, title)
    db.add_specimens(key, edition, "false")


class AddBook:
    def __init__(self):
        self.adding_window = tk.Tk()
        self.adding_window.geometry("350x150")

        self.title = tk.Entry(self.adding_window, width=30)
        self.title.grid(row=0, column=1)
        title_label = tk.Label(self.adding_window, text="Tytuł")
        title_label.grid(row=0, column=0, padx=20)
        self.author = tk.Entry(self.adding_window, width=30)
        self.author.grid(row=1, column=1)
        author_label = tk.Label(self.adding_window, text="Autor")
        author_label.grid(row=1, column=0, padx=20)
        self.edition = tk.Entry(self.adding_window, width=30)
        self.edition.grid(row=2, column=1)
        edition_label = tk.Label(self.adding_window, text="Rok Wydania")
        edition_label.grid(row=2, column=0, padx=20)
        pic_path_button = tk.Button(self.adding_window, text="Zdjecie", command=self.get_pic_path)
        pic_path_button.grid(row=3, column=1, padx=20)
        self.pic_path = tk.Entry(self.adding_window, width=30)
        self.pic_path.grid(row=3, column=0)

        add = tk.Button(self.adding_window, text="Dodaj", command=self.add_book, padx=30)
        add.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky=tk.W + tk.E + tk.S + tk.N)

    def add_book(self):
        tit = self.title.get()
        aut = self.author.get()
        ed = self.edition.get()
        pic = self.pic_path.get()
        res_path = 'resources/' + str(tit) + "_" + str(aut) + "." + pic[-3:]
        checkbook(aut, tit, ed, res_path)
        shutil.copyfile(pic, res_path)
        self.title.delete(0, tk.END)
        self.author.delete(0, tk.END)
        self.edition.delete(0, tk.END)
        self.pic_path.delete(0, tk.END)
        messagebox.showinfo(title="Info", message="Dodano egzemplarz")
        self.adding_window.destroy()
        AfterLogin()

    def get_pic_path(self):
        path = filedialog.askopenfilename(title="Select a file",
                                          filetypes=(("png", ".png"), ("jpg", ".jpg"), ("ico", ".ico")))
        self.pic_path.insert(0, path)


class Register:
    def __init__(self):
        self.register_window = tk.Tk()
        self.register_window.geometry("300x300")

        self.first_name = tk.Entry(self.register_window, width=30)
        self.first_name.grid(row=0, column=1)
        first_name_label = tk.Label(self.register_window, text="Imie")
        first_name_label.grid(row=0, column=0, padx=20)
        self.last_name = tk.Entry(self.register_window, width=30)
        self.last_name.grid(row=1, column=1)
        last_name_label = tk.Label(self.register_window, text="Nazwisko")
        last_name_label.grid(row=1, column=0, padx=20)
        self.address = tk.Entry(self.register_window, width=30)
        self.address.grid(row=2, column=1)
        address_label = tk.Label(self.register_window, text="Adres")
        address_label.grid(row=2, column=0, padx=20)
        self.city = tk.Entry(self.register_window, width=30)
        self.city.grid(row=3, column=1)
        city_label = tk.Label(self.register_window, text="Miasto")
        city_label.grid(row=3, column=0, padx=20)
        self.login = tk.Entry(self.register_window, width=30)
        self.login.grid(row=4, column=1)
        login_label = tk.Label(self.register_window, text="Login")
        login_label.grid(row=4, column=0, padx=20)
        self.password = tk.Entry(self.register_window, show="*", width=30)
        self.password.grid(row=5, column=1)
        password_label = tk.Label(self.register_window, text="Haslo")
        password_label.grid(row=5, column=0, padx=20)
        register_button = tk.Button(self.register_window, text="Zarejestruj się", command=self.add_user, padx=30)
        register_button.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky=tk.W + tk.E + tk.S + tk.N)

    def add_user(self):
        fn = self.first_name.get()
        ln = self.last_name.get()
        ad = self.address.get()
        ct = self.city.get()
        lg = self.login.get()
        pwd = self.password.get()
        check = db.check_login(lg)

        if check is False:
            db.register_user(fn, ln, ad, ct, lg, pwd)
            messagebox.showinfo(title="Register", message="Użytkownik zarejestrowany!")
            self.register_window.destroy()
            LoginPage()
        elif check:
            messagebox.showerror(title="Error", message="Login już zajęty!")


class BookBrowserTest:
    def __init__(self):
        self.root = tk.Tk()
        img = ImageTk.PhotoImage(Image.open("resources/A_A.jpg"))
        panel = tk.Label(self.root, image=img)
        panel.grid(row=1, column=1)
        self.root.mainloop()


class BookBrowser:
    def __init__(self):
        self.book_browser = tk.Tk()
        self.book_browser.title("books")
        self.image_list = []
        self.checker()

        self.status = tk.Label(self.book_browser, text="Image 1 out of " + str(len(self.image_list)), bd=1,
                               relief=tk.SUNKEN, anchor=tk.E)
        img = ImageTk.PhotoImage(Image.open(self.image_list[0]))
        self.book_display = tk.Label(self.book_browser, image=img)
        self.book_display.grid(row=0, column=0, columnspan=3)

        self.button_back = tk.Button(self.book_browser, text="<<", command=lambda: self.back(2))
        self.button_forward = tk.Button(self.book_browser, text=">>", command=lambda: self.forward(2))
        if len(self.image_list) == 1:
            self.button_back = tk.Button(self.book_browser, text="<<", state=tk.DISABLED)
            self.button_forward = tk.Button(self.book_browser, text=">>", state=tk.DISABLED)
        self.button_borrow = tk.Button(self.book_browser, text="Wypozycz", command=lambda: self.wyp(self.book_list[0]))
        self.book_title = tk.Label(self.book_browser, text="Autor: " + self.book_list[0][1])
        self.book_title.grid(row=1, column=0, sticky=tk.W, columnspan=3)
        self.book_title.config(font=("Times New Roman", 14))
        self.book_author = tk.Label(self.book_browser, text="Tytul: " + self.book_list[0][2])
        self.book_author.grid(row=2, column=0, sticky=tk.W, columnspan=3)
        self.book_author.config(font=("Times New Roman", 14))
        self.button_back.grid(row=3, column=0)
        self.button_borrow.grid(row=3, column=1)
        self.button_forward.grid(row=3, column=2, pady=10)
        self.status.grid(row=4, column=0, columnspan=3, sticky=tk.W + tk.E)
        self.book_browser.protocol('WM_DELETE_WINDOW', lambda: self.back_to_main())
        self.book_browser.mainloop()

    def back_to_main(self):
        self.book_browser.destroy()
        AfterLogin()

    def back(self, img_no):
        self.book_display.grid_forget()
        self.status.grid_forget()
        self.book_title.grid_forget()
        self.book_author.grid_forget()
        self.button_borrow.grid_forget()
        img = ImageTk.PhotoImage(Image.open(self.image_list[img_no - 1]))
        self.book_display = tk.Label(self.book_browser, image=img)
        self.button_forward = tk.Button(self.book_browser, text=">>", command=lambda: self.forward(img_no + 1))
        self.button_back = tk.Button(self.book_browser, text="<<", command=lambda: self.back(img_no - 1))
        self.button_borrow = tk.Button(self.book_browser, text="Wypozycz",
                                       command=lambda: self.wyp(self.book_list[img_no - 1]))
        self.book_title = tk.Label(self.book_browser, text="Autor: " + self.book_list[img_no - 1][1])
        self.book_title.grid(row=1, column=0, sticky=tk.W, columnspan=3)
        self.book_title.config(font=("Times New Roman", 14))
        self.book_author = tk.Label(self.book_browser, text="Tytul: " + self.book_list[img_no - 1][2])
        self.book_author.grid(row=2, column=0, sticky=tk.W, columnspan=3)
        self.book_author.config(font=("Times New Roman", 14))
        self.book_display.grid(row=0, column=0, columnspan=3)
        self.status = tk.Label(self.book_browser, text="Image " + str(img_no) + " out of " + str(len(self.image_list)),
                               bd=1, relief=tk.SUNKEN, anchor=tk.E)

        if img_no == 1:
            self.button_back = tk.Button(self.book_browser, text="<<", state=tk.DISABLED)

        self.button_forward.grid(row=3, column=2)
        self.button_back.grid(row=3, column=0)
        self.button_borrow.grid(row=3, column=1)
        self.status.grid(row=4, column=0, columnspan=3, sticky=tk.W + tk.E)
        self.book_browser.mainloop()

    def forward(self, img_no):
        self.book_display.grid_forget()
        self.status.grid_forget()
        self.book_title.grid_forget()
        self.book_author.grid_forget()
        self.button_borrow.grid_forget()
        img = ImageTk.PhotoImage(Image.open(self.image_list[img_no - 1]))
        self.book_display = tk.Label(self.book_browser, image=img)
        self.button_forward = tk.Button(self.book_browser, text=">>", command=lambda: self.forward(img_no + 1))
        self.button_back = tk.Button(self.book_browser, text="<<", command=lambda: self.back(img_no - 1))
        self.button_borrow = tk.Button(self.book_browser, text="Wypozycz",
                                       command=lambda: self.wyp(self.book_list[img_no]))
        self.book_title = tk.Label(self.book_browser, text="Autor: " + self.book_list[img_no - 1][1])
        self.book_title.grid(row=1, column=0, sticky=tk.W, columnspan=3)
        self.book_title.config(font=("Times New Roman", 14))
        self.book_author = tk.Label(self.book_browser, text="Tytul: " + self.book_list[img_no - 1][2])
        self.book_author.grid(row=2, column=0, sticky=tk.W, columnspan=3)
        self.book_author.config(font=("Times New Roman", 14))
        self.book_display.grid(row=0, column=0, columnspan=3)
        self.status = tk.Label(self.book_browser, text="Image " + str(img_no) + " out of " + str(len(self.image_list)),
                               bd=1, relief=tk.SUNKEN, anchor=tk.E)

        if img_no == len(self.image_list):
            self.button_forward = tk.Button(self.book_browser, text=">>", state=tk.DISABLED)

        self.button_forward.grid(row=3, column=2)
        self.button_back.grid(row=3, column=0)
        self.button_borrow.grid(row=3, column=1)
        self.status.grid(row=4, column=0, columnspan=3, sticky=tk.W + tk.E)
        self.book_browser.mainloop()

    def wyp(self, book):
        if len(self.borrowed_books) < 3:
            db.lend_book(book, logged_user)
            messagebox.showinfo(title="Info", message="Wypożyczyłeś książkę")
            self.book_browser.destroy()
            AfterLogin()
        else:
            messagebox.showerror(title="Błąd!", message="Masz zbyt dużo wypożyczonych książek!")

    def checker(self):
        self.book_list = db.get_free_specs()
        self.borrowed_books = db.check_lendings(logged_user[0])
        self.image_list = []
        self.book_list = list(set(self.book_list) - set(self.borrowed_books))

        for book in self.book_list:
            self.image_list.append(book[3])

        if len(self.image_list) == 0:
            messagebox.showinfo(title="Info", message="Brak książek do wypożyczenia")
            self.book_browser.destroy()
            AfterLogin()


class ReturnBook(tk.Frame):
    def __init__(self, master, name, percentage, domain):
        self.percentage = percentage
        tk.Frame.__init__(self, master, bd=2, relief='raised')
        tk.Label(self, text=percentage, font=('Arial', 24), fg='#88F', width=4, anchor='w').grid(row=0, column=0, )
        tk.Label(self, text=name, font=('Aria', 16, 'bold'), fg='black', width=15, anchor='w').grid(row=0, column=1)
        tk.Label(self, text=domain, font=('Aria', 10), fg='black').grid(row=1, column=1, sticky='w')
        tk.Button(self, text='Oddaj', fg='white', bg='#44F', command=self.ret).grid(row=0, column=2, rowspan=2, padx=10)
        self.columnconfigure(1, weight=1)

    def ret(self):
        db.return_book(self.percentage, logged_user)
        messagebox.showinfo(title="Info", message="Zwrócono książkę")
        self.destroy()


LP = LoginPage()
