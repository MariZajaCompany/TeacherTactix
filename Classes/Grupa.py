from Classes.Klasa import Klasa
class Grupa:
    def __init__(self, dzien, godzina):
        self.lista_klas = []
        self.liczba_dzieci = 0
        self.dzien = dzien
        self.godzina = godzina
        self.opiekun = ""
        self.sala = ""

    def get_lista_klas(self):
        return self.lista_klas

    def get_liczba_dzieci(self):
        return self.liczba_dzieci

    def dodaj_dzieci(self, obiekt):
        if isinstance(obiekt, Grupa):
            if self.liczba_dzieci + obiekt.get_liczba_dzieci() <= 25:
                self.lista_klas += obiekt.get_lista_klas()
                self.liczba_dzieci += obiekt.get_liczba_dzieci()
                #print(klasa.get_nazwa_klasy())
                return True #klasa moze zostac usunieta z listy klas do podzialu
            else:
                return False  
        elif isinstance(obiekt, Klasa):
            if self.liczba_dzieci + obiekt.get_obecnosc(self.dzien,self.godzina) <= 25:
                self.lista_klas.append(obiekt)
                self.liczba_dzieci += obiekt.get_obecnosc(self.dzien,self.godzina)
                #print(klasa.get_nazwa_klasy())
                return True #klasa moze zostac usunieta z listy klas do podzialu
            else:
                return False  
            