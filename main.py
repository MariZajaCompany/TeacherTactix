from Classes.Opiekun import Opiekun
from Classes.Klasa import Klasa
from Classes.Grupa import Grupa
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
            #print(f"Nazwa pliku: {nazwa_pliku}, Klasa: {obiekt_klasy.poziom_klasy}, {obiekt_klasy.litera_klasy}")
            sciezka_do_csv = os.path.join("Data", nazwa_pliku)
            obiekt_klasy.wczytaj_z_csv(sciezka_do_csv)
        else:
            print(f"Niewłaściwy format nazwy pliku: {nazwa_pliku}")

    return utworzone_klasy

if __name__ == '__main__':
    
    lista_klas = utworz_klasy_z_folderu('Data')
    liczba_klas = len(lista_klas)

    for klasa in lista_klas:
        print(f"\nKlasa: {klasa.nazwa_klasy}")
        klasa.wyswietl_rozklad_dzieci()

    # utworzenie harmonogramu
    
    for dzien in range(1):
        for godzina in range(5):
            lista_obecnych = []
            lista_grup = []
            for klasa in lista_klas:
                if klasa.get_obecnosc(dzien, godzina) > 0:
                    lista_obecnych.append(klasa)
            
            lista_obecnych = sorted(lista_obecnych, key=lambda klasa: klasa.get_obecnosc(dzien, godzina), reverse=True)

            while lista_obecnych: # dzialanie tej petli jest specjalne
                for klasa in lista_obecnych:
                    grupa = Grupa(dzien, godzina)
                    lista_obecnych.remove(klasa)
                    
                    grupa.dodaj_klase(klasa)
                    for inna_klasa in lista_obecnych:
                        if grupa.dodaj_klase(inna_klasa):
                            lista_obecnych.remove(inna_klasa)
                    lista_grup.append(grupa)
            
            if lista_grup:
                print("Dzien: ", dzien, "Godzina: ", godzina)
                for grupa in lista_grup:
                    for klasa in grupa.get_lista_klas():
                        print(f"{klasa.get_nazwa_klasy()} ({klasa.get_obecnosc(dzien, godzina)})", end=" + " if grupa.get_lista_klas().index(klasa) < len(grupa.get_lista_klas()) - 1 else "",)
                    print()  # Dodaj nową linię po wyświetleniu wszystkich klas w grupie
            



            
            

    """
    # Przykład opiekuna:
    opiekun = Opiekun("Jan Kowalski", 1)
    print("\nJan Kowalski:")
    opiekun.wczytaj_z_csv("Data\\jan_kowalski.csv")
    opiekun.wyswietl_dostepnosc()
    """
