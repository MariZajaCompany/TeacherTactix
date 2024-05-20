from Classes.ClassInSchool import ClassInSchool
class Group:
    def __init__(self, day):
        self.attendance = [0,0,0,0,0]
        self.subgroups = []
        self.teacher = ""
        self.room = ""

    def get_list_of_classes(self):
        return self.subgroups
    
    def get_attendance(self, hour):
        return self.attendance[hour]

    def new_add_children(self, day, object):
        for hour in range(5):
            self.attendance[hour] += object.get_attendance(day, hour)
        self.subgroups.append(object)