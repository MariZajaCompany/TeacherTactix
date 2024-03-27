
from Classes.ClassInSchool import ClassInSchool
from Classes.Group import Group
import copy
import csv

class Schedule:
    def __init__(self, classes):
        self.classes = classes
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


    def create_groups(self):

        for day in range(5):
            prev_groups = [[], [], [], []]
            for hour in range(5):
                present_groups = [[], [], [], []]
                # check attendance
                for school_class in self.classes:
                    class_attendance = school_class.get_attendance(day, hour)
                    if class_attendance > 0:
                        present_groups[school_class.get_grade()].append(school_class)
                
                if day == 1 and hour == 3:
                    print(" ")
                # update group size and elements
                for i in range(4):
                    expelled_groups = [[], [], [], []]
                    for group in prev_groups[i]:
                        group.set_time(day, hour)
                        for school_class in group.get_list_of_classes():
                            for g in range(4):
                                for c in present_groups[g]: 
                                    if school_class.get_class_name() == c.get_class_name(): # removing classes that are already in groups 
                                        present_groups[g].remove(c)

                        # removing classes from too big subgroups
                        for g in range(4):
                            subgroup = sorted(group.get_subgroup(g), key=lambda school_class: school_class.get_attendance(day, hour), reverse=True)
                            for school_class in subgroup:
                                if group.get_grade_attendance(g) > 25:
                                    group.remove_class(school_class) 
                                    present_groups[school_class.get_grade()].append(school_class)
                                else:
                                    break
                        
                        # removing subgroups from too big groups
                        subgroups = group.get_subgroups() # starting with the oldest group
                        expelled_group = Group(day, hour)
                        for subgroup in subgroups:
                            if group.get_attendance() > 25:
                                for school_class in subgroup:
                                    group.remove_class(school_class) # we remove each class separately (not as a whole group) - debatable
                                    #present_groups[school_class.get_grade()].append(school_class)
                                    if not expelled_group.add_children(school_class):
                                        expelled_groups[expelled_group.get_youngest_grade()].append(expelled_group)
                                        expelled_group = Group(day, hour)
                            else:
                                break
                        if expelled_group.get_attendance != 0:
                            expelled_groups[expelled_group.get_youngest_grade()].append(expelled_group)
                    prev_groups[i] += expelled_groups[i]

                new_groups = [[], [], [], []]
                
                # creating same-level groups
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
                                classes_before = group.get_list_of_classes()
                                if isinstance(another_group, Group):
                                    classes_before += another_group.get_list_of_classes()
                                elif isinstance(another_group, ClassInSchool):
                                    classes_before.append(another_group)

                                if group.add_children(another_group): # as a result of calling this function here, one of the classes MAY be deprived of its group
                                    present_groups[grade].remove(another_group)
                                    classes_after = group.get_list_of_classes()
                                    while classes_after:
                                        for c1 in classes_before:
                                            for c2 in classes_after:
                                                if c1 == c2:
                                                    classes_before.remove(c1)
                                                    classes_after.remove(c2)
                                    
                                    re_sorting = False
                                    for c in classes_before:
                                        present_groups[c.get_grade()].append(c) # allowing reassignment to classes that have lost their group as a result of being replaced
                                        re_sorting = True # classes intended for grouping should be sorted again
                                    if re_sorting:
                                        present_groups[grade] = sorted(present_groups[grade], key=lambda school_class: school_class.get_attendance(day, hour), reverse=True)
                            new_groups[grade].append(group)
                
                # creating cross-level groups
                for grade in range(3): # starting with the oldest
                    younger_grade = sorted(new_groups[grade], key=lambda group: group.get_attendance(), reverse=True)
                    older_grade = sorted(new_groups[grade+1], key=lambda group: group.get_attendance(), reverse=True)
                    indices_to_remove = []
                    for older_group_index, older_group in enumerate(older_grade):
                        for younger_group in younger_grade:
                            if younger_group.add_children(older_group):  # as a result of calling this function here, any class CANNOT be deprived of its group
                                indices_to_remove.append(older_group_index)
                                break

                    new_groups[grade+1] = [group for idx, group in enumerate(older_grade) if idx not in indices_to_remove] # removing duplicates

                if new_groups[0]: # removing the only empty group
                    if new_groups[0][0].get_attendance() == 0:
                        new_groups = [[], [], [], []]

                for grade in range(4):
                    self.add_groups(new_groups[grade], day, hour)

                prev_groups = copy.deepcopy(new_groups)
        

    def save_as(self, filepath, filename):
        days = ["", "Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
        filename = filepath + '\\'+ filename + ".csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(days)
             #row_index = 0
            for hour in range(5):
                max_number_of_groups = 0
                for day in range(5):
                    list_of_groups = self.scheduleTable[day][hour]
                    if max_number_of_groups < len(list_of_groups):
                        max_number_of_groups = len(list_of_groups)
                hour_table =  [["" for _ in range(6)] for _ in range(max_number_of_groups)]
                hour_table[0][0] = hour + 1
                for day in range(5):
                    list_of_groups = self.scheduleTable[day][hour]
                    for i, group in enumerate(list_of_groups):
                        hour_table[i][day + 1] = group.get_group_info()
                writer.writerows(hour_table)