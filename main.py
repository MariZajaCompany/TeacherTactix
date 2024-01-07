from Classes.Opiekun import Opiekun
from Classes.Klasa import Klasa

if __name__ == '__main__':
    # Przykład użycia:
    opiekun = Opiekun("Jan Kowalski", 1)
    print("Jan Kowalski:")
    opiekun.wyswietl_dostepnosc()

    # Wczytanie danych z pliku CSV
    opiekun.wczytaj_z_csv("Data\\jan_kowalski.csv")
    print("\nTablica po wczytaniu z pliku CSV:")
    opiekun.wyswietl_dostepnosc()

    # Przykład użycia:
    klasa = Klasa(0, 'A')
    print("\n" + klasa.get_nazwa_klasy() + ":")
    klasa.wyswietl_rozklad_dzieci()

    # Wczytanie danych z pliku CSV
    klasa.wczytaj_z_csv("Data\\rozklad_0_A.csv")
    print("\nTablica po wczytaniu z pliku CSV:")
    klasa.wyswietl_rozklad_dzieci()
