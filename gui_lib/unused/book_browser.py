from tkinter import *
from PIL import ImageTk, Image
import gui_lib.db_operations as db
from tkinter import messagebox


def forward(img_no, list_size):
    global book_display
    global button_forward
    global button_back
    global status
    global f

    f.grid_forget()
    book_display.grid_forget()
    status.grid_forget()
    book_display = Label(image=image_list[img_no - 1])
    button_forward = Button(book_browser, text=">>", command=lambda: forward(img_no + 1, list_size))
    button_back= Button(book_browser, text="<<", command=lambda: back(img_no - 1, list_size))
    button_quit = Button(book_browser, text="Wypozycz", command=lambda: wyp(book_list[img_no - 1]))
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
    global f

    f.grid_forget()
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

def wyp(book):
    db.lend_book(logged_user)
    messagebox.showinfo(title="Info", message="Wypozyczono książkę")

def main_window(user):
    global image_list
    global book_browser
    global book_list
    global book_display
    global status
    global logged_user

    logged_user = user

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
    book_display = Label(image=img)
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
    book_browser.protocol("WM_DELETE_WINDOW", on_closing)
    book_browser.mainloop()

def on_closing():
        book_browser.destroy()
        return True