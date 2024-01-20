
from Classes.Schedule import Schedule
from Classes.ClassInSchool import ClassInSchool

import os
import re

def create_classes_from_folder(directory):
    filePrefix = 'rozklad_'
    csvFilesList = [plik for plik in os.listdir(directory) if plik.startswith(filePrefix) and plik.endswith('.csv')]
    createdClasses = []

    for fileName in csvFilesList:
        result = re.match(r'rozklad_(\d+)(\w)\.csv', fileName)
        if result:
            number, letter = result.groups()
            classObject = ClassInSchool(int(number), letter)
            createdClasses.append(classObject)
            csvFilePath = os.path.join("Data", fileName)
            classObject.read_from_csv(csvFilePath)
        else:
            print(f"Wrong file name format: {fileName}")
    return createdClasses



if __name__ == '__main__':
    
    all_classes = create_classes_from_folder('Data')
    
    for school_class in all_classes:
        print(f"\nClassInSchool: {school_class.class_name}")
        school_class.print_children_layout()

    # utworzenie harmonogramu
    schedule = Schedule()    
    schedule.create_groups(all_classes)

    schedule.display_schedule2()

    schedule.save_as()
                