
from Classes.ClassInSchool import ClassInSchool
from Classes.Group import Group

def sorting_key(object, day, hour):
    if isinstance(object, Group):
        return object.get_number_of_children()
    elif isinstance(object, ClassInSchool):
        return object.get_attendance(day, hour)

class Schedule:
    def __init__(self):
        self.scheduleTable = [[[] for _ in range(5)] for _ in range(5)]

    def add_groups(self, list_of_groups, day, hour):
        for group in list_of_groups:
            self.scheduleTable[day][hour].append(group)

    def display_schedule(self):
        for day in range(5):
            for hour in range(5):
                print(f"Day {day + 1}, Hour {hour + 1}:")
                list_of_groups = self.scheduleTable[day][hour]
                for group in list_of_groups:
                    group.display_group()


    def create_groups(self, all_classes):
        for day in range(5):
            for hour in range(5):
                #print("Day: ", day, "Hour: ", hour)
                current_groups = [[], [], [], []]
                present_classes = [[], [], [], []]
                for school_class in all_classes:
                    if school_class.get_attendance(day, hour) > 0:
                        present_classes[school_class.class_grade].append(school_class)

                for grade in range(4):
                    
                    present_classes[grade] = sorted(present_classes[grade], key=lambda school_class: school_class.get_attendance(day, hour), reverse=True)
                    
                    if grade > 0: #sprawdzanie czy mlodsza group może "awansować" do gradeu wyżej
                        tmp_present_classes = list(present_classes[grade])
                        tmp_current_groups = list(current_groups[grade - 1])
                        for younger_group in tmp_current_groups:
                            for school_class in tmp_present_classes:
                                if younger_group.get_number_of_children() < 25 - school_class.get_attendance(day, hour):
                                    tmp_present_classes.remove(school_class)
                                    present_classes[grade].append(younger_group)
                                    current_groups[grade - 1].remove(younger_group)
                        present_classes[grade] = sorted(present_classes[grade], key=lambda object: sorting_key(object, day, hour), reverse=True)

                    while present_classes[grade]: # dzialanie tej petli jest specjalne
                            for school_class in present_classes[grade]:
                                group = Group(day, hour)
                                present_classes[grade].remove(school_class)
                                group.add_children(school_class)
                                for inna_ClassInSchool in present_classes[grade]:
                                    if group.add_children(inna_ClassInSchool):
                                        present_classes[grade].remove(inna_ClassInSchool)
                                current_groups[grade].append(group)
                    
                for grade in range(4):
                    self.add_groups(current_groups[grade], day, hour)   
        

    def save_as(self):
        print("Dobrze byłoby eksportować jako jakąś czytelną tabelę")