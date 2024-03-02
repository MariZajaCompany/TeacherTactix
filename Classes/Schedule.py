
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

        for day in range(3):
            prev_groups = [[], [], [], []]
            for hour in range(5):
                present_groups = [[], [], [], []]
                # check attendance
                for school_class in all_classes:
                    class_attendance = school_class.get_attendance(day, hour)
                    if class_attendance > 0:
                        present_groups[school_class.get_grade()].append(school_class)
                
                if day == 1 and hour == 3:
                    print(" ")
                # update group size and elements
                for i in range(4):
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
                        subgroups = sorted(group.get_subgroups(), key=lambda subgroup: sum(c.get_attendance(day, hour) for c in subgroup), reverse=True)
                        for subgroup in subgroups:
                            if group.get_attendance() > 25:
                                for school_class in subgroup:
                                    group.remove_class(school_class) # we remove each class separately (not as a whole group) - debatable
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

                            # TO DO 

                            ##################
                            for another_group in present_groups[grade]:
                                if group.add_children(another_group): # w wyniku wywołania tutaj tej funkcji MOŻE nastąpić pozbawienie jakiejś z klas jej grupy 
                                    #if another_group.get_attendance(day, hour) == 0:
                                        present_groups[grade].remove(another_group)
                                        # 3 opcje - nieudane, udane poprzez merge, udane poprzez wymianę(wtedy nie powinna być usuwana z present_groups
                                        # i powinno zostać sprawdzone, które klasy zostały pozbawione grupy
                                        
                            ##################

                            new_groups[grade].append(group)
                
                # creating cross-level groups  - aktualnie nie jest możliwe w pierszym takim łączeniu otrzymac 0 i 2 klasę w jednej grupie
                for grade in range(3):
                    younger_grade = sorted(new_groups[grade], key=lambda group: group.get_attendance(), reverse=True)
                    older_grade = sorted(new_groups[grade+1], key=lambda group: group.get_attendance(), reverse=True)
                    indices_to_remove = []
                    for older_group_index, older_group in enumerate(older_grade):
                        for younger_group in younger_grade:
                            if younger_group.add_children(older_group):  # w wyniku wywołania tutaj tej funkcji NIE może nastąpić pozbawienie jakiejś z klas jej grupy 
                                indices_to_remove.append(older_group_index)
                                break

                    new_groups[grade+1] = [group for idx, group in enumerate(older_grade) if idx not in indices_to_remove] # removing duplicates
                
                # TO DO - algorytm do przydzielenia klas, które zostały wyrzucone ze swoich dotychczasowych grup
                    
                    ##################




                    #################

                if new_groups[0]: # usuwanie jedynej pustej grupy
                    if new_groups[0][0].get_attendance() == 0:
                        new_groups = [[], [], [], []]

                for grade in range(4):
                    self.add_groups(new_groups[grade], day, hour)

                prev_groups = copy.deepcopy(new_groups) #aktualizacja prev_groups
        

    def save_as(self):
        print("\nDobrze byłoby eksportować jako jakąś czytelną tabelę")