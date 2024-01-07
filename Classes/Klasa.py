import csv

class Klasa:
    def __init__(self, poziom_klasy, litera_klasy):
        self.nazwa_klasy = str(poziom_klasy) + litera_klasy
        self.poziom_klasy = poziom_klasy
        self.litera_klasy = litera_klasy
        self.rozklad_dzieci = [[0] * 5 for _ in range(5)]

    def get_nazwa_klasy(self):
        return self.nazwa_klasy

    def wyswietl_rozklad_dzieci(self):
        for row in self.rozklad_dzieci:
            print(row)

    def ustaw_wartosc(self, wiersz, kolumna, wartosc):
        if 0 <= wiersz < 5 and 0 <= kolumna < 5:
            self.rozklad_dzieci[wiersz][kolumna] = wartosc
        else:
            print("Błędne współrzędne")

    def wczytaj_z_csv(self, sciezka_csv): #nazwa pliku może być ściśle zależna od nazwy danej klasy np rozklad_1A.csv,
        # oszczędzi to klikania, ale będzie trochę mniej intuicyjne
        try:
            with open(sciezka_csv, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for i, row in enumerate(reader):
                    for j, value in enumerate(row):
                        self.ustaw_wartosc(i, j, int(value))
        except FileNotFoundError:
            print(f"Plik CSV '{sciezka_csv}' nie został znaleziony.")
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania pliku CSV: {e}")