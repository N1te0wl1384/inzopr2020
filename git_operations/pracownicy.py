class Pracownik:
    def __init__(self, imie, pensja):
        self.imie = imie
        self.pensja = pensja

    def obliczPensje(self):
        b = self.pensja
        c = float('%.2f'% (round(b*0.0976,2) + round(b*0.015,2) + round(b*0.0245,2)))
        d = b - c
        e = float('%.2f'% round(d*0.09, 2))
        f = float('%.2f'%round(d*0.0775, 2))
        g = 111.25
        h = float('%.2f'%round(b - g - c))
        i = float('%.2f'%(round(h*0.18,2) -46.33))
        j = round(i - f)
        k = b - c - e - j
        return k

    def skladkiPracodawcy(self):
        b = self.pensja
        c = float('%.2f'%(round(b*0.0976,2) + round(b*0.065,2) + round(b*0.0245,2) + round(b*0.0193,2) + round(b*0.001,2)))
        return c

liczba_pracownikow = int(input())
pracownicy = [];
for i in range(liczba_pracownikow):
    pracownik = input()
    dane=[]
    for dana in pracownik.split():
        dane.append(dana)
    pracownicy.append(dane)

lacznie = 0
for i in pracownicy:
    pracownik_instancja = Pracownik(i[0], float(i[1]))
    skladki_pracodawcy = pracownik_instancja.skladkiPracodawcy()
    pensja = pracownik_instancja.pensja
    laczny_koszt = skladki_pracodawcy + pensja
    print(pracownik_instancja.imie, '%.2f' % pracownik_instancja.obliczPensje(), '%.2f' % skladki_pracodawcy, '%.2f' % laczny_koszt)
    lacznie = lacznie + laczny_koszt
print('%.2f' % lacznie)
