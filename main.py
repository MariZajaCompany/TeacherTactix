from Classes.Opiekun import Opiekun
from Classes.Klasa import Klasa
import os
import re

def utworz_klasy_z_folderu(folder_danych):
    prefix_pliku = 'rozklad_'
    lista_plikow_csv = [plik for plik in os.listdir(folder_danych) if plik.startswith(prefix_pliku) and plik.endswith('.csv')]
    utworzone_klasy = []

    for nazwa_pliku in lista_plikow_csv:
        wynik = re.match(r'rozklad_(\d+)(\w)\.csv', nazwa_pliku)
        if wynik:
            cyfra, litera = wynik.groups()
            obiekt_klasy = Klasa(int(cyfra), litera)
            utworzone_klasy.append(obiekt_klasy)
            print(f"Nazwa pliku: {nazwa_pliku}, Klasa: {obiekt_klasy.poziom_klasy}, {obiekt_klasy.litera_klasy}")
            sciezka_do_csv = os.path.join("Data", nazwa_pliku)
            obiekt_klasy.wczytaj_z_csv(sciezka_do_csv)
        else:
            print(f"Niewłaściwy format nazwy pliku: {nazwa_pliku}")

    return utworzone_klasy

if __name__ == '__main__':
    
    lista_klas = utworz_klasy_z_folderu('Data')
    
    for klasa in lista_klas:
        print(f"\nKlasa: {klasa.nazwa_klasy}")
        klasa.wyswietl_rozklad_dzieci()

    # Przykład opiekuna:
    opiekun = Opiekun("Jan Kowalski", 1)
    print("\nJan Kowalski:")
    opiekun.wczytaj_z_csv("Data\\jan_kowalski.csv")
    opiekun.wyswietl_dostepnosc()

