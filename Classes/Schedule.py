
from Classes.ClassInSchool import ClassInSchool
from Classes.Group import Group
import copy

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

    def display_schedule2(self):
        for day in range(5):
            print(f"Day {day + 1}")
            for hour in range(5):
                list_of_groups = self.scheduleTable[day][hour]
                for group in list_of_groups:
                    group.display_group2()
                print()
            print()


    def create_groups(self, all_classes):

        for day in range(1):
            prev_groups = [[], [], [], []]
            for hour in range(5):
                present_groups = [[], [], [], []]
                # check attendance
                for school_class in all_classes:
                    class_attendance = school_class.get_attendance(day, hour)
                    if class_attendance > 0:
                        present_groups[school_class.get_grade()].append(school_class)
                
                # update group size and elements
                for i in range(4):
                    for group in prev_groups[i]:
                        group.set_time(day, hour)
                        for school_class in group.get_list_of_classes():
                            for c in present_groups[i]: 
                                if school_class.get_class_name() == c.get_class_name(): # removing classes that are already in groups 
                                    present_groups[i].remove(c)

                        # removing classes from too big subgroups
                        for grade in range(4):
                            subgroup = sorted(group.get_subgroup(grade), key=lambda school_class: school_class.get_attendance(day, hour), reverse=True)
                            for school_class in subgroup:
                                if group.get_grade_attendance(grade) > 25:
                                    group.remove_class(school_class)
                                    present_groups[school_class.get_grade()].append(school_class)
                                else:
                                    break
                        
                        # removing classes from too big subgroups
                        subgroups = sorted(group.get_subgroups(), key=lambda subgroup: sum(c.get_attendance(day, hour) for c in subgroup), reverse=True)
                        for subgroup in subgroups:
                            if group.get_attendance(grade) > 25:
                                for school_class in group.get_subgroup(grade):
                                    group.remove_class(school_class)
                                    present_groups[school_class.get_grade()].append(school_class)
                            else:
                                break

                new_groups = [[], [], [], []]
                
                for grade in range(4):

                    for group in prev_groups[grade]: # adding previous groups to present groups
                        present_groups[grade].append(group)
                    
                    present_groups[grade] = sorted(present_groups[grade], key=lambda school_class: school_class.get_attendance(day, hour), reverse=True)

                    while present_groups[grade]: # dzialanie tej petli jest specjalne
                        for existing_group in present_groups[grade]:
                            group = Group(day, hour)
                            present_groups[grade].remove(existing_group)
                            group.add_children(existing_group)
                            for another_group in present_groups[grade]:
                                if group.add_children(another_group):
                                    present_groups[grade].remove(another_group)
                            new_groups[grade].append(group)
                if hour == 3:
                    print(" ")
                    
                for grade in range(4):
                    self.add_groups(new_groups[grade], day, hour)

                prev_groups = copy.deepcopy(new_groups) #aktualizacja prev_groups
        

    def save_as(self):
        print("\nDobrze byłoby eksportować jako jakąś czytelną tabelę")