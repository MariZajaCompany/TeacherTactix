from Classes.ClassInSchool import ClassInSchool
class Group:
    def __init__(self, day, hour, subgroups = [[],[],[],[]]):
        self.grade_attendance = [0,0,0,0]
        self.subgroups = [[],[],[],[]]
        for grade in range(4):
            for school_class in subgroups[grade]:
                class_attendance = school_class.get_attendance(day, hour)
                self.grade_attendance[grade] += class_attendance
                if class_attendance > 0:
                    self.subgroups[grade].append(school_class)
        self.day = day
        self.hour = hour

    def get_list_of_classes(self):
        list_of_classes = []
        for i in range(4):
            list_of_classes += self.subgroups[i]
        return list_of_classes
    
    def set_time(self, day, hour): #update of a group size and removing absent classes
        self.day = day
        self.hour = hour
        self.grade_attendance = [0] * 4
        for grade in range(4):
            self.subgroups[grade] = [c for c in self.subgroups[grade] if c.get_attendance(day, hour) > 0]
            self.grade_attendance[grade] = sum(c.get_attendance(day, hour) for c in self.subgroups[grade])

    def get_subgroup(self, grade):
        return self.subgroups[grade]
    
    def get_subgroups(self):
        return self.subgroups
    
    def get_attendance(self, *arguments): # any number of arguments
        return sum(self.grade_attendance)
    
    def get_grade_attendance(self, grade): # any number of arguments
        return self.grade_attendance[grade]
    
    def remove_class(self, c):
        grade = c.get_grade()
        self.subgroups[grade] = [sc for sc in self.subgroups[grade] if sc.get_class_name() != c.get_class_name()]
        self.grade_attendance[grade] -= c.get_attendance(self.day, self.hour)

    def get_youngest_grade(self):
        for i in range(4):
            if self.grade_attendance[i] != 0:
                return i  # finding lowest grade in the group
        return -1

    def add_children(self, obj):
        youngest_grade = self.get_youngest_grade()  # finding lowest grade in the group
        if isinstance(obj, Group):
            if self.get_attendance() + obj.get_attendance() <= 25:  # merging groups together
                for g in range(4):
                    self.subgroups[g] += obj.get_subgroup(g)
                    self.grade_attendance[g] += obj.get_grade_attendance(g)
                return True  # group added successfully
            else:
                if obj.get_grade_attendance(youngest_grade) != 0 and self.get_grade_attendance(youngest_grade) + obj.get_grade_attendance(youngest_grade) <= 25:
                    self.subgroups[youngest_grade] += obj.get_subgroup(youngest_grade)
                    self.grade_attendance[youngest_grade] += obj.get_grade_attendance(youngest_grade)
                    
                    for g in range(youngest_grade + 1, 4):
                        while self.get_attendance() > 25 and obj.get_grade_attendance(g) > 0:
                            for c in obj.get_subgroup(g):
                                self.add_children(c)
                                obj.remove_class(c)
                    return True  # group added successfully
                return False
        elif isinstance(obj, ClassInSchool):
            if self.get_attendance() + obj.get_attendance(self.day, self.hour) <= 25:  # adding class
                self.subgroups[obj.get_grade()].append(obj)
                self.grade_attendance[obj.get_grade()] += obj.get_attendance(self.day, self.hour)
                return True  # class added successfully
            elif obj.get_grade() == youngest_grade and self.get_grade_attendance(youngest_grade) + obj.get_attendance(self.day, self.hour) <= 25:
                self.subgroups[youngest_grade].append(obj)
                self.grade_attendance[youngest_grade] += obj.get_attendance(self.day, self.hour)

                for g in range(3, youngest_grade, -1):
                    while self.get_attendance() > 25:
                        if self.get_attendance() > 25:  # whole subgroups are being removed until a group is lesser or equal to 25
                            for c in self.subgroups[g]:
                                self.remove_class(c)
                        else:
                            break
                return True  # group added successfully
            return False