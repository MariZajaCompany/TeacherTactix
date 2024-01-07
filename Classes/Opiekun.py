import csv

class Opiekun:
    def __init__(self, imie_nazwisko, id):
        self.id = id
        self.imie_nazwisko = imie_nazwisko
        self.dostepnosc = [[False] * 5 for _ in range(5)]

    def wyswietl_dostepnosc(self):
        for row in self.dostepnosc:
            print(row)

    def ustaw_wartosc(self, wiersz, kolumna, wartosc):
        if 0 <= wiersz < 5 and 0 <= kolumna < 5:
            self.dostepnosc[wiersz][kolumna] = wartosc
        else:
            print("Błędne współrzędne")

    def wczytaj_z_csv(self, sciezka_csv):
        try:
            with open(sciezka_csv, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for i, row in enumerate(reader):
                    for j, value in enumerate(row):
                        self.ustaw_wartosc(i, j, bool(int(value)))
        except FileNotFoundError:
            print(f"Plik CSV '{sciezka_csv}' nie został znaleziony.")
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania pliku CSV: {e}")