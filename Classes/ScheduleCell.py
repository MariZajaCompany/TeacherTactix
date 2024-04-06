from Classes.ClassInSchool import ClassInSchool

class ScheduleCell:
    def __init__(self, day, hour, classes, attendance):
        self.day = day
        self.hour = hour
        self.classes = classes
        self.attendance = attendance

    def display_info(self):
        for c in self.classes:
            print(f"{c.get_class_name()}", end=' ')
        print(f"({self.attendance})", end='')