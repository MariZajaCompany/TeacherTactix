import csv
import random
import os

def generate_table(rows, columns):
    # Inicjalizacja tabeli
    table = []

    # Generowanie pierwszego wiersza
    first_row = [random.randint(0, 25) for _ in range(columns)]
    table.append(first_row)

    # Generowanie kolejnych wierszy
    for i in range(1, rows):
        row = [random.randint(0, table[i - 1][j]) for j in range(columns)]
        table.append(row)

    return table


def save_to_csv(table, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(table)


def generate_and_save_files(num_grades, num_classes, rows, columns, output_folder):
    # Usunięcie istniejących plików CSV w folderze "Generated Data"
    for filename in os.listdir(output_folder):
        if filename.endswith(".csv"):
            os.remove(os.path.join(output_folder, filename))

    num_files = num_classes * num_grades
    for i in range(num_files):
        # Generowanie tabeli
        generated_table = generate_table(rows, columns)

        # Tworzenie nazwy pliku na podstawie numeru i litery
        filename = os.path.join(output_folder, f'rozklad_{i // num_classes}{chr(ord("A") + i % num_classes)}.csv')

        # Zapis do pliku CSV
        save_to_csv(generated_table, filename)


if __name__ == "__main__":
    num_grades = 4  # ile ma być roczników; tu: od 0 do 3
    num_classes = 5  # ile ma być klas w roczniku; tu" od A do E
    rows = 5  # godziny
    columns = 5  # dni tygodnia
    output_folder = "Generated Data"

    # Generowanie i zapis plików
    generate_and_save_files(num_grades, num_classes, rows, columns, output_folder)

    print(f"{num_classes * num_grades} plików zostało wygenerowanych i zapisanych.")
