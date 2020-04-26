import string
import gui_lib.db_operations as db

class Biblioteka:
    def __init__(self, liczba_wyp):
        self._liczba_wyp = liczba_wyp
        self._lista_czytelnikow = []
        self._lista_ksiazek = []
        self._lista_egzemplarzy = dict()


    def wypozycz(self, nazwisko: str, tytul: str):
        lista_niewypozyczonych = self.dostepne_egz(tytul)
        wypozyczajacy = None
        for czytelnik in self._lista_czytelnikow:
            if czytelnik.nazwisko() == nazwisko:
                wypozyczajacy = czytelnik
        if wypozyczajacy == None:
            wypozyczajacy = Czytelnik(nazwisko)
            self._lista_czytelnikow.append(wypozyczajacy)
        if len(lista_niewypozyczonych) == 0:
            return False
        else:
            for egzemplarz in lista_niewypozyczonych:
                if egzemplarz.wypozyczony == False:
                    egzemplarz_do_wypozyczenia = egzemplarz
                    break
            return wypozyczajacy.wypozycz(egzemplarz_do_wypozyczenia, self._liczba_wyp)

    def oddaj(self, nazwisko: str, tytul: str):
        oddajacy = None
        egzemplarz_do_oddania = None
        for czytelnik in self._lista_czytelnikow:
            if czytelnik.nazwisko() == nazwisko:
                oddajacy = czytelnik
        if oddajacy is None:
            return False
        for egzemplarz in oddajacy.lista_ksiazek():
            if egzemplarz.get_ksiazka().tytul() == tytul:
                egzemplarz_do_oddania = egzemplarz
        if egzemplarz_do_oddania is None:
            return False
        zwrocona_ksiazka = self._lista_egzemplarzy[egzemplarz_do_oddania.get_ksiazka()]
        for egzemplarz in zwrocona_ksiazka:
            if egzemplarz == egzemplarz_do_oddania:
                egzemplarz.wypozyczony = False
                return oddajacy.oddaj(egzemplarz_do_oddania)

    def dodaj_egz_ksiazki(self, tytul: str, autor: str, rok_wydania: int, pic):
        k = None
        b_list = db.get_books()
        for book in b_list:
            if tytul == book[1] and autor == book[2]:
                k = book
        if k == None:
            db.add_book(tytul, autor, pic)
        key = db.get_book_key(tytul, autor)
        db.add_specimens(key, rok_wydania, "false")
        print("DODANO")
        return True


class Ksiazka:
    def __init__(self, tytul: str, autor: str, pic:str):
        self._tytul = tytul
        self._autor = autor
        self._pic

    def tytul(self):
        return self._tytul

    def autor(self):
        return self._autor

    def pic(self):
        return self._pic


class Egzemplarz:
    def __init__(self, ksiazka: Ksiazka, rok_wydania: int, wypozyczony: bool):
        self._ksiazka = ksiazka
        self._rok_wydania = rok_wydania
        self.wypozyczony = wypozyczony

    def get_ksiazka(self):
        return self._ksiazka

    def rok_wydania(self):
        return self.rok_wydania()


class Czytelnik:
    def __init__(self, imie: str ,nazwisko: str, adres: str, miasto: str, login: str, haslo: str):
        self._imie = imie
        self._nazwisko = nazwisko
        self._adres = adres
        self._miasto = miasto
        self._login = login
        self._haslo = haslo


    def get_login(self):
        return self._login

    def nazwisko(self):
        return self._nazwisko

    def imie(self):
        return self._imie

    def wypozycz(self, egzemplarz: Egzemplarz, ilosc: int):
        for egzemplarz_czytelnika in self._lista_ksiazek:
            if egzemplarz_czytelnika.get_ksiazka().tytul() == egzemplarz.get_ksiazka().tytul():
                return False
        if len(self._lista_ksiazek) < ilosc:
            self._lista_ksiazek.append(egzemplarz)
            egzemplarz.wypozyczony = True
            print("wypozyczono")
            return True

        else:
            return False

    def oddaj(self, egzemplarz: Egzemplarz):
        for egzemplarz_wyp in self._lista_ksiazek:
            if egzemplarz_wyp.get_ksiazka().tytul() == egzemplarz.get_ksiazka().tytul():
                self._lista_ksiazek.remove(egzemplarz_wyp)
                return True
        return False
