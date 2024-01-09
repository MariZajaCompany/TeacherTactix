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

def klucz_sortowania(obiekt, dzien, godzina):
    if isinstance(obiekt, Grupa):
        return obiekt.get_liczba_dzieci()
    elif isinstance(obiekt, Klasa):
        return obiekt.get_obecnosc(dzien, godzina)


if __name__ == '__main__':
    
    lista_klas = utworz_klasy_z_folderu('Data')
    liczba_klas = len(lista_klas)

    for klasa in lista_klas:
        print(f"\nKlasa: {klasa.nazwa_klasy}")
        klasa.wyswietl_rozklad_dzieci()

    # utworzenie harmonogramu
    
    for dzien in range(1):
        for godzina in range(5):
            print("Dzien: ", dzien, "Godzina: ", godzina)
            lista_grup = [[], [], [], []]
            lista_obecnych = [[], [], [], []]
            for klasa in lista_klas:
                if klasa.get_obecnosc(dzien, godzina) > 0:
                    lista_obecnych[klasa.poziom_klasy].append(klasa)

            for poziom in range(4):
                
                lista_obecnych[poziom] = sorted(lista_obecnych[poziom], key=lambda klasa: klasa.get_obecnosc(dzien, godzina), reverse=True)
                
                if poziom > 0: #sprawdzanie czy mlodsza grupa może "awansować" do poziomu wyżej
                    tmp_obecne_klasy = list(lista_obecnych[poziom])
                    for mlodsza_grupa in lista_grup[poziom - 1]:
                        for klasa in tmp_obecne_klasy:
                            if mlodsza_grupa.get_liczba_dzieci() < 25 - klasa.get_obecnosc(dzien, godzina):
                                tmp_obecne_klasy.remove(klasa)
                                lista_obecnych[poziom].append(mlodsza_grupa)
                    lista_obecnych[poziom] = sorted(lista_obecnych[poziom], key=lambda obiekt: klucz_sortowania(obiekt, dzien, godzina), reverse=True)
                

                    # Wyświetlanie listy_obecnych
                    """
                    if lista_obecnych[poziom]:
                        print(f"Poziom {poziom}:")
                        for obiekty in enumerate(lista_obecnych[poziom]):
                                for obiekt in obiekty:
                                    if isinstance(obiekt, Grupa):
                                        print(f"  Grupa - Liczba dzieci: {obiekt.get_liczba_dzieci()}")
                                    elif isinstance(obiekt, Klasa):
                                        print(f"  Klasa - Obecność: {obiekt.get_obecnosc(dzien, godzina)}")
                    """


                while lista_obecnych[poziom]: # dzialanie tej petli jest specjalne
                    for klasa in lista_obecnych[poziom]:
                        grupa = Grupa(dzien, godzina)
                        lista_obecnych[poziom].remove(klasa)
                        grupa.dodaj_dzieci(klasa)
                        for inna_klasa in lista_obecnych[poziom]:
                            if grupa.dodaj_dzieci(inna_klasa):
                                lista_obecnych[poziom].remove(inna_klasa)
                        lista_grup[poziom].append(grupa)
                
                if lista_grup[poziom]:
                    print("Klasy: ", poziom)
                    for grupa in lista_grup[poziom]:
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
