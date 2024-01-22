from Classes.ClassInSchool import ClassInSchool
class Group:
    def __init__(self, day, hour):
        self.list_of_classes = []
        self.number_of_children = 0
        self.day = day
        self.hour = hour
        self.teacher = ""
        self.room = ""

    def get_list_of_classes(self):
        return self.list_of_classes
        
    def get_number_of_children(self):
        return self.number_of_children

    def add_children(self, object):
        if isinstance(object, Group):
            if self.number_of_children + object.get_attendance(self.day,self.hour) <= 25:
                self.list_of_classes += object.get_list_of_classes()
                self.number_of_children += object.get_attendance(self.day,self.hour)
                return True # group added successfully
            else:
                return False  
        elif isinstance(object, ClassInSchool):
            if self.number_of_children + object.get_attendance(self.day,self.hour) <= 25:
                self.list_of_classes.append(object)
                self.number_of_children += object.get_attendance(self.day,self.hour)
                return True # class added successfully
            else:
                return False
            
    def get_attendance(self, day, hour):
        attendance = 0
        for c in self.list_of_classes:
            attendance += c.get_attendance(day, hour)
        return attendance
            
    def display_group(self):
        #print(f"Day: {self.day}")
        #print(f"Hour: {self.hour}")
        print(f"Number of Children: {self.number_of_children}")
        print(f"Teacher: {self.teacher}")
        print(f"Room: {self.room}")
        print("Classes:")
        for school_class in self.get_list_of_classes():
            print(f"{school_class.get_class_name()} ({school_class.get_attendance(self.day, self.hour)})", end=" + " if self.get_list_of_classes().index(school_class) < len(self.get_list_of_classes()) - 1 else "",)
        print("\n")

    def display_group2(self):
        for school_class in self.get_list_of_classes():
            attendance = school_class.get_attendance(self.day, self.hour)
            if attendance != 0:
                print(f"{school_class.get_class_name()} ({school_class.get_attendance(self.day, self.hour)})", end=" + ")
        print(",", end="")