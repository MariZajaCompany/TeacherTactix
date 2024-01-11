
from Classes.ClassInSchool import ClassInSchool
from Classes.Group import Group
import copy

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


    def create_groups(self, list_of_classes):
        for day in range(5):
            classes_and_groups = list(list_of_classes)
            for hour in range(5):
                
                current_groups = [[], [], [], []]  # przechowuje tylko grupy
                present_classes = [[], [], [], []] # może przechowywać grupy i klasy
                for object in classes_and_groups:
                    if isinstance(object, Group):
                        group = copy.deepcopy(object)
                        group.update_group()
                        
                        # zaktualizować godzinę i liczbę dzieci w (Group)object - jakieś mogły wrócić do domu

                        present_classes[object.get_younger_grade()].append(group)
                    elif isinstance(object, ClassInSchool):
                        if object.get_attendance(day, hour) > 0:
                            present_classes[object.get_class_grade()].append(object)

                for grade in range(4):
                    
                    present_classes[grade] = sorted(present_classes[grade], key=lambda object: sorting_key(object, day, hour), reverse=True)
                    
                    if grade > 0: #sprawdzanie czy mlodsza group może "awansować" do gradeu wyżej
                        tmp_present_classes = list(present_classes[grade])
                        tmp_younger_groups = list(current_groups[grade - 1])
                        for younger_group in tmp_younger_groups:
                            for school_class in tmp_present_classes:
                                free_space = 25
                                if isinstance(school_class, Group):
                                    free_space -= school_class.get_number_of_children()
                                elif isinstance(school_class, ClassInSchool):
                                    free_space -= school_class.get_attendance(day, hour)

                                if younger_group.get_number_of_children() < free_space:
                                    tmp_present_classes.remove(school_class)
                                    present_classes[grade].append(younger_group)
                                    current_groups[grade - 1].remove(younger_group)
                        present_classes[grade] = sorted(present_classes[grade], key=lambda object: sorting_key(object, day, hour), reverse=True)

                    while present_classes[grade]: # dzialanie tej petli jest specjalne
                        for school_class in present_classes[grade]:
                            group = Group(day, hour)
                            present_classes[grade].remove(school_class)

                            for object in classes_and_groups:
                                if object == school_class:
                                    classes_and_groups.remove(object)

                            """
                            for object in classes_and_groups:
                                if isinstance(object, Group) and isinstance(school_class, Group):
                                    if object == school_class:
                                        classes_and_groups.remove(object)
                                elif isinstance(object, ClassInSchool) and isinstance(school_class, ClassInSchool):
                                    if object.get_class_name() == school_class.get_class_name()
                                        classes_and_groups.remove(object)
                            """
                            
                            group.add_children(school_class)
                            for another_school_class in present_classes[grade]:
                                if group.add_children(another_school_class):
                                    present_classes[grade].remove(another_school_class)
                                    for object in classes_and_groups:
                                        if object == another_school_class:
                                            classes_and_groups.remove(object)
                            current_groups[grade].append(group)
                            classes_and_groups.append(group)
                    
                for grade in range(4):
                    self.add_groups(current_groups[grade], day, hour)   
        

    def save_as(self):
        print("Dobrze byłoby eksportować jako jakąś czytelną tabelę")