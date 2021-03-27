import tkinter as tk
from tkinter import ttk
from functools import partial
from PIL import ImageTk, Image
from tkinter import messagebox as msg
from tkinter import scrolledtext
import sqlite3
import getpass
from tkinter import filedialog
from io import BytesIO
from pynput import keyboard
from LanguagePack import I18N
import random


class DatabaseMethods:

    def __init__(self, lang):
        self.lang = lang
        self.i18n = I18N(self.lang)

    def get_database_connection(self):
        conn = sqlite3.connect("movies.db")
        return conn

    def load_all_film_names(self):
        title = ""
        if self.lang == "tr":
            title = "tr_title"
        elif self.lang == "en":
            title = "en_title"
        filmlist = []
        try:
            conn = self.get_database_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT {title} FROM Films")
            records = cur.fetchall()
            for r in records:
                filmlist.append(r[0])

        except Exception as exc:
            print(str(exc))

        return filmlist

    def loadfilm_with_filmID(self, film_Id):
        film_name = self.find_film_names_with_filmID(film_Id)
        cat_en = self.load_categories_en_for_films(film_name, self.lang)
        cat_tr = self.load_categories_tr_for_films(film_name, self.lang)
        actors = self.load_actors_for_films(film_name, self.lang)
        director = self.load_director_name(film_name, self.lang)

        # film_ID = self.find_filmId(values[0])

        new_film = None

        try:
            conn = self.get_database_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM Films WHERE film_ID = {film_Id}")
            records = cur.fetchall()
            cur.close()
            conn.close()

            for r in records:
                new_film = Film(r[0], r[1], r[2], r[3], r[4], r[5], r[6], director, cat_tr, cat_en, actors, r[8])

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        return new_film

    def find_film_names_with_filmID(self, film_ID):
        sorgu = ""
        if self.lang == "tr":
            sorgu = "tr_title"
        elif self.lang == "en":
            sorgu = "en_title"

        name = ""

        try:
            conn = self.get_database_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT {sorgu} from Films WHERE film_ID = {film_ID}")
            records = cur.fetchall()
            r = records[0]
            name = r[0]

            cur.close()
            conn.close()

        except Exception as exc:
            print(exc)

        return name

    def load_image_from_db(self, image):
        file_image = BytesIO(image)
        img = Image.open(file_image)
        resized_pic = img.resize((200, 300), Image.ANTIALIAS)
        n_pic = ImageTk.PhotoImage(resized_pic)
        return n_pic

    def load_actors_for_films(self, title, lang):
        sorgu = tk.StringVar()
        if lang == "tr":
            sorgu = "tr_title"
        elif lang == "en":
            sorgu = "en_title"

        actor_list = []
        try:
            conn = self.get_database_connection()
            cur = conn.cursor()

            cur.execute(f"SELECT actor_name FROM Actors WHERE actor_ID IN "
                        f"(SELECT actor_ID FROM FilmActor WHERE film_Id IN "
                        f"(SELECT film_ID FROM Films WHERE {sorgu} = '{title}'))")

            records = cur.fetchall()
            for r in records:
                actor_list.append(r[0])

            cur.close()
            conn.close()

        except Exception as exc:
            print(str(exc))

        return actor_list

    def load_categories_en_for_films(self, title, lang):
        sorgu = tk.StringVar()
        catlang = "c_enName"
        if lang == "tr":
            sorgu = "tr_title"

        elif lang == "en":
            sorgu = "en_title"
        cat_list = []
        try:
            conn = self.get_database_connection()
            cur = conn.cursor()
            cur.execute(
                f"SELECT {catlang} FROM Categories WHERE c_ID IN "
                f"(SELECT c_ID FROM FilmCategory WHERE film_Id IN "
                f"(SELECT film_ID FROM Films WHERE {sorgu} = '{title}'))")
            records = cur.fetchall()
            for r in records:
                cat_list.append(r[0])
            cur.close()
            conn.close()

        except Exception as exc:
            print(str(exc))

        return cat_list

    def load_categories_tr_for_films(self, title, lang):
        sorgu = tk.StringVar()
        catlang = "c_trName"
        if lang == "tr":
            sorgu = "tr_title"

        elif lang == "en":
            sorgu = "en_title"
        cat_list = []
        try:
            conn = self.get_database_connection()
            cur = conn.cursor()
            cur.execute(
                f"SELECT {catlang} FROM Categories WHERE c_ID IN "
                f"(SELECT c_ID FROM FilmCategory WHERE film_Id IN "
                f"(SELECT film_ID FROM Films WHERE {sorgu} = '{title}'))")
            records = cur.fetchall()
            for r in records:
                cat_list.append(r[0])
            cur.close()
            conn.close()

        except Exception as exc:
            print(str(exc))

        return cat_list

    def load_director_name(self, title, lang):
        sorgu = tk.StringVar()
        dir_name = tk.StringVar()
        if lang == "tr":
            sorgu = "tr_title"
        elif lang == "en":
            sorgu = "en_title"

        try:
            conn = self.get_database_connection()
            cur = conn.cursor()
            cur.execute(
                f"SELECT d_name FROM Directors WHERE d_ID IN (SELECT d_ID FROM Films WHERE {sorgu} = '{title}')")
            records = cur.fetchall()
            r = records[0]
            dir_name.set(r[0])
            cur.close()
            conn.close()

        except Exception as exc:
            print(str(exc))

        return dir_name.get()

    def find_filmId(self, film_name):
        try:
            sorgu = ""
            if self.lang == "tr":
                sorgu = "tr_title"
            elif self.lang == "en":
                sorgu = "en_title"

            conn = self.get_database_connection()
            cur = conn.cursor()

            cur.execute(f"SELECT film_ID FROM Films WHERE {sorgu} = '{film_name}'")
            data = cur.fetchall()
            d = data[0]
            film_ID = d[0]
            cur.close()
            conn.close()
            return film_ID

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        return None


class Window1:
    def __init__(self, lang):
        self.MainPage = tk.Tk()
        self.lang = lang
        self.i18n = I18N(self.lang)
        self.MainPage.title(self.i18n.title)
        self.MainPage.iconbitmap('icons//appicon.ico')
        # self.MainPage.geometry("200x200+300+300")
        self.First_Page()

    def reload_gui_text(self, lang):
        self.i18n = I18N(lang)
        self.MainPage.title(self.i18n.title)
        self.buttonAdmin.configure(text=self.i18n.bAdmin)
        self.buttonGuest.configure(text=self.i18n.bGuest)
        self.buttonLanguage.configure(text=self.i18n.bLanguage)

    def buttonAdminPage(self):
        # self.MainPage.withdraw()
        x_konumu = self.MainPage.winfo_x()
        y_konumu = self.MainPage.winfo_y()
        self.MainPage.destroy()
        w2 = Window2(self.lang)
        w2.win.geometry(f"+{x_konumu}+{y_konumu}")
        w2.win.focus_force()

    def buttonGuestPage(self):
        self.MainPage.destroy()
        w5 = Window5(self.lang)
        w5.GuestPage.focus_force()

    def buttonLang(self):
        if (self.LangSet.get()) == "English":
            self.lang = "en"
            self.reload_gui_text("en")
        elif (self.LangSet.get()) == "Türkçe":
            self.lang = "tr"
            self.reload_gui_text("tr")
        else:
            pass

    def First_Page(self):
        self.headline = tk.Label(self.MainPage, text="Film Catalogue", bg="#1FFBFF", width="25", height="2",
                                 font=("Brush Script MT", 22))
        self.headline.grid(row=0, column=0, columnspan=2)

        self.buttonAdmin = ttk.Button(self.MainPage, text=self.i18n.bAdmin, command=self.buttonAdminPage)
        self.buttonAdmin.grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky="WENS")
        self.buttonGuest = ttk.Button(self.MainPage, text=self.i18n.bGuest, command=self.buttonGuestPage)
        self.buttonGuest.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky="WENS")
        self.LangSet = tk.StringVar()
        self.comboBox = ttk.Combobox(self.MainPage, textvariable=self.LangSet, values=("Türkçe", "English"),
                                     state='readonly')
        self.comboBox.grid(column=0, row=3, columnspan=1, padx=5, pady=5, sticky="WENS")

        self.comboBox.current(1)
        if self.lang == "en":
            self.comboBox.current(1)
        elif self.lang == "tr":
            self.comboBox.current(0)

        self.buttonLanguage = ttk.Button(self.MainPage, text=self.i18n.bLanguage, command=self.buttonLang)
        self.buttonLanguage.grid(column=1, row=3, columnspan=1, padx=5, pady=5, sticky="WENS")


class Window2:
    def __init__(self, lang):
        self.win = tk.Tk()
        self.lang = lang
        self.i18n = I18N(self.lang)
        self.win.title(self.i18n.title)
        # self.win.geometry("330x165+710+290")
        self.user_name = tk.StringVar()
        self.user_password = tk.StringVar()
        self.users = []
        self.create_widgets()

    def reload_gui_text(self, lang):
        self.i18n = I18N(lang)
        self.win.title(self.i18n.title)
        self.lbl_user_name.configure(text=self.i18n.lblUsername)
        self.lbl_user_password.configure(text=self.i18n.lblPassword)
        self.buttonLogin.configure(text=self.i18n.bLogin)
        self.buttonRegister.configure(text=self.i18n.bRegister)
        self.buttonBack.configure(text=self.i18n.bHomePage)

    def load_all_users(self):
        conn = DatabaseMethods(self.lang).get_database_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User")
        records = cursor.fetchall()

        for r in records:
            u = User(r[1], r[2])
            # print(u)
            self.users.append(u)

    def find_user(self, username):
        u = None
        self.users = []
        self.load_all_users()
        for i in range(len(self.users)):
            user: User = self.users[i]
            # print("for döngüsü", user)
            if user.get_username() == username:
                u = user
                # print("Find", user)
        return u

    def find_username(self, username):
        self.users = []
        self.load_all_users()

        for i in range(len(self.users)):
            user: User = self.users[i]
            if user.get_username() == username:
                return True
        return False

    def buttonLoginPage(self):

        u = self.find_user(self.txt_user_name.get())
        if u is None:
            msg.showerror(self.i18n.warning1, self.i18n.warning2)
        else:
            if u.get_password() != self.txt_user_password.get():
                msg.showerror(self.i18n.warning1, self.i18n.warning3)
            if u.get_password() == self.txt_user_password.get():
                print("Sisteme Girildi.")
                x_konumu = self.win.winfo_x()
                y_konumu = self.win.winfo_y()
                self.win.destroy()
                w3 = Window3(self.lang)
                w3.EditMovie.geometry(f"+{x_konumu}+{y_konumu}")
                w3.EditMovie.focus_force()

    def buttonRegisterPage(self):
        if self.find_username(self.txt_user_name.get()):
            msg.showerror(self.i18n.Error1, self.i18n.problem3)
        else:
            if len(self.txt_user_password.get()) >= 3 and len(self.txt_user_name.get()) >= 3:

                # conn = sqlite3.connect("movies.db")
                conn = DatabaseMethods(self.lang).get_database_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO User(userName,userPassword) VALUES(:name,:password)",
                               {"name": self.txt_user_name.get(),
                                "password": self.txt_user_password.get()
                                })
                conn.commit()
                conn.close()
                msg.showinfo(self.i18n.done1, self.i18n.done2)

            else:
                if len(self.txt_user_name.get()) == 0 and len(self.txt_user_password.get()) == 0:
                    msg.showerror(self.i18n.Error1, self.i18n.problem1)
                else:
                    msg.showerror(self.i18n.Error1, self.i18n.problem2)

    def buttonBackPage(self):
        x_konumu = self.win.winfo_x()
        y_konumu = self.win.winfo_y()
        self.win.destroy()
        w1 = Window1(self.lang)
        w1.MainPage.geometry(f"+{x_konumu}+{y_konumu}")
        w1.MainPage.focus_force()

    def checkbutton_handler(self):
        if self.passvar.get() == 0:
            self.txt_user_password.configure(show="*")
        elif self.passvar.get() == 1:
            self.txt_user_password.configure(show="")

    def create_widgets(self):
        self.headline = tk.Label(self.win, text="Film Catalogue", bg="#1FFBFF", width="25", height="2",
                                 font=("Brush Script MT", 22))
        self.headline.grid(row=0, column=0, columnspan=3)

        # LABEL
        self.lbl_user_name = ttk.Label(self.win, text=self.i18n.lblUsername)
        self.lbl_user_name.grid(column=0, row=1, padx=5, pady=5)
        self.lbl_user_password = ttk.Label(self.win, text=self.i18n.lblPassword)
        self.lbl_user_password.grid(column=0, row=2, padx=5, pady=5)

        # TEXT BOX
        self.txt_user_name = ttk.Entry(self.win, textvariable=self.user_name, width=35)
        self.txt_user_name.grid(column=1, row=1, padx=5, pady=5, columnspan=2)
        self.txt_user_password = ttk.Entry(self.win, textvariable=self.user_password, width=35, show="*")
        self.txt_user_password.grid(column=1, row=2, padx=5, pady=5, columnspan=2)
        # BUTTON
        # self.button_register = ttk.Button(self.win, text="Login", command=self.login)
        # self.button_register.grid(column=0, row=3, columnspan=2, padx=5, pady=5)
        self.passvar = tk.IntVar()
        ch_show = ttk.Checkbutton(self.win, text=self.i18n.cpassword, variable=self.passvar,
                                  command=self.checkbutton_handler)
        ch_show.grid(row=3, column=1)

        self.buttonLogin = ttk.Button(self.win, text=self.i18n.bLogin, command=self.buttonLoginPage)
        self.buttonLogin.grid(column=0, row=5, columnspan=1, padx=5, pady=5, sticky="WENS")
        self.buttonRegister = ttk.Button(self.win, text=self.i18n.bRegister, command=self.buttonRegisterPage)
        self.buttonRegister.grid(column=1, row=5, columnspan=1, padx=5, pady=5, sticky="WENS")
        self.buttonBack = ttk.Button(self.win, text=self.i18n.bHomePage, command=self.buttonBackPage)
        self.buttonBack.grid(column=2, row=5, columnspan=1, padx=5, pady=5, sticky="WENS")


class Window3:
    def __init__(self, lang):
        self.EditMovie = tk.Tk()
        self.lang = lang
        self.i18n = I18N(self.lang)
        self.EditMovie.title(self.i18n.title)
        self.EditMovie.iconbitmap('icons//appicon.ico')
        # self.MainPage.geometry("200x200+300+300")
        self.lang = lang
        self.Movie_Edit()

    def reload_gui_text(self, lang):
        self.i18n = I18N(lang)
        self.EditMovie.title(self.i18n.title)
        self.buttonAdd.configure(text=self.i18n.bAdd)
        self.buttonRemove.configure(text=self.i18n.bRemove)
        self.buttonPrevious.configure(text=self.i18n.bHomePage)

    def AddButton(self):
        self.EditMovie.destroy()
        add = AddPage(self.lang)
        add.win.focus_force()

    def RemoveButton(self):
        self.EditMovie.destroy()
        del_page = DeletePage(self.lang)
        del_page.win.focus_force()

    def PreviousButton(self):
        x_konumu = self.EditMovie.winfo_x()
        y_konumu = self.EditMovie.winfo_y()
        self.EditMovie.destroy()
        w1 = Window1(self.lang)
        w1.MainPage.geometry(f"+{x_konumu}+{y_konumu}")
        w1.MainPage.focus_force()

    def Movie_Edit(self):
        self.headline = tk.Label(self.EditMovie, text="Film Catalogue", bg="#1FFBFF", width="25", height="2",
                                 font=("Brush Script MT", 22))
        self.headline.grid(row=0, column=0, columnspan=3)

        self.buttonAdd = ttk.Button(self.EditMovie, text=self.i18n.bAdd, command=self.AddButton)
        self.buttonAdd.grid(column=0, row=2, columnspan=3, padx=5, pady=5, sticky="WENS")
        self.buttonRemove = ttk.Button(self.EditMovie, text=self.i18n.bRemove, command=self.RemoveButton)
        self.buttonRemove.grid(column=0, row=3, columnspan=3, padx=5, pady=5, sticky="WENS")
        self.buttonPrevious = ttk.Button(self.EditMovie, text=self.i18n.bHomePage, command=self.PreviousButton)
        self.buttonPrevious.grid(column=0, row=4, columnspan=3, padx=5, pady=5, sticky="WENS")


class Window5:
    def __init__(self, lang):
        self.GuestPage = tk.Tk()
        self.lang = lang
        self.i18n = I18N(self.lang)
        self.GuestPage.title(self.i18n.title)
        self.GuestPage.iconbitmap('icons//appicon.ico')
        # self.MainPage.geometry("200x200+300+300")
        self.lang = lang
        # self.film: Film = film
        self.filmtitle = tk.StringVar()
        self.describ = tk.StringVar()
        self.year = tk.IntVar()
        self.director = tk.StringVar()
        self.imdb = tk.DoubleVar()
        self.update_lang(self.lang)
        self.Guest_Page()

    def reload_gui_text(self, lang):
        self.i18n = I18N(lang)
        self.GuestPage.title(self.i18n.title)
        self.buttonFilter.configure(text=self.i18n.bFilter)
        self.buttonSearch.configure(text=self.i18n.bSearch)
        self.buttonRandom.configure(text=self.i18n.bRandom)
        self.buttonBackPage.configure(text=self.i18n.bPrevious)

    def FilterButton(self):
        self.GuestPage.destroy()
        f = Filter(self.lang)
        f.win.focus_force()

    def SearchButton(self):
        self.GuestPage.destroy()
        s = SearchPage(self.lang)
        s.win.focus_force()

    def BackPageButton(self):
        self.GuestPage.destroy()
        w1 = Window1(self.lang)
        w1.MainPage.focus_force()

    def RandomButton(self):
        for widget in self.recommended_frame.winfo_children():
            widget.destroy()

        dm = DatabaseMethods(self.lang)

        # film_names = self.load_all_film_names()
        film_names = dm.load_all_film_names()
        rn = random.randint(0, len(film_names) - 1)
        name = film_names[rn]
        # print("Film Name", name)
        film_ID = dm.find_filmId(name)
        film = dm.loadfilm_with_filmID(film_ID)
        self.load_filmdatas(film, self.lang)

        showPoster = tk.Frame(self.recommended_frame, width=380, height=450, bg="#BFBDBD")
        showPoster.grid(row=0, column=0, padx=10, pady=10)
        showDesc = tk.Frame(self.recommended_frame, width=380, height=450)
        showDesc.grid(row=0, column=1, padx=0, pady=0)

        self.lbl_title = tk.Label(showPoster, text=self.filmtitle.get(), font=("Helvetica", 14))
        self.lbl_title.grid(row=0, column=0, padx=10, pady=10)

        self.scr = scrolledtext.ScrolledText(showDesc, font=("Arial", 14), height=17, width=40, wrap=tk.WORD,
                                             state=tk.DISABLED)
        self.scr.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.insert_texts()

        global resized_pic
        image = Image.open('unknown.png')
        resized = image.resize((200, 300), Image.ANTIALIAS)
        resized_pic = ImageTk.PhotoImage(resized)

        resized_pic = dm.load_image_from_db(film.__getattribute__("image"))

        self.label_image = tk.Label(showPoster, image=resized_pic)
        self.label_image.grid(row=1, column=0, padx=20, pady=20)

    def update_lang(self, lang):
        if lang == "tr":
            self.desc = "Konu : "
            self.stars = "Aktörler/Aktrisler : "
            self.directed_by = "Yönetmen : "
            self.ctg = "Kategoriler : "
            self.time = "Yıl: "

        elif lang == "en":
            self.desc = "Description : "
            self.stars = "Actors/Actresses : "
            self.directed_by = "Director : "
            self.ctg = "Categories : "
            self.time = "Year : "

    def insert_texts(self):
        self.scr.configure(state=tk.NORMAL)
        self.scr.insert(tk.INSERT, "\n" + self.desc + self.describ.get() + "\n\n")
        self.scr.insert(tk.INSERT, self.directed_by + self.director.get() + "\n\n")
        stractors = ""
        for i in range(len(self.actors)):
            if i == 0:
                stractors += self.actors[i]
            else:
                stractors += ", " + self.actors[i]

        self.scr.insert(tk.INSERT, self.stars + stractors + "\n\n")

        strcat = ""
        for i in range(len(self.categories)):
            if i == 0:
                strcat += self.categories[i]
            else:
                strcat += ", " + self.categories[i]

        self.scr.insert(tk.INSERT, self.ctg + strcat + "\n\n")

        self.scr.insert(tk.INSERT, self.time + str(self.year.get()) + "\n\n")
        self.scr.insert(tk.INSERT, "Imdb : " + str(self.imdb.get()))

        self.scr.configure(state=tk.DISABLED)

    def load_filmdatas(self, film, lang):
        if lang == "tr":
            self.filmtitle.set(film.__getattribute__("tr_title"))
            self.describ.set(film.__getattribute__("tr_desc"))
            self.categories = film.__getattribute__("categories_tr")
        elif lang == "en":
            self.filmtitle.set(film.__getattribute__("en_title"))
            self.describ.set(film.__getattribute__("en_desc"))
            self.categories = film.__getattribute__("categories_en")

        self.actors = film.__getattribute__("actors")
        self.director.set(film.__getattribute__("director"))
        self.year.set(film.__getattribute__("year"))
        self.imdb.set(film.__getattribute__("imdb"))
        img_data = film.__getattribute__("image")
        file_image = BytesIO(img_data)
        img = Image.open(file_image)
        resized_pic = img.resize((200, 300), Image.ANTIALIAS)
        n_pic = ImageTk.PhotoImage(resized_pic)
        self.photo = n_pic

    def Guest_Page(self):
        self.headline = tk.Label(self.GuestPage, text="Film Catalogue", bg="#1FFBFF", width="40", height="2",
                                 font=("Brush Script MT", 22))
        self.headline.grid(row=0, column=0, columnspan=4, sticky="WENS")

        self.recommended_frame = tk.Frame(self.GuestPage)
        self.recommended_frame.grid(row=1, column=0, columnspan=4)

        self.RandomButton()
        # self.recommended = tk.Label(self.GuestPage, text="Recommended", width="22", height="2")
        # self.recommended.grid(row=1, column=0, columnspan=3)
        self.buttonFilter = ttk.Button(self.GuestPage, text=self.i18n.bFilter, command=self.FilterButton)
        self.buttonFilter.grid(column=0, row=2, columnspan=1, padx=5, pady=5, sticky="WENS")

        self.buttonSearch = ttk.Button(self.GuestPage, text=self.i18n.bSearch, command=self.SearchButton)
        self.buttonSearch.grid(column=1, row=2, columnspan=1, padx=5, pady=5, sticky="WENS")

        self.buttonRandom = ttk.Button(self.GuestPage, text=self.i18n.bRandom, command=self.RandomButton)
        self.buttonRandom.grid(column=2, row=2, columnspan=1, padx=5, pady=5, sticky="WENS")

        self.buttonBackPage = ttk.Button(self.GuestPage, text=self.i18n.bPrevious, command=self.BackPageButton)
        self.buttonBackPage.grid(column=3, row=2, columnspan=1, padx=5, pady=5, sticky="WENS")


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def __str__(self):
        return f"username: {self.username}, password: {self.password}"


class AddPage:
    def __init__(self, lang):
        self.win = tk.Tk()
        self.lang = lang
        self.i18n = I18N(self.lang)
        self.imgDirectory = ""
        self.win.title(self.i18n.title)
        # self.win.geometry("700x400")
        self.create_widgets()

    def reload_gui_text(self, lang):
        self.i18n = I18N(lang)
        self.win.title(self.i18n.title)
        self.window_director.title(self.i18n.dtitle)
        self.label_title_tr.configure(text=self.i18n.trtitle)
        self.label_title_en.configure(text=self.i18n.entitle)
        self.label_desc_tr.configure(text=self.i18n.trdesc)
        self.label_desc_en.configure(text=self.i18n.endesc)
        self.btn_add_director.configure(text=self.i18n.AddDir)
        self.btn_choose_actor.configure(text=self.i18n.AddAct)
        self.lbl_year.configure(text=self.i18n.lblyear)
        # self.lbl_imdb.configure(text=self.i18n.)
        self.btn_save.configure(text=self.i18n.bSave)
        self.btn_back.configure(text=self.i18n.bPrevious)
        self.lbl_name.configure(text=self.i18n.dName)
        self.btn_add_director.configure(text=self.i18n.dAdd)
        self.btn_select_image.configure(text=self.i18n.sImage)

    def selectImage(self):
        try:
            self.imgDirectory = ""
            user = getpass.getuser()
            global resized_pic
            self.imageDir = tk.filedialog.askopenfilename(initialdir='C:/Users/%s' % user, title="Select a image",
                                                          filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
            selectedImage = Image.open(self.imageDir)
            resized = selectedImage.resize((200, 300), Image.ANTIALIAS)
            resized_pic = ImageTk.PhotoImage(resized)
            self.label_image.configure(image=resized_pic)
            self.imgDirectory = self.imageDir
            # print(self.imgDirectory)

        except Exception as exc:
            print("Resim seçilmedi")

    def load_categories(self, lang):
        conn = DatabaseMethods(self.lang).get_database_connection()
        cur = conn.cursor()
        cur.execute("""SELECT * FROM Categories""")
        records = cur.fetchall()
        ctglist = []
        if lang == "tr":
            for r in records:
                ctglist.append(r[1])

        elif lang == "en":
            for r in records:
                ctglist.append(r[2])

        return ctglist

    def add_actors(self):
        self.scr_actors.config(state="normal")

        self.cast.append(self.entry_actor.get())
        if self.scr_actors.get("1.0", tk.END) == "\n":
            self.scr_actors.insert(tk.INSERT, self.entry_actor.get())
        else:
            self.scr_actors.insert(tk.INSERT, ", " + self.entry_actor.get())

        self.scr_actors.config(state="disabled")

        if not self.check_actors(self.entry_actor.get()):
            try:
                conn = DatabaseMethods(self.lang).get_database_connection()
                cur = conn.cursor()
                cur.execute(f"INSERT INTO Actors (actor_name) VALUES ('{self.entry_actor.get()}') ")
                conn.commit()
                cur.close()
                conn.close()

            except Exception as exc:
                msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

    def load_all_actors(self):
        all_actors = []
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute("SELECT actor_name FROM Actors")
            records = cur.fetchall()
            for r in records:
                all_actors.append(r[0])

            cur.close()
            conn.close()

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        return all_actors

    def check_actors(self, actor_name):
        all_actors = self.load_all_actors()
        for a in all_actors:
            if a == actor_name:
                return True
        return False

    def load_directors(self):
        directors = []
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute("SELECT d_name FROM Directors")
            data = cur.fetchall()
            for d in data:
                directors.append(d[0])
            conn.commit()
            cur.close()
            conn.close()

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        return directors

    def find_actor_in_db(self, actor_name):
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT actor_ID FROM Actors WHERE actor_name = '{actor_name}'")
            data = cur.fetchall()
            # print(len(data))
            cur.close()
            conn.close()
            d = data[0]
            return d[0]

        except Exception as exc:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute(f"INSERT INTO Actors(actor_name) VALUES ('{actor_name}')")
            conn.commit()
            cur.execute(f"SELECT actor_ID FROM Actors WHERE actor_name = '{actor_name}'")
            data = cur.fetchall()
            cur.close()
            conn.close()
            print(str(exc))
            d = data[0]
            return d[0]
            # msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

    def add_filmActors(self, film_name_en, film_name_tr, actorlist):

        try:
            dm = DatabaseMethods(self.lang)
            # film_ID = self.find_filmId(film_name)
            film_ID = 0
            if self.lang == "tr":
                film_ID = dm.find_filmId(film_name_tr)
            elif self.lang == "en":
                film_ID = dm.find_filmId(film_name_en)

            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()

            for actor in actorlist:
                act_id = self.find_actor_in_db(actor)
                cur.execute(f"INSERT INTO FilmActor (actor_ID, film_ID) VALUES ({act_id}, {film_ID})")

            conn.commit()
            cur.close()
            conn.close()

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

    def find_category_in_db(self, category, lang):
        catlang = tk.StringVar()
        if lang == "tr":
            catlang = "c_trName"
        if lang == "en":
            catlang = "c_enName"
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            query = f"SELECT c_ID FROM Categories WHERE {catlang} = '{category}'"
            # print(query)
            cur.execute(query)
            data = cur.fetchall()
            d = data[0]
            # print(d[0])
            cur.close()
            conn.close()
            return d[0]

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        return None

    def check_categories(self, film_name_en, film_name_tr):

        categories = []
        for i in range(len(self.chvars)):
            if self.chvars[i].get() == 1:
                c: tk.Checkbutton = self.checkbuttons[i]
                categories.append(c.cget("text"))

        dm = DatabaseMethods(self.lang)
        film_ID = 0
        if self.lang == "tr":
            film_ID = dm.find_filmId(film_name_tr)
        elif self.lang == "en":
            film_ID = dm.find_filmId(film_name_en)

        for c in categories:
            cid = self.find_category_in_db(c, self.lang)
            # print("cid: ", cid)

            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            query = f"INSERT INTO FilmCategory(c_ID, film_ID) VALUES ({cid}, {film_ID})"
            # print(query)
            cur.execute(f"INSERT INTO FilmCategory(c_ID, film_ID) VALUES ({cid}, {film_ID})")
            conn.commit()
            cur.close()
            conn.close()

    def find_director_id(self, director_name):
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT d_id FROM Directors WHERE d_name = '{director_name}'")
            data = cur.fetchall()
            d = data[0]
            cur.close()
            conn.close()
            return d[0]

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        return None

    def click_director(self):
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute(f"INSERT INTO Directors (d_name) VALUES ('{self.entry_director_name.get()}')")

            conn.commit()
            cur.close()
            conn.close()

            msg.showinfo("", self.i18n.done3)

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        self.update_combobox()

    def add_director(self):
        self.window_director = tk.Toplevel()
        self.window_director.title(self.i18n.dtitle)
        self.lbl_name = tk.Label(self.window_director, text=self.i18n.dName)
        self.lbl_name.grid(row=0, column=0, padx=5, pady=5)
        self.entry_director_name = ttk.Entry(self.window_director, width=20)
        self.entry_director_name.grid(row=0, column=1, padx=5, pady=5)
        self.btn_add_director = tk.Button(self.window_director, text=self.i18n.dAdd, command=self.click_director)
        self.btn_add_director.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def update_combobox(self):
        directors = sorted(self.load_directors())
        self.comboBox.configure(values=directors)

    def film_save(self):
        try:
            self.ctglen = 0
            for i in range(len(self.chvars)):
                if self.chvars[i].get() == 1:
                    self.ctglen += 1

            if len(self.entry_title_tr.get()) != 0 and len(self.entry_title_en.get()) != 0 and len(
                    self.scr_desc_tr.get("1.0", tk.END)) != 0 and len(self.scr_desc_en.get("1.0", tk.END)) != 0 and len(
                self.entry_imdb.get()) != 0 and len(
                self.entry_year.get()) != 0 and self.ctglen != 0 and self.imgDirectory != "" and self.director.get() != self.i18n.chooseDirector and len(
                self.cast) != 0:

                # print(self.imgDirectory)

                conn = DatabaseMethods(self.lang).get_database_connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO Films (tr_title, en_title, tr_desc, en_desc, image, imdb, d_ID, year) "
                            "VALUES (:trt, :ent, :trdsc, :endsc, :image, :imdb, :d_ID, :year)",
                            {"trt": self.entry_title_tr.get(),
                             "ent": self.entry_title_en.get(),
                             "trdsc": self.scr_desc_tr.get("1.0", tk.END),
                             "endsc": self.scr_desc_en.get("1.0", tk.END),
                             "image": self.image_to_blob(self.imgDirectory),
                             "imdb": self.entry_imdb.get(),
                             "d_ID": self.find_director_id(self.director.get()),
                             "year": self.entry_year.get()})

                conn.commit()
                cur.close()
                conn.close()

                self.check_categories(self.entry_title_en.get(), self.entry_title_tr.get())
                self.add_filmActors(self.entry_title_en.get(), self.entry_title_tr.get(), self.cast)

                # self.scr_actors.get("1.0", tk.END)
                self.scr_actors.config(state=tk.NORMAL)
                self.scr_actors.delete("1.0", tk.END)
                self.cast = []
                self.scr_actors.config(state=tk.DISABLED)
                msg.showinfo("", self.i18n.msave)

            elif len(self.entry_title_tr.get()) == 0 and len(self.entry_title_en.get()) == 0 and len(
                    self.scr_desc_tr.get("1.0", tk.END)) == 1 and len(self.scr_desc_en.get("1.0", tk.END)) == 1 and len(
                self.entry_imdb.get()) == 0 and len(
                self.entry_year.get()) == 0 and self.ctglen == 0 and len(self.imgDirectory) == 0:
                msg.showerror(self.i18n.Error1, self.i18n.problem1)
            elif len(self.entry_title_tr.get()) == 0:
                msg.showerror(self.i18n.Error1, self.i18n.pAdd1)
            elif len(self.entry_title_en.get()) == 0:
                msg.showerror(self.i18n.Error1, self.i18n.pAdd2)
            elif len(self.scr_desc_tr.get(1.0, tk.END)) == 1:
                msg.showerror(self.i18n.Error1, self.i18n.pAdd3)
            elif len(self.scr_desc_en.get(1.0, tk.END)) == 1:
                msg.showerror(self.i18n.Error1, self.i18n.pAdd4)
            elif self.ctglen == 0:
                msg.showerror(self.i18n.Error1, self.i18n.pAdd5)
            elif self.director.get() == self.i18n.chooseDirector:
                msg.showerror(self.i18n.Error1, self.i18n.pAdd6)
            elif len(self.cast) == 0:
                msg.showerror(self.i18n.Error1, self.i18n.pAdd7)
            elif len(self.entry_imdb.get()) == 0:
                msg.showerror(self.i18n.Error1, self.i18n.pAdd8)
            elif len(self.entry_year.get()) == 0:
                msg.showerror(self.i18n.Error1, self.i18n.pAdd9)
            elif len(self.imgDirectory) == 0:
                msg.showerror(self.i18n.Error1, self.i18n.pAdd10)
            else:
                msg.showerror(self.i18n.Error1, self.i18n.problem1)

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))
            print("error burda")

    def convertToBinaryData(self, filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    def image_to_blob(self, directory):
        blobPic = self.convertToBinaryData(directory)
        return blobPic

    def back_btn(self):
        self.win.destroy()
        w3 = Window3(self.lang)
        w3.EditMovie.focus_force()

    def create_widgets(self):
        frameMovie = tk.Frame(self.win, width=800, height=450)
        frameMovie.grid(row=0, column=0, padx=10, pady=10)

        framePoster = tk.Frame(frameMovie, width=380, height=450, bg="#BFBDBD")
        framePoster.grid(row=0, column=0, padx=10, pady=10)

        frameDesc = tk.Frame(frameMovie, width=380, height=450)
        frameDesc.grid(row=0, column=1, padx=0, pady=0, sticky="NSEW")

        canvas = tk.Canvas(frameDesc)
        scrollbar = ttk.Scrollbar(frameDesc, orient="vertical", command=canvas.yview)
        info_frame = tk.Frame(canvas)
        info_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=info_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.label_title_tr = tk.Label(info_frame, text=self.i18n.trtitle)
        self.label_title_tr.grid(row=0, column=0, padx=5, pady=5)
        self.entry_title_tr = ttk.Entry(info_frame, width=30)
        self.entry_title_tr.grid(row=0, column=1, padx=5, pady=5)

        self.label_title_en = tk.Label(info_frame, text=self.i18n.entitle)
        self.label_title_en.grid(row=1, column=0, padx=5, pady=5)
        self.entry_title_en = ttk.Entry(info_frame, width=30)
        self.entry_title_en.grid(row=1, column=1, padx=5, pady=5)

        self.label_desc_tr = tk.Label(info_frame, text=self.i18n.trdesc)
        self.label_desc_tr.grid(row=2, column=0, padx=5, pady=5)
        self.scr_desc_tr = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, width=25, height=1)
        self.scr_desc_tr.grid(row=2, column=1, padx=5, pady=5)

        self.label_desc_en = tk.Label(info_frame, text=self.i18n.endesc)
        self.label_desc_en.grid(row=3, column=0, padx=5, pady=5)
        self.scr_desc_en = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, width=25, height=1)
        self.scr_desc_en.grid(row=3, column=1, padx=5, pady=5)

        # btn_choose_ctg = tk.Button(info_frame, text="Choose Categories", height=2)
        # btn_choose_ctg.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        ctglist = self.load_categories(self.lang)

        self.checkbuttons = []
        self.chvars = []

        self.ch1var = tk.IntVar()
        self.ch2var = tk.IntVar()
        self.ch3var = tk.IntVar()
        self.ch4var = tk.IntVar()
        self.ch5var = tk.IntVar()
        self.ch6var = tk.IntVar()
        self.ch7var = tk.IntVar()
        self.ch8var = tk.IntVar()
        self.ch9var = tk.IntVar()
        self.ch10var = tk.IntVar()
        self.ch11var = tk.IntVar()
        self.ch12var = tk.IntVar()

        self.chvars.append(self.ch1var)
        self.chvars.append(self.ch2var)
        self.chvars.append(self.ch3var)
        self.chvars.append(self.ch4var)
        self.chvars.append(self.ch5var)
        self.chvars.append(self.ch6var)
        self.chvars.append(self.ch7var)
        self.chvars.append(self.ch8var)
        self.chvars.append(self.ch9var)
        self.chvars.append(self.ch10var)
        self.chvars.append(self.ch11var)
        self.chvars.append(self.ch12var)

        self.ch1 = tk.Checkbutton(info_frame, text=ctglist[0], variable=self.ch1var)
        self.ch2 = tk.Checkbutton(info_frame, text=ctglist[1], variable=self.ch2var)
        self.ch3 = tk.Checkbutton(info_frame, text=ctglist[2], variable=self.ch3var)
        self.ch4 = tk.Checkbutton(info_frame, text=ctglist[3], variable=self.ch4var)
        self.ch5 = tk.Checkbutton(info_frame, text=ctglist[4], variable=self.ch5var)
        self.ch6 = tk.Checkbutton(info_frame, text=ctglist[5], variable=self.ch6var)
        self.ch7 = tk.Checkbutton(info_frame, text=ctglist[6], variable=self.ch7var)
        self.ch8 = tk.Checkbutton(info_frame, text=ctglist[7], variable=self.ch8var)
        self.ch9 = tk.Checkbutton(info_frame, text=ctglist[8], variable=self.ch9var)
        self.ch10 = tk.Checkbutton(info_frame, text=ctglist[9], variable=self.ch10var)
        self.ch11 = tk.Checkbutton(info_frame, text=ctglist[10], variable=self.ch11var)
        self.ch12 = tk.Checkbutton(info_frame, text=ctglist[11], variable=self.ch12var)

        self.ch1.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch2.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        self.ch3.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch4.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        self.ch5.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch6.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        self.ch7.grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch8.grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)
        self.ch9.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch10.grid(row=8, column=1, sticky=tk.W, padx=5, pady=5)
        self.ch11.grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch12.grid(row=9, column=1, sticky=tk.W, padx=5, pady=5)

        self.checkbuttons.append(self.ch1)
        self.checkbuttons.append(self.ch2)
        self.checkbuttons.append(self.ch3)
        self.checkbuttons.append(self.ch4)
        self.checkbuttons.append(self.ch5)
        self.checkbuttons.append(self.ch6)
        self.checkbuttons.append(self.ch7)
        self.checkbuttons.append(self.ch8)
        self.checkbuttons.append(self.ch9)
        self.checkbuttons.append(self.ch10)
        self.checkbuttons.append(self.ch11)
        self.checkbuttons.append(self.ch12)

        self.director = tk.StringVar()
        directors = ["Ertem Eğilmez", "NBC", "Çağan Irmak"]
        self.director.set(self.i18n.chooseDirector)

        directors = sorted(self.load_directors())

        self.comboBox = ttk.Combobox(info_frame, textvariable=self.director, values=directors,
                                     state='readonly', width=15)

        self.comboBox.grid(row=10, column=0, padx=5, pady=5)

        self.btn_add_director = tk.Button(info_frame, text=self.i18n.AddDir, command=self.add_director)
        self.btn_add_director.grid(row=10, column=1, padx=5, pady=5)

        self.entry_actor = ttk.Entry(info_frame, width=20)
        self.entry_actor.grid(row=11, column=0, padx=5, pady=5)

        self.cast = []

        self.btn_choose_actor = tk.Button(info_frame, text=self.i18n.AddAct, command=self.add_actors)
        self.btn_choose_actor.grid(row=12, column=0, padx=5, pady=5)

        self.scr_actors = scrolledtext.ScrolledText(info_frame, width=25, height=1, state="disabled", wrap=tk.WORD)
        self.scr_actors.grid(row=11, column=1, padx=5, pady=5, rowspan=2)

        self.lbl_year = tk.Label(info_frame, text=self.i18n.lblyear)
        self.lbl_year.grid(row=13, column=0, padx=5, pady=5)

        self.entry_year = ttk.Entry(info_frame, width=30)
        self.entry_year.grid(row=13, column=1, padx=5, pady=5)

        self.lbl_imdb = tk.Label(info_frame, text="Imdb :")
        self.lbl_imdb.grid(row=14, column=0, padx=5, pady=5)

        self.entry_imdb = ttk.Entry(info_frame, width=30)
        self.entry_imdb.grid(row=14, column=1, padx=5, pady=5)

        self.btn_save = tk.Button(info_frame, text=self.i18n.bSave, command=self.film_save)
        self.btn_save.grid(row=15, column=0, padx=5, pady=5, columnspan=2)

        self.btn_back = tk.Button(info_frame, text=self.i18n.bPrevious, command=self.back_btn)
        self.btn_back.grid(row=16, column=0, padx=5, pady=5, columnspan=2)

        global resized_pic
        image = Image.open('unknown.png')
        # img = ImageTk.PhotoImage(Image.open('unknown.png'))
        resized = image.resize((200, 300), Image.ANTIALIAS)
        resized_pic = ImageTk.PhotoImage(resized)

        self.label_image = tk.Label(framePoster, image=resized_pic)
        self.label_image.grid(row=0, column=0, padx=10, pady=10)
        self.btn_select_image = tk.Button(framePoster, text=self.i18n.sImage, command=self.selectImage)
        self.btn_select_image.grid(row=1, column=0, padx=10, pady=10)


class DeletePage:
    def __init__(self, lang):
        self.win = tk.Tk()
        self.lang = lang
        self.i18n = I18N(self.lang)
        self.win.title(self.i18n.deletetitle)
        self.win.geometry("750x270+710+290")
        self.create_widgets()
        self.list_grades()

    def reload_gui_text(self, lang):
        self.i18n = I18N(lang)
        self.win.title(self.i18n.deletetitle)
        self.Back_Page.configure(text=self.i18n.bPrevious)

    def on_double_click(self, event):
        selected_items = self.treeview.selection()
        values = self.treeview.item(selected_items)['values']
        # print(values[0])
        tr_name = values[0]
        en_name = values[1]
        answer = None
        value = None
        if self.lang == "tr":
            answer = msg.askyesno("Sil", f"{tr_name} silmek istediğine emin misin ?")
            value = values[0]
        elif self.lang == "en":
            answer = msg.askyesno("Delete", f"Are you sure you want to delete {en_name}?")
            value = values[1]

        # print("Answer", answer)
        if answer:
            self.delete_film(DatabaseMethods(self.lang).find_filmId(value))
            # self.delete_film(DatabaseMethods(self.lang).find_filmId(values[1]))

    def delete_film(self, film_id):
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute(f"DELETE FROM Films WHERE film_ID = {film_id}")
            cur.execute(f"DELETE FROM FilmCategory WHERE film_ID = {film_id}")
            cur.execute(f"DELETE FROM FilmActor WHERE film_ID = {film_id}")
            conn.commit()
            cur.close()
            conn.close()

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        # print({film_id}, " li film silindi")
        self.list_grades()

    def list_grades(self):

        for i in self.treeview.get_children():
            self.treeview.delete(i)

        filmlist = self.load_all_films()
        for film in filmlist:
            f: Film = film
            film_Id = f.__getattribute__("film_Id")
            year = f.__getattribute__("year")
            tr_title = f.__getattribute__("tr_title")
            en_title = f.__getattribute__("en_title")

            self.treeview.insert(parent="", index="end", iid=film_Id, values=(tr_title, en_title, year))
            # self.treeview.insert((parent="", index="end", iid=f[0], values=(f[1], f[2], f[3])))

    def Page_Back(self):
        self.win.destroy()
        w3 = Window3(self.lang)
        w3.EditMovie.focus_force()

    def create_widgets(self):
        self.delete_film_frame = tk.Frame(self.win)
        self.delete_film_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.treeview_frame = tk.Frame(self.delete_film_frame)
        self.treeview_frame.pack()
        self.Back_Page = tk.Button(self.delete_film_frame, text=self.i18n.bPrevious, command=self.Page_Back)
        self.Back_Page.pack()

        self.scroll_bar = ttk.Scrollbar(self.treeview_frame)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeview = ttk.Treeview(self.treeview_frame, yscrollcommand=self.scroll_bar.set)
        self.treeview.bind("<Double-1>")
        self.treeview.pack(fill=tk.BOTH)

        self.scroll_bar.configure(command=self.treeview.yview)

        # self.treeview["columns"] = ("film_ID", "tr_title", "en_title", "year")
        self.treeview["columns"] = ("tr_title", "en_title", "year")

        self.treeview.column("#0", width=0, stretch=tk.NO)
        # self.treeview.column("film_ID", anchor=tk.CENTER, width=50, stretch=tk.NO)
        self.treeview.column("tr_title", anchor=tk.W, width=270)
        self.treeview.column("en_title", anchor=tk.W, width=270)
        self.treeview.column("year", anchor=tk.CENTER, width=100)

        self.treeview.heading("#0", text="")
        # self.treeview.heading("film_ID", text="film_ID", anchor=tk.CENTER)
        self.treeview.heading("tr_title", text=self.i18n.trtitle, anchor=tk.W)
        self.treeview.heading("en_title", text=self.i18n.entitle, anchor=tk.W)
        self.treeview.heading("year", text=self.i18n.lblyear, anchor=tk.CENTER)

        self.treeview.bind("<Double-1>", self.on_double_click)

    def load_all_films(self):
        filmlist = []
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute("SELECT film_ID, tr_title, en_title, tr_desc, en_desc, image, imdb, year FROM Films")
            records = cur.fetchall()
            for r in records:
                film_Id = r[0]
                tr_title = r[1]
                en_title = r[2]
                tr_desc = r[3]
                en_desc = r[4]
                image = DatabaseMethods(self.lang).load_image_from_db(r[5])
                imdb = r[6]
                year = r[7]
                actors = DatabaseMethods(self.lang).load_actors_for_films(en_title, "en")
                director = DatabaseMethods(self.lang).load_director_name(en_title, "en")
                categories_en = DatabaseMethods(self.lang).load_categories_en_for_films(en_title, "en")
                categories_tr = DatabaseMethods(self.lang).load_categories_tr_for_films(en_title, "en")

                film = Film(film_Id, tr_title, en_title, tr_desc, en_desc, image, imdb, director, categories_tr,
                            categories_en, actors, year)
                filmlist.append(film)

            cur.close()
            conn.close()

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        return filmlist

    def load_categories_for_films(self, title, lang):
        sorgu = tk.StringVar()
        catlang = tk.StringVar()
        if lang == "tr":
            sorgu = "tr_title"
            catlang = "c_trName"
        elif lang == "en":
            sorgu = "en_title"
            catlang = "c_enName"

        cat_list = []
        try:

            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute(
                f"SELECT {catlang} FROM Categories WHERE c_ID IN "
                f"(SELECT c_ID FROM FilmCategory WHERE film_Id IN "
                f"(SELECT film_ID FROM Films WHERE {sorgu} = '{title}'))")

            records = cur.fetchall()
            for r in records:
                cat_list.append(r[0])

            cur.close()
            conn.close()

        except Exception as exc:
            print(str(exc))

        return cat_list


class Filter:
    def __init__(self, lang):
        self.win = tk.Tk()
        self.lang = lang
        self.i18n = I18N(self.lang)
        self.win.title(self.i18n.title)
        self.create_widgets()

    def reload_gui_text(self, lang):
        self.i18n = I18N(lang)
        self.win.title(self.i18n.title)
        self.btn_filter.configure(text=self.i18n.bFilter)
        self.btn_back.configure(text=self.i18n.bPrevious)

    def load_categories(self, lang):
        conn = DatabaseMethods(self.lang).get_database_connection()
        cur = conn.cursor()
        cur.execute("""SELECT * FROM Categories""")
        records = cur.fetchall()
        ctglist = []
        if lang == "tr":
            for r in records:
                ctglist.append(r[1])

        elif lang == "en":
            for r in records:
                ctglist.append(r[2])

        return ctglist

    def load_all_actors(self):
        all_actors = []
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute("SELECT actor_name FROM Actors")
            records = cur.fetchall()
            for r in records:
                all_actors.append(r[0])

            cur.close()
            conn.close()

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        return all_actors

    def control_checkboxes(self):
        categories = []
        for i in range(len(self.chvars)):

            if self.chvars[i].get() == 1:
                c: tk.Checkbutton = self.checkbuttons[i]
                categories.append(c.cget("text"))

        return categories

    def load_directors(self):
        directors = []
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute("SELECT d_name FROM Directors")
            data = cur.fetchall()
            for d in data:
                directors.append(d[0])
            conn.commit()
            cur.close()
            conn.close()

        except Exception as exc:
            msg.showerror(self.i18n.Error1, self.i18n.Error2 + str(exc))

        return directors

    def click_filter(self):
        director = self.director.get()
        actor = self.actor.get()
        ctg = self.control_checkboxes()

        if self.director.get() == self.i18n.cDirector:
            director = None
        if self.actor.get() == self.i18n.cActor:
            actor = None
        if len(ctg) == 0:
            ctg = None

        fm = FilterMovies(ctg, director, actor, self.lang)

    def click_back(self):
        self.win.destroy()
        w5 = Window5(self.lang)
        w5.GuestPage.focus_force()

    def create_widgets(self):
        ctglist = self.load_categories(self.lang)

        self.checkbuttons = []
        self.chvars = []

        self.ch1var = tk.IntVar()
        self.ch2var = tk.IntVar()
        self.ch3var = tk.IntVar()
        self.ch4var = tk.IntVar()
        self.ch5var = tk.IntVar()
        self.ch6var = tk.IntVar()
        self.ch7var = tk.IntVar()
        self.ch8var = tk.IntVar()
        self.ch9var = tk.IntVar()
        self.ch10var = tk.IntVar()
        self.ch11var = tk.IntVar()
        self.ch12var = tk.IntVar()

        self.chvars.append(self.ch1var)
        self.chvars.append(self.ch2var)
        self.chvars.append(self.ch3var)
        self.chvars.append(self.ch4var)
        self.chvars.append(self.ch5var)
        self.chvars.append(self.ch6var)
        self.chvars.append(self.ch7var)
        self.chvars.append(self.ch8var)
        self.chvars.append(self.ch9var)
        self.chvars.append(self.ch10var)
        self.chvars.append(self.ch11var)
        self.chvars.append(self.ch12var)

        self.ch1 = tk.Checkbutton(self.win, text=ctglist[0], variable=self.ch1var)
        self.ch2 = tk.Checkbutton(self.win, text=ctglist[1], variable=self.ch2var)
        self.ch3 = tk.Checkbutton(self.win, text=ctglist[2], variable=self.ch3var)
        self.ch4 = tk.Checkbutton(self.win, text=ctglist[3], variable=self.ch4var)
        self.ch5 = tk.Checkbutton(self.win, text=ctglist[4], variable=self.ch5var)
        self.ch6 = tk.Checkbutton(self.win, text=ctglist[5], variable=self.ch6var)
        self.ch7 = tk.Checkbutton(self.win, text=ctglist[6], variable=self.ch7var)
        self.ch8 = tk.Checkbutton(self.win, text=ctglist[7], variable=self.ch8var)
        self.ch9 = tk.Checkbutton(self.win, text=ctglist[8], variable=self.ch9var)
        self.ch10 = tk.Checkbutton(self.win, text=ctglist[9], variable=self.ch10var)
        self.ch11 = tk.Checkbutton(self.win, text=ctglist[10], variable=self.ch11var)
        self.ch12 = tk.Checkbutton(self.win, text=ctglist[11], variable=self.ch12var)

        self.checkbuttons.append(self.ch1)
        self.checkbuttons.append(self.ch2)
        self.checkbuttons.append(self.ch3)
        self.checkbuttons.append(self.ch4)
        self.checkbuttons.append(self.ch5)
        self.checkbuttons.append(self.ch6)
        self.checkbuttons.append(self.ch7)
        self.checkbuttons.append(self.ch8)
        self.checkbuttons.append(self.ch9)
        self.checkbuttons.append(self.ch10)
        self.checkbuttons.append(self.ch11)
        self.checkbuttons.append(self.ch12)

        self.ch1.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch2.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        self.ch3.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch4.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        self.ch5.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch6.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        self.ch7.grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch8.grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)
        self.ch9.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch10.grid(row=8, column=1, sticky=tk.W, padx=5, pady=5)
        self.ch11.grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
        self.ch12.grid(row=9, column=1, sticky=tk.W, padx=5, pady=5)

        self.director = tk.StringVar()
        self.director.set(self.i18n.cDirector)

        dirs = sorted(self.load_directors())
        directors = [self.i18n.cDirector] + dirs

        self.cb_directors = ttk.Combobox(self.win, font=("helvetica", 10), values=directors, width=20,
                                         textvariable=self.director, state='readonly')
        self.cb_directors.grid(row=10, column=0, padx=5, pady=5)
        self.win.option_add('*TCombobox*Listbox.font', ("helvetica", 10))

        self.actor = tk.StringVar()
        self.actor.set(self.i18n.cActor)
        actors = sorted(self.load_all_actors(), key=str.lower)
        actors = [self.i18n.cActor] + actors

        self.cb_actors = ttk.Combobox(self.win, font=("helvetica", 10), values=actors, width=20,
                                      textvariable=self.actor, state='readonly')
        self.cb_actors.grid(row=10, column=1, padx=5, pady=5)

        self.btn_filter = tk.Button(self.win, text=self.i18n.bFilter, font=("helvetica", 10), width=14,
                                    command=self.click_filter)
        self.btn_filter.grid(row=11, column=0, padx=5, pady=5)

        self.btn_back = tk.Button(self.win, text=self.i18n.bPrevious, font=("helvetica", 10), width=14,
                                  command=self.click_back)
        self.btn_back.grid(row=11, column=1, padx=5, pady=5)


class FilterMovies:

    def __init__(self, categories, director, actor, lang):
        self.categories = categories
        self.director = director
        self.actor = actor
        self.lang = lang
        self.i18n = I18N(self.lang)
        # self.win = tk.Tk()
        self.win = tk.Toplevel()
        self.win.title("")
        self.create_widgets()
        self.filter_db()

    def loadfilmIDs_for_an_category(self, ctgname):
        films = []
        sorgu = ""
        if self.lang == "tr":
            sorgu = "c_trName"
        elif self.lang == "en":
            sorgu = "c_enName"
        try:

            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()

            cur.execute("SELECT film_ID FROM FilmCategory f, Categories c WHERE c.c_ID = f.c_ID AND "
                        f"{sorgu} = '{ctgname}'")
            records = cur.fetchall()
            for r in records:
                films.append(r[0])
            cur.close()
            conn.close()

        except Exception as exc:
            print(exc)

        return films

    def loadfilmIds_for_an_actor(self, actorname):
        films = []
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute("SELECT film_ID from FilmActor WHERE actor_ID IN "
                        f"(SELECT actor_ID FROM Actors WHERE actor_name = '{actorname}')")
            records = cur.fetchall()
            for r in records:
                films.append(r[0])

            cur.close()
            conn.close()

        except Exception as exc:
            print(exc)

        return films

    def loadfilmIds_for_an_director(self, directorname):
        films = []
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute("SELECT film_ID from Films WHERE d_ID IN "
                        f"(SELECT d_ID FROM Directors WHERE d_name = '{directorname}')")
            records = cur.fetchall()
            for r in records:
                films.append(r[0])

            cur.close()
            conn.close()

        except Exception as exc:
            print(exc)

        return films

    def load_all_filmIDs(self):
        idlist = []
        try:
            conn = DatabaseMethods(self.lang).get_database_connection()
            cur = conn.cursor()
            cur.execute("SELECT film_ID FROM Films")
            records = cur.fetchall()
            cur.close()
            conn.close()

            for r in records:
                idlist.append(r[0])

        except Exception as exc:
            print(exc)

        return idlist

    def filter_db(self):
        filmIDs = []
        actorIDs = []
        directorIDs = []
        catIDs = []
        if self.actor is not None:
            actorIDs = self.loadfilmIds_for_an_actor(self.actor)

        if self.director is not None:
            directorIDs = self.loadfilmIds_for_an_director(self.director)

        if self.categories is not None:
            catIDs = self.loadfilmIDs_for_an_category(self.categories[0])
            for c in self.categories:
                catIDs = set(catIDs) & set(self.loadfilmIDs_for_an_category(c))

        if len(actorIDs) != 0:
            if len(directorIDs) != 0:
                if len(catIDs) != 0:
                    filmIDs = set(actorIDs) & set(directorIDs) & set(catIDs)
                else:
                    filmIDs = set(actorIDs) & set(directorIDs)
            else:
                if len(catIDs) != 0:
                    filmIDs = set(actorIDs) & set(catIDs)
                else:
                    filmIDs = actorIDs

        else:
            if len(directorIDs) != 0:
                if len(catIDs) != 0:
                    filmIDs = set(directorIDs) & set(catIDs)
                else:
                    filmIDs = directorIDs
            else:
                if len(catIDs) != 0:
                    filmIDs = catIDs
                else:
                    if self.categories is None:
                        filmIDs = self.load_all_filmIDs()

        self.load_films_into_treeview(filmIDs)

        for f in filmIDs:
            name = DatabaseMethods(self.lang).find_film_names_with_filmID(f)
            # print(name)

    def load_films_into_treeview(self, filmIDlist):
        for f in filmIDlist:
            # film: Film = self.loadfilm_with_filmID(f)
            film: Film = DatabaseMethods(self.lang).loadfilm_with_filmID(f)
            # print(film)
            # name = self.find_film_names_with_filmID(f)
            name = DatabaseMethods(self.lang).find_film_names_with_filmID(f)
            # print(name)
            director = film.__getattribute__("director")
            year = film.__getattribute__("year")

            self.treeview.insert(parent="", index="end", iid=f, values=(name, director, year))

    def on_double_click(self, event):
        selected_items = self.treeview.selection()
        values = self.treeview.item(selected_items)['values']
        film_name = values[0]
        f_id = DatabaseMethods(self.lang).find_filmId(values[0])
        film = DatabaseMethods(self.lang).loadfilm_with_filmID(f_id)

        sf = ShowFilms(film, self.lang)

    def create_widgets(self):
        self.delete_film_frame = tk.Frame(self.win)
        self.delete_film_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.treeview_frame = tk.Frame(self.delete_film_frame)
        self.treeview_frame.pack()

        self.scroll_bar = ttk.Scrollbar(self.treeview_frame)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeview = ttk.Treeview(self.treeview_frame, yscrollcommand=self.scroll_bar.set)
        self.treeview.bind("<Double-1>")
        self.treeview.pack(fill=tk.BOTH)

        self.scroll_bar.configure(command=self.treeview.yview)

        # self.treeview["columns"] = ("film_ID", "tr_title", "en_title", "year")
        self.treeview["columns"] = ("title", "director", "year")

        self.treeview.column("#0", width=0, stretch=tk.NO)
        # self.treeview.column("film_ID", anchor=tk.CENTER, width=50, stretch=tk.NO)
        self.treeview.column("title", anchor=tk.W, width=300)
        self.treeview.column("director", anchor=tk.W, width=200)
        self.treeview.column("year", anchor=tk.CENTER, width=100)

        self.treeview.heading("#0", text="")
        # self.treeview.heading("film_ID", text="film_ID", anchor=tk.CENTER)
        self.treeview.heading("title", text=self.i18n.mtitle, anchor=tk.W)
        self.treeview.heading("director", text=self.i18n.dNames, anchor=tk.W)
        self.treeview.heading("year", text=self.i18n.txtyear, anchor=tk.CENTER)

        self.treeview.bind("<Double-1>", self.on_double_click)


class SearchPage:
    def __init__(self, lang):
        self.win = tk.Tk()
        self.lang = lang
        self.i18n = I18N(self.lang)
        self.win.title(self.i18n.stitle)
        self.create_widgets()

    def reload_gui_text(self, lang):
        self.i18n = I18N(lang)
        self.win.title(self.i18n.stitle)
        self.buttonBack.configure(text=self.i18n.bPrevious)

    def on_press(self, key):
        # print(self.entry_search.get())
        # print("Key pressed")
        pass

    def films_into_frame(self, filmlist):
        self.lb.delete(0, tk.END)
        for f in filmlist:
            self.lb.insert(tk.END, f)

    def on_release(self, key):
        # print(self.entry_search.get())
        dm = DatabaseMethods(self.lang)
        filmlist = dm.load_all_film_names()
        # print(filmlist)
        new_list = []
        # string_Entry = self.entry_search.get()
        string_Entry = self.srch.get()
        string_Entry = string_Entry.capitalize()
        if len(string_Entry) != 0:
            for film in filmlist:
                f: str = film
                result = f.find(string_Entry)
                if result != -1:
                    # print("Bulundu", f)
                    new_list.append(f)

        self.films_into_frame(new_list)

        # print("Key released")

    def keyboardListener(self, event):
        self.key_listener = keyboard.Listener(on_press=self.on_press,
                                              on_release=self.on_release)
        self.key_listener.start()
        # self.key_listener.join()

    def on_double_click(self, event):
        name = self.lb.get(tk.ACTIVE)
        film_Id = DatabaseMethods(self.lang).find_filmId(name)
        film = DatabaseMethods(self.lang).loadfilm_with_filmID(film_Id)

        sf = ShowFilms(film, self.lang)

    def BackButton(self):
        self.win.destroy()
        w5 = Window5(self.lang)
        w5.GuestPage.focus_force()

    def create_widgets(self):
        self.srch = tk.StringVar()
        self.entry_search = ttk.Entry(self.win, width=20, font=("TimesNewRoman", 10), textvariable=self.srch)
        self.entry_search.grid(row=0, column=0, padx=5, pady=5)

        # self.entry_search.bind("<FocusIn>", self.keyboardListener)
        self.entry_search.bind("<KeyRelease>", self.on_release)

        self.lb = tk.Listbox(self.win, width=45, font=("TimesNewRoman", 10))
        self.lb.grid(row=1, column=0, padx=5, pady=5)

        self.buttonBack = ttk.Button(self.win, text=self.i18n.bPrevious, command=self.BackButton)
        self.buttonBack.grid(column=0, row=2, columnspan=1, padx=5, pady=5, sticky="WENS")

        self.lb.bind("<Double-1>", self.on_double_click)


class ShowFilms:
    def __init__(self, film, lang):
        self.win = tk.Toplevel()
        self.win.title("Show Films")
        self.lang = lang
        self.film: Film = film
        self.filmtitle = tk.StringVar()
        self.describ = tk.StringVar()
        self.year = tk.IntVar()
        self.director = tk.StringVar()
        self.imdb = tk.DoubleVar()
        self.update_lang(lang)
        self.load_filmdatas(lang)
        self.create_widgets()

    def load_filmdatas(self, lang):
        if lang == "tr":
            self.filmtitle.set(self.film.__getattribute__("tr_title"))
            self.describ.set(self.film.__getattribute__("tr_desc"))
            self.categories = self.film.__getattribute__("categories_tr")
        elif lang == "en":
            self.filmtitle.set(self.film.__getattribute__("en_title"))
            self.describ.set(self.film.__getattribute__("en_desc"))
            self.categories = self.film.__getattribute__("categories_en")

        self.actors = self.film.__getattribute__("actors")
        self.director.set(self.film.__getattribute__("director"))
        self.year.set(self.film.__getattribute__("year"))
        self.imdb.set(self.film.__getattribute__("imdb"))
        img_data = self.film.__getattribute__("image")
        file_image = BytesIO(img_data)
        img = Image.open(file_image)
        resized_pic = img.resize((200, 300), Image.ANTIALIAS)
        n_pic = ImageTk.PhotoImage(resized_pic)
        self.photo = n_pic

    def update_lang(self, lang):
        if lang == "tr":
            self.desc = "Konu : "
            self.stars = "Aktörler/Aktrisler : "
            self.directed_by = "Yönetmen : "
            self.ctg = "Kategoriler : "
            self.time = "Yıl: "

        elif lang == "en":
            self.desc = "Description : "
            self.stars = "Actors/Actresses : "
            self.directed_by = "Director : "
            self.ctg = "Categories : "
            self.time = "Year : "

    def insert_texts(self):
        self.scr.configure(state=tk.NORMAL)
        self.scr.insert(tk.INSERT, "\n" + self.desc + self.describ.get() + "\n\n")
        self.scr.insert(tk.INSERT, self.directed_by + self.director.get() + "\n\n")
        stractors = ""
        for i in range(len(self.actors)):
            if i == 0:
                stractors += self.actors[i]
            else:
                stractors += ", " + self.actors[i]

        self.scr.insert(tk.INSERT, self.stars + stractors + "\n\n")

        strcat = ""
        for i in range(len(self.categories)):
            if i == 0:
                strcat += self.categories[i]
            else:
                strcat += ", " + self.categories[i]

        self.scr.insert(tk.INSERT, self.ctg + strcat + "\n\n")

        self.scr.insert(tk.INSERT, self.time + str(self.year.get()) + "\n\n")
        self.scr.insert(tk.INSERT, "Imdb : " + str(self.imdb.get()))

        self.scr.configure(state=tk.DISABLED)

    def create_widgets(self):
        showMovie = tk.Frame(self.win, width=800, height=450)
        showMovie.grid(row=0, column=0, padx=10, pady=10)

        showPoster = tk.Frame(showMovie, width=380, height=450, bg="#BFBDBD")
        showPoster.grid(row=0, column=0, padx=10, pady=10)
        showDesc = tk.Frame(showMovie, width=380, height=450)
        showDesc.grid(row=0, column=1, padx=0, pady=0)

        # self.ornek()

        self.lbl_title = tk.Label(showPoster, text=self.filmtitle.get(), font=("Helvetica", 14))
        self.lbl_title.grid(row=0, column=0, padx=10, pady=10)

        global resized_pic
        image = Image.open('unknown.png')
        resized = image.resize((200, 300), Image.ANTIALIAS)
        resized_pic = ImageTk.PhotoImage(resized)

        # resized_pic = self.load_image_from_db(self.film.__getattribute__("image"))
        dm = DatabaseMethods(self.lang)
        resized_pic = dm.load_image_from_db(self.film.__getattribute__("image"))

        # self.label_image = tk.Label(showPoster, image=resized_pic)
        self.label_image = tk.Label(showPoster, image=resized_pic)
        self.label_image.grid(row=1, column=0, padx=20, pady=20)

        self.scr = scrolledtext.ScrolledText(showDesc, font=("Arial", 14), height=17, width=40, wrap=tk.WORD,
                                             state=tk.DISABLED)
        self.scr.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        # self.update_lang("tr")
        self.insert_texts()


class Film:
    def __init__(self, film_Id, tr_title, en_title, tr_desc, en_desc, image, imdb, director,
                 categories_tr, categories_en, actors, year):
        self.film_Id = film_Id
        self.tr_title = tr_title
        self.en_title = en_title
        self.tr_desc = tr_desc
        self.en_desc = en_desc
        self.image = image
        self.imdb = imdb
        self.director = director
        self.categories_tr = categories_tr
        self.categories_en = categories_en
        self.actors = actors
        self.year = year

    def __str__(self):
        return f"{self.tr_title} {self.imdb} {self.year} {self.actors} {self.director} {self.categories_en}"
        # return f"{self.film_Id} {self.tr_title} {self.en_title} {self.tr_desc} {self.en_desc}"


app = Window1("en")
app.MainPage.mainloop()
