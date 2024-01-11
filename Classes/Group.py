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
    
    def update_group(self):
        self.hour += 1
        self.number_of_children = 0
        school_classes = self.list_of_classes
        for school_class in school_classes:
            self.number_of_children += school_class.get_attendance(self.day, self.hour)
            if school_class.get_attendance(self.day, self.hour) == 0:
                self.list_of_classes.remove(school_class)
                

    def get_younger_grade(self):
        min_grade = self.list_of_classes[0].class_grade

        # Iteruj po pozostałych klasach i aktualizuj min_grade, jeśli znajdziesz niższy poziom klasy
        for school_class in self.list_of_classes[1:]:
            if school_class.class_grade < min_grade:
                min_grade = school_class.class_grade

        return min_grade
    
    def get_number_of_children(self):
        return self.number_of_children

    def add_children(self, object):
        if isinstance(object, Group):
            if self.number_of_children + object.get_number_of_children() <= 25:
                self.list_of_classes += object.get_list_of_classes()
                self.number_of_children += object.get_number_of_children()
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
            
    def display_group(self):
        #print(f"Day: {self.day}")
        #print(f"Hour: {self.hour}")
        print(f"\tNumber of Children: {self.number_of_children}")
        print(f"\tTeacher: {self.teacher}")
        print(f"\tRoom: {self.room}")
        class_names = [f"{school_class.get_class_name()} ({school_class.get_attendance(self.day, self.hour)})" for school_class in self.get_list_of_classes()]
        # Join class names with ' + ' and print
        print("\tClasses: " + " + ".join(class_names))
        print("\n")