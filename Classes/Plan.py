
class KomorkaPlanu:
    def __init__(self, opiekun=None, sala=None):
        self.opiekun = opiekun
        self.sala = sala

class Plan:
    def __init__(self):
        self.tablica_planu = [[KomorkaPlanu() for _ in range(5)] for _ in range(5)]

    def wyswietl_plan(self):
        for wiersz in self.tablica_planu:
            for komorka in wiersz:
                if komorka.opiekun is not None:
                    print(f"Opiekun: {komorka.opiekun}, Sala: {komorka.sala}")
                else:
                    print("Pusta komórka")
            print()