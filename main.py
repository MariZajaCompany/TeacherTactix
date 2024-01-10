from Classes.Teacher import Teacher
from Classes.ClassInSchool import ClassInSchool
from Classes.Group import Group
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
            #print(f"Nazwa pliku: {fileName}, ClassInSchool: {classObject.poziom_klasy}, {classObject.letter_klasy}")
            csvFilePath = os.path.join("Data", fileName)
            classObject.read_from_csv(csvFilePath)
        else:
            print(f"Wrong file name format: {fileName}")

    return createdClasses

if __name__ == '__main__':
    
    listOfClasses = create_classes_from_folder('Data')
    numberOfClasses = len(listOfClasses)

    for classInSchool in listOfClasses:
        print(f"\nClassInSchool: {classInSchool.className}")
        classInSchool.print_children_layout()

    # utworzenie harmonogramu
    
    for day in range(1):
        for hour in range(5):
            listOfCurrent = []
            listOfGroups = []
            for classInSchool in listOfClasses:
                if classInSchool.get_attendance(day, hour) > 0:
                    listOfCurrent.append(classInSchool)
            
            listOfCurrent = sorted(listOfCurrent, key=lambda ClassInSchool: ClassInSchool.get_attendance(day, hour), reverse=True)

            while listOfCurrent: # dzialanie tej petli jest specjalne
                for classInSchool in listOfCurrent:
                    group = Group(day, hour)
                    listOfCurrent.remove(classInSchool)
                    
                    group.add_class_in_school(classInSchool)
                    for nextClassInSchool in listOfCurrent:
                        if group.add_class_in_school(nextClassInSchool):
                            listOfCurrent.remove(nextClassInSchool)
                    listOfGroups.append(group)
            
            if listOfGroups:
                print("Day: ", day, "Hour: ", hour)
                for group in listOfGroups:
                    for classInSchool in group.get_list_of_classes():
                        print(f"{classInSchool.get_class_name()} ({classInSchool.get_attendance(day, hour)})", end=" + " if group.get_list_of_classes().index(classInSchool) < len(group.get_list_of_classes()) - 1 else "",)
                    print()  # Dodaj nową linię po wyświetleniu wszystkich klas w grupie
            



            
            

    """
    # Przykład Teachera:
    Teacher = Teacher("Jan Kowalski", 1)
    print("\nJan Kowalski:")
    Teacher.wczytaj_z_csv("Data\\jan_kowalski.csv")
    Teacher.wyswietl_dostepnosc()
    """
