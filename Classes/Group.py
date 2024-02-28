from Classes.ClassInSchool import ClassInSchool
#from Classes.Subgroup import Subgroup
class Group:
    def __init__(self, day, hour):
        self.grade_attendance = [0,0,0,0]
        self.subgroups = [[],[],[],[]]
        self.day = day
        self.hour = hour
        self.teacher = ""
        self.room = ""

    def get_list_of_classes(self):
        list_of_classes = []
        for i in range(4):
            list_of_classes += self.subgroups[i]
        return list_of_classes
    
    def get_subgroup(self, grade):
        return self.subgroups[grade]
    
    def get_subgroups(self):
        return self.subgroups
    
    def get_attendance(self, *arguments): # any number of arguments
        return sum(self.grade_attendance)
    
    def get_grade_attendance(self, grade): # any number of arguments
        return self.grade_attendance[grade]
    
    def set_time(self, day, hour): #update of a group size and removing absent classes
        self.day = day
        self.hour = hour
        self.attendance = 0
        for c in self.get_list_of_classes():
            class_attendance = c.get_attendance(day, hour)
            self.grade_attendance[c.get_grade()] += class_attendance
            if class_attendance == 0:
                self.remove_class(c)
    
    def remove_class(self, c):
        grade = c.get_grade()
        for c in self.subgroups[grade]:
            if c.get_class_name() == c.get_class_name():
                self.subgroups[grade].remove(c)
                break
        self.grade_attendance[grade] -= c.get_attendance(self.day, self.hour)

    def add_children(self, object):
        youngest_grade = -1
        for i in range(4):
            if self.grade_attendance[i] != 0:
                youngest_grade = i # finding lowest grade in the group
                break
            
        if isinstance(object, Group):
            if self.get_attendance() + object.get_attendance() <= 25:
                for g in range(4):
                    self.subgroups[g] += object.get_subgroup(g)
                self.grade_attendance[g] += object.get_attendance()
                return True # group added successfully
            else:
                

                return False  
        elif isinstance(object, ClassInSchool):
            if self.get_attendance() + object.get_attendance(self.day,self.hour) <= 25: # adding class
                youngest_grade = object.get_grade()
                self.subgroups[youngest_grade].append(object)
                self.grade_attendance[youngest_grade] += object.get_attendance(self.day,self.hour)
                return True # class added successfully
            
            elif self.get_grade_attendance(youngest_grade) + object.get_attendance(self.day,self.hour) <= 25 and youngest_grade == object.get_grade(): # exchanging class for a better fitting one
                self.subgroups[youngest_grade].append(object)
                self.grade_attendance[youngest_grade] += object.get_attendance(self.day,self.hour)
                
                g = 3
                while youngest_grade < g and self.get_attendance() + c.get_attendance(self.day,self.hour) > 25:
                    tmp_subgroups = self.subgroups[g]
                    for c in tmp_subgroups:
                        self.subgroups[g].remove(c)
                        self.grade_attendance[g] -= c.get_attendance(self.day,self.hour)
                        # if self.get_attendance() + c.get_attendance(self.day,self.hour) > 25: # usuwanie tylko tyle klas ile potrzeba, a 
                        #     self.subgroups[g].remove(c)
                        #     self.grade_attendance[g] -= c.get_attendance(self.day,self.hour)
                        # else:
                        #     break
                    g -= 1
                return True # class exchanged successfully
            else:
                return False
            
    def display_group(self):
        #print(f"Day: {self.day}")
        #print(f"Hour: {self.hour}")
        print(f"Number of Children: {self.get_attendance()}")
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