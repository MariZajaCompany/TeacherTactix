import csv

class Teacher:
    def __init__(self, nameAndSurname, id):
        self.id = id
        self.nameAndSurname = nameAndSurname
        self.availability = [[False] * 5 for _ in range(5)]

    def print_availability(self):
        for row in self.availability:
            print(row)

    def set_value_in_availability(self, row, column, value):
        if 0 <= row < 5 and 0 <= column < 5:
            self.availability[row][column] = value
        else:
            print("Wrong coordinates")

    def read_from_csv(self, path_csv):
        try:
            with open(path_csv, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for i, row in enumerate(reader):
                    for j, value in enumerate(row):
                        self.set_value_in_availability(i, j, bool(int(value)))
        except FileNotFoundError:
            print(f"CSV file '{path_csv}' was not found.")
        except Exception as e:
            print(f"Error occured while read the file: {e}")