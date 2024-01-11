import csv

class Teacher:
    def __init__(self, name_surname, id):
        self.id = id
        self.name_surname = name_surname
        self.availability = [[False] * 5 for _ in range(5)]

    def print_availability(self):
        for hour in self.availability:
            print(hour)

    def set_value_in_availability(self, hour, day, value):
        if 0 <= hour < 5 and 0 <= day < 5:
            self.availability[hour][day] = value
        else:
            print("Wrong coordinates")

    def read_from_csv(self, path_csv):
        try:
            with open(path_csv, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for i, hour in enumerate(reader):
                    for j, value in enumerate(hour):
                        self.set_value_in_availability(i, j, bool(int(value)))
        except FileNotFoundError:
            print(f"CSV file '{path_csv}' was not found.")
        except Exception as e:
            print(f"Error occured while read the file: {e}")