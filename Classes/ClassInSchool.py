import csv
from Classes.Schedule import Schedule

class ClassInSchool:
    def __init__(self, classGrade, classLetter):
        self.className = str(classGrade) + classLetter
        self.classGrade = classGrade
        self.classLetter = classLetter
        self.childrenLayout = [[0] * 5 for _ in range(5)]
        self.schedule = Schedule()

    def get_class_name(self):
        return self.className
    
    def get_schedule(self):
        return self.schedule
    
    def get_attendance(self, day, hour):
        return self.childrenLayout[hour][day]
    
    def get_children_layout(self):
        return self.childrenLayout

    def print_children_layout(self):
        for row in self.childrenLayout:
            print(row)

    def set_value_in_layout(self, hour, day, value):
        if 0 <= hour < 5 and 0 <= day < 5:
            self.childrenLayout[hour][day] = value
        else:
            print("Wrong coordinates")

    def read_from_csv(self, path_csv): #nazwa pliku może być ściśle zależna od nazwy danej klasy np rozklad_1A.csv,
        # oszczędzi to klikania, ale będzie trochę mniej intuicyjne
        try:
            with open(path_csv, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for i, row in enumerate(reader):
                    for j, value in enumerate(row):
                        self.set_value_in_layout(i, j, int(value))
        except FileNotFoundError:
            print(f"CSV file '{path_csv}' was not found.")
        except Exception as e:
            print(f"Error occured while read the file: {e}")