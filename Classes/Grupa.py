class Grupa:
    def __init__(self, dzien, godzina):
        self.lista_klas = []
        self.liczba_dzieci = 0
        self.dzien = dzien
        self.godzina = godzina

    def get_lista_klas(self):
        return self.lista_klas

    def dodaj_klase(self, klasa):
        if self.liczba_dzieci + klasa.get_obecnosc(self.dzien,self.godzina) <= 25:
            self.lista_klas.append(klasa)
            self.liczba_dzieci += klasa.get_obecnosc(self.dzien,self.godzina)
            #print(klasa.get_nazwa_klasy())
            return True #klasa moze zostac usunieta z listy klas do podzialu
        else:
            return False