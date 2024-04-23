
from Classes.ClassInSchool import ClassInSchool
from Classes.Group import Group
from Classes.ScheduleCell import ScheduleCell
import copy

class Schedule:
    def __init__(self):
        self.scheduleTable = []

    def display_schedule(self):
        for day in range(5):
            day_schedule = self.scheduleTable[day]
            print(f"Day {day + 1}")
            for hour in range(5):
                for cell in day_schedule[hour]:
                    cell.display_info()
                    print(',', end = '')
                print()

    def check_grades(self, group, school_class):
        class_grade = school_class.get_grade()
        for g in group.get_list_of_classes():
            difference = abs(g.get_grade() - class_grade)
            if difference > 1:
                return False
        return True

    def new_create_groups(self, all_classes):
        for day in range(5):
            end = False
            classes_added = [0] * len(all_classes)
            groups_for_day = []
            while not end:
                new_group = Group(day)
                i = 0
                for school_class in all_classes:
                    to_add = True
                    for hour in range(5):
                        if school_class.get_attendance(day, hour) + new_group.get_attendance(hour) > 25:
                            to_add = False
                            break
                    if to_add and classes_added[i] == 0 and self.check_grades(new_group, school_class):
                        new_group.new_add_children(day, school_class)
                        classes_added[i] = 1
                    i += 1
                if sum(classes_added) == len(classes_added):
                    end = True
                groups_for_day.append(new_group)

            print(f"Day {day + 1}")

            self.create_day_schedule(day, groups_for_day);

    def create_day_schedule(self, day, groups):
        day_schedule = []
        for hour in range(5):
            print(f"Hour {hour + 1}")
            end = False
            groups_added = [0] * len(groups)
            day_schedule.append([])
            #all_children = sum(g.get_attendance(hour) for g in groups)
            while not end:
                new_group = []
                new_attendance = [0] * 5
                i = 0
                for group in groups:
                    to_add = True
                    for h in range(hour, 5):
                        if group.get_attendance(h) + new_attendance[h] > 25:
                            to_add = False
                            break
                    if to_add and groups_added[i] == 0:
                        new_group += group.get_list_of_classes()
                        for h in range(hour, 5):   
                            new_attendance[h] += group.get_attendance(h)
                        groups_added[i] = 1
                    i += 1
                if sum(groups_added) == len(groups_added):
                    end = True
                new_cell = ScheduleCell(day, hour, new_group, new_attendance[hour])
                day_schedule[hour].append(new_cell)
        self.scheduleTable.append(day_schedule)

    def save_as(self):
        print("\nDobrze byłoby eksportować jako jakąś czytelną tabelę")