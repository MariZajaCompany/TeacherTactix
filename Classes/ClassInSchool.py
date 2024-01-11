import csv

class ClassInSchool:
    def __init__(self, class_grade, class_letter):
        self.class_name = str(class_grade) + class_letter
        self.class_grade = class_grade
        self.class_letter = class_letter
        self.children_layout = [[0] * 5 for _ in range(5)]
        # 5 x 5 table with groups?

    def get_class_name(self):
        return self.class_name
    
    def get_schedule(self):
        return self.schedule
    
    def get_attendance(self, day, hour):
        return self.children_layout[hour][day]
    
    def get_children_layout(self):
        return self.children_layout

    def print_children_layout(self):
        for row in self.children_layout:
            print(row)

    def set_value_in_layout(self, hour, day, value):
        if 0 <= hour < 5 and 0 <= day < 5:
            self.children_layout[hour][day] = value
        else:
            print("Wrong coordinates")

    def read_from_csv(self, path_csv): 
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