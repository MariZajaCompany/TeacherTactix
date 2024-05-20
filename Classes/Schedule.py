
from Classes.ClassInSchool import ClassInSchool
from Classes.Group import Group
from Classes.ScheduleCell import ScheduleCell
import copy
import csv
import os
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side, PatternFill

TESTING = True

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

            self.create_day_schedule(day, groups_for_day);

    def create_day_schedule(self, day, groups):
        day_schedule = []
        for hour in range(5):
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

    def save_as(self, filepath, filename):
        days = ["Godzina", "Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]

        full_path = os.path.join(filepath, filename + ".csv")
        counter = 1
        while os.path.exists(full_path):
            full_path = os.path.join(filepath, f"{filename}({counter}).csv")
            counter += 1

        with open(full_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(days)
            for hour in range(5):
                max_number_of_groups = 0
                for day in range(5):
                    schedule_cells = self.scheduleTable[day][hour]
                    if max_number_of_groups < len(schedule_cells):
                        max_number_of_groups = len(schedule_cells)
                hour_table =  [["" for _ in range(6)] for _ in range(max_number_of_groups)]
                hour_table[0][0] = hour + 1
                for day in range(5):
                    schedule_cells = self.scheduleTable[day][hour]
                    for i, cell in enumerate(schedule_cells):
                        if not TESTING:
                            hour_table[i][day + 1] = cell.get_info()
                        else:
                            hour_table[i][day + 1] = cell.get_info_with_sizes()
                writer.writerows(hour_table)

    def save_as_xlsx(self, filepath, filename):
        column_names = ["Godzina", "Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
        row_names = ["11:30 - 12:30", "12:30 - 13:30", "13:30 - 14:30", "14:30 - 15:30", "15:30 - 16:30", "16:30 - 17:00"]
        wb = Workbook()
        ws = wb.active
        ws.append(column_names)
        wrap_alignment = Alignment(wrap_text=True)
        table_length = 0
        for hour in range(5):
            max_number_of_groups = 0
            for day in range(5):
                schedule_cells = self.scheduleTable[day][hour]
                if max_number_of_groups < len(schedule_cells):
                    max_number_of_groups = len(schedule_cells)

            hour_table = [["" for _ in range(6)] for _ in range(max_number_of_groups)]
            hour_table[0][0] = row_names[hour]
            for day in range(5):
                schedule_cells = self.scheduleTable[day][hour]
                for i, cell in enumerate(schedule_cells):
                    if not TESTING:
                        hour_table[i][day + 1] = cell.get_info()
                    else:
                        hour_table[i][day + 1] = cell.get_info_with_sizes()
                

            for row in hour_table:
                ws.append(row)
                ws.append(["" for _ in range(6)])
                table_length += 2

            # Zastosowanie zawijania tekstu do wszystkich komórek
            for row in ws.iter_rows(min_row=1, max_col=6, max_row=ws.max_row):
                for cell in row:
                    cell.alignment = wrap_alignment
        
        # Scalanie komórek
        current_value = None
        start_row = None

        for row in range(2, table_length + 2):
            cell_value = ws[f'A{row}'].value
            if cell_value is not None and cell_value != '':  # Znaleziono nową wartość
                if current_value is not None and start_row is not None:  # Scal poprzednie komórki
                    end_row = row - 1
                    if end_row > start_row:  # Scal tylko jeśli jest co scalać
                        ws.merge_cells(start_row=start_row, start_column=1, end_row=end_row, end_column=1)
                current_value = cell_value
                start_row = row
            elif cell_value is None or cell_value == '':  # Pusta komórka
                continue
        if current_value is not None and start_row is not None:
            end_row = table_length + 1
            if end_row > start_row:
                ws.merge_cells(start_row=start_row, start_column=1, end_row=end_row, end_column=1)
        
        # Definiowanie kolumn, dla których chcesz ustawić szerokość
        columns = ['A', 'B', 'C', 'D', 'E', 'F']
        empty_block = False
        start_row = None
        for col in range(1, 6):
            for row in range(2, table_length + 2, 2):
                cell_value = ws[f'{columns[col]}{row}'].value
                if cell_value is None or cell_value == '':  # Pusta komórka
                    if not empty_block:
                        start_row = row
                        empty_block = True
                else:
                    if empty_block:
                        ws.merge_cells(start_row=start_row, start_column=col+1, end_row=row - 1, end_column=col+1)
                        empty_block = False

        # Ustawianie szerokości kolumn
        for col in columns:
            ws.column_dimensions[col].width = 20

        # Ustawianie wysokości wierszy na nauczycieli
        for row in range(3, table_length + 3, 2):
            ws.row_dimensions[row].height = 30

        # Ustawienie środkowania dla kolumny A
        for cell in ws['A']:
            cell.alignment = Alignment(horizontal='center', vertical='center')

        
        # Przypisanie stylu ramki
        border_style = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
        for i in range(1, table_length + 2):
            for j in range(1, 7):
                cell = ws.cell(row=i, column=j)
                cell.border = border_style

        full_path = os.path.join(filepath, filename + ".xlsx")
        counter = 1
        while os.path.exists(full_path):
            full_path = os.path.join(filepath, f"{filename}({counter}).xlsx")
            counter += 1
        wb.save(full_path)