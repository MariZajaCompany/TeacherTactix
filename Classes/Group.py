class Group:
    def __init__(self, day, hour):
        self.listOfClasses = []
        self.numberOfChildren = 0
        self.day = day
        self.hour = hour

    def get_list_of_classes(self):
        return self.listOfClasses

    def add_class_in_school(self, classInSchool):
        if self.numberOfChildren + classInSchool.get_attendance(self.day,self.hour) <= 25:
            self.listOfClasses.append(classInSchool)
            self.numberOfChildren += classInSchool.get_attendance(self.day,self.hour)
            #print(classInSchool.get_nazwa_klasy())
            return True #classInSchool moze zostac usunieta z listy klas do podzialu
        else:
            return False