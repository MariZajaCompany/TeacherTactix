
from Classes.Schedule import Schedule
from Classes.ClassInSchool import ClassInSchool
import ControllerGUI

import os
import re

def create_classes_from_folder(directory):
    filePrefix = 'rozklad_'
    csvFilesList = [plik for plik in os.listdir(directory) if plik.startswith(filePrefix) and plik.endswith('.csv')]
    createdClasses = []

    for fileName in sorted(csvFilesList):
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



def start():
    
    data_folder = "Data"

    all_classes = create_classes_from_folder(data_folder)

    # utworzenie harmonogramu
    schedule = Schedule() 
    schedule.new_create_groups(all_classes)
    schedule.display_schedule()
    #schedule.save_as("Results", "harmonogram")
    schedule.save_as_xlsx("Results", "harmonogram_excel")

if __name__ == "__main__":
    start()
    #ControllerGUI.start_graphic_user_interface(start)
                