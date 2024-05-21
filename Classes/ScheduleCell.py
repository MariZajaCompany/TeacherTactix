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
    
    def get_info_with_sizes(self):
        info = ""
        for c in self.classes:
            if c.get_attendance(self.day, self.hour) != 0:
                info += str(c.get_class_name()) + " "
        info += "(" + str(self.attendance) + ")"
        return info
    
    def get_info(self):
        info = ""
        for c in self.classes:
            if c.get_attendance(self.day, self.hour) != 0:
                info += str(c.get_class_name()) + " "
        info = info[:-1]
        return info