import csv
import os
import re
from tkinter import messagebox, filedialog

import customtkinter

customtkinter.set_appearance_mode("Light")  # Modes: "Dark", "Light"
customtkinter.set_default_color_theme("magenta.json")

current_scale = 1
data_directory = "Data"
user_manual_1 = "------- Instrukcja obsługi ------- \nWersja 1.2.9 \nProgram ten służy do generowania grafiku " \
                "dla grup w świetlicy. Dostosuj wygląd interfejsu opcjami w lewym dolnym rogu."
user_manual_2 = "Aby dodać grafik dla klasy kliknij przycisk po lewej stronie. Przycisk poniżej pozwala na zmianę ram " \
                "czasowych dla harmonogramu. Zmiany te resetują się przy ponownym uruchomieniu."
user_manual_3 = "W oknie po prawej zostaną wyświelone dodane harmonogramy. Zamknięcie programu nie usuwa dodanych klas."
user_manual_4 = "Naciśnij przycisk (Stwórz grafik), kiedy dodane zostaną wszystkie klasy. Rozpocznie się działanie algorytmu."
week_days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
day_hours = ["12:30 - 13:30", "13:30 - 14:30", "14:30 - 15:00", "15:00 - 16:00", "16:00 - 17:00"]
file_path = ""

class ClassScheduleWindow(customtkinter.CTkToplevel):
    def __init__(self, root, data_array):
        super().__init__(root)
        self.root_reference = root
        self.data_array = data_array

        self.geometry(str(600 * current_scale) + 'x' + str(420 * current_scale))
        self.title("Dodaj klasę")
        self.attributes("-topmost", True)

        self.label = customtkinter.CTkLabel(self, text="KLASA:")
        self.label.grid(row=0, column=0, padx=(0, 40))
        if data_array is None:
            self.entry_class = customtkinter.CTkEntry(self, placeholder_text="", width=30, height=30)
        else:
            self.entry_class = customtkinter.CTkEntry(self, placeholder_text=data_array[5], width=30, height=30)
        self.entry_class.grid(row=0, column=0, padx=(40, 0))

        for i in range(1, 6):
            for j in range(1, 6):
                # impossible to execute, overrides the previous entry, unable to create a list
                # self.entry = customtkinter.CTkEntry(self, placeholder_text="0", width=40, height=40)
                # self.entry.grid(row=i, column=j, padx=10, pady=10)

                self.entry_day = customtkinter.CTkLabel(self, text=week_days[j - 1], width=70, height=40,
                                                        fg_color="#E9D5DE", corner_radius=10, text_color="gray8")
                self.entry_day.grid(row=0, column=j, padx=10, pady=10)

                self.entry_hour = customtkinter.CTkLabel(self, text=day_hours[i - 1], width=70, height=40,
                                                         fg_color="#E9D5DE", corner_radius=10, text_color="gray8")
                self.entry_hour.grid(row=i, column=0, padx=10, pady=10)

        for row in range(1, 6):
            for column in range(1, 6):
                entry_name = f"entry_{row}_{column}"
                if data_array is None:
                    entry = customtkinter.CTkEntry(self, placeholder_text="0", width=40, height=40)
                else:
                    entry = customtkinter.CTkEntry(self, placeholder_text=data_array[row - 1][column - 1], width=40,
                                                   height=40)
                setattr(self, entry_name, entry)
                entry.grid(row=row, column=column, padx=10, pady=10)

        self.save_button = customtkinter.CTkButton(self, text="Zapisz", fg_color="#D4A5BC", border_width=1,
                                                   border_color="#8D3863", text_color=("gray10", "#DCE4EE"), width=40,
                                                   command=self.save_class)
        self.save_button.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")

    def save_class(self):
        if self.data_array is None:
            class_name = self.entry_class.get()
            class_name = class_name.upper()
            if not os.path.exists(data_directory):  # Check if "Data" directory exists
                os.makedirs(data_directory)  # If not, create it
            class_file = os.path.join(data_directory, f"rozklad_{class_name}.csv")  # Prepend directory path

            if not re.match(r'^[0-9][A-Z]$', class_name):
                messagebox.showwarning("Błąd",
                                       "Nazwa klasy musi składać się dokładnie z dwóch znaków, gdzie pierwszy to "
                                       "cyfra od 0 do 9, a drugi to litera od A do Z.")
                return
        else:
            class_name = self.data_array[5]
            class_file = os.path.join(data_directory, f"rozklad_{class_name}.csv")

        entry_values = []  # Create an empty list to store the values
        for row in range(1, 6):
            row_values = []  # Create a list for each row
            for column in range(1, 6):
                entry_name = f"entry_{row}_{column}"
                entry = getattr(self, entry_name)  # Get the entry object
                value = entry.get()  # Get the value of the entry
                if value == "":
                    if self.data_array is None:
                        value = "0"  # Replace empty strings with "0"
                    else:
                        value = self.data_array[row - 1][column - 1]
                row_values.append(value)  # Append the value to the row list
            entry_values.append(row_values)  # Append the row list to the main list

        if all(value.isdigit() for row in entry_values for value in row):
            with open(class_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(entry_values)
            messagebox.showinfo("Zapis udany", "Klasa została dodana.")
            self.root_reference.refresh_file_list()
            self.destroy()
        else:
            messagebox.showwarning("Błąd", "Nie wszystkie wprowadzone wartości to liczby. Dane nie zostały zapisane.")


# class TeacherScheduleWindow(customtkinter.CTkToplevel):  # TODO dodać - czy to bedzie potrzebne??
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.geometry("600x300")
#         self.title("Dodaj nauczyciela")
#         self.attributes("-topmost", True)

#         self.label = customtkinter.CTkLabel(self, text="Dodaj grafik dla nauczyciela:")
#         self.label.grid(row=0, column=0, padx=20, pady=20)

class DayHoursWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("245x430")
        self.title("Zmień godziny")
        self.attributes("-topmost", True)

        self.label = customtkinter.CTkLabel(self, text="Zmień godziny dla grafików klas\nFormat powinien zostać "
                                                       "zachowany!\n HH:MM - HH:MM")
        self.label.grid(row=0, column=0, padx=20, pady=(10, 5))

        for i in range(1, 6):
            hour_name = f"hour_{i}"
            hour = customtkinter.CTkEntry(self, placeholder_text=day_hours[i - 1], width=100,
                                          height=40)
            setattr(self, hour_name, hour)
            hour.grid(row=i, column=0, padx=10, pady=10)

        self.save_button = customtkinter.CTkButton(self, text="Zapisz", fg_color="#D4A5BC", border_width=1,
                                                   border_color="#8D3863", text_color=("gray10", "#DCE4EE"), width=40,
                                                   command=self.save_hours)
        self.save_button.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")

    def save_hours(self):
        for i in range(1, 6):
            hour_name = f"hour_{i}"
            hour = getattr(self, hour_name)  # Get the entry object
            value = hour.get()  # Get the value of the entry
            if value != "":
                day_hours[i - 1] = value
        messagebox.showinfo("Zapis udany", "Godziny zostały zmienione.")
        self.destroy()

class App(customtkinter.CTk):
    def __init__(self, start):
        super().__init__()

        self.start = start

        # configure window
        self.title("TeacherTactix.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="TeacherTactix",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # create top add buttons
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Dodaj klasę",
                                                        command=lambda: self.open_toplevel_class(None))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        # self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Test",
        #                                                 command=self.save_file_dialog())
        # self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Zmień godziny",
                                                        command=lambda: self.open_toplevel_day_hours())
        self.sidebar_button_3.grid(row=2, column=0, padx=20, pady=10)

        self.toplevel_window = None  # definition needed for the top window function

        # create bottom option buttons
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Wygląd interfejsu:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Jasny", "Ciemny"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Skalowanie interfejsu:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main label and user manual
        self.main_frame = customtkinter.CTkFrame(self, width=960, corner_radius=40)
        self.main_frame.grid(row=0, column=1, rowspan=4, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.logo_label = customtkinter.CTkLabel(self.main_frame, text="Witaj!", text_color=("#4d1535", "white"),
                                                 font=customtkinter.CTkFont(size=50, weight="bold"))
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=30, pady=10, sticky="w")

        self.logo_label = customtkinter.CTkLabel(self.main_frame, text=user_manual_1,
                                                 wraplength=400, justify="left", font=customtkinter.CTkFont(size=20))
        self.logo_label.grid(row=1, column=0, columnspan=2, padx=20, pady=1, sticky="nw")
        self.logo_label = customtkinter.CTkLabel(self.main_frame, text=user_manual_2,
                                                 wraplength=400, justify="left", font=customtkinter.CTkFont(size=20))
        self.logo_label.grid(row=2, column=0, columnspan=2, padx=20, pady=1, sticky="nw")
        self.logo_label = customtkinter.CTkLabel(self.main_frame, text=user_manual_3,
                                                 wraplength=400, justify="left", font=customtkinter.CTkFont(size=20))
        self.logo_label.grid(row=3, column=0, columnspan=2, padx=20, pady=1, sticky="nw")
        self.logo_label = customtkinter.CTkLabel(self.main_frame, text=user_manual_4,
                                                 wraplength=400, justify="left", font=customtkinter.CTkFont(size=20))
        self.logo_label.grid(row=4, column=0, columnspan=2, padx=20, pady=1, sticky="nw")

        # create view for entered data
        self.tabview = customtkinter.CTkTabview(self.main_frame, width=400, height=300)
        self.tabview.grid(row=0, column=2, columnspan=2, rowspan=4, padx=20, pady=10, sticky="nsew")
        self.tabview.add("Klasy")
        #self.tabview.add("Nauczyciele")
        self.tabview.tab("Klasy").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Klasy"),
                                                                 label_text="Lista dodanych klas", height=300)
        self.scrollable_frame.grid(row=0, column=0, rowspan=4, padx=10, pady=5, sticky="nsew")

        # create display for added classes
        self.labels = []
        self.buttons = []
        self.refresh_file_list()

        # self.tabview.tab("Nauczyciele").grid_columnconfigure(0, weight=1)
        # self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Nauczyciele"),
        #                                           text="Miejsce na wprowadzone dane nauczycieli")
        # self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)


        # create start algorithm button and refresh button

        # self.main_button_1 = customtkinter.CTkButton(self.main_frame, text="Odśwież",
        #                                              border_width=1, border_color="#8D3863", state="disabled",
        #                                              text_color=("gray10", "#DCE4EE"), command=self.refresh_file_list)
        # self.main_button_1.grid(row=4, column=2, padx=20, pady=20, sticky="nsew")
        self.main_button_2 = customtkinter.CTkButton(self.main_frame, text="Stwórz grafik",
                                                     border_width=1, border_color="#8D3863", height=60,
                                                     text_color=("gray10", "#DCE4EE"), command=self.start_algorithm)
        self.main_button_2.grid(row=4, column=2,columnspan=2, padx=20, pady=20, sticky="nsew")

    def refresh_file_list(self):
        if not os.path.exists(data_directory):  # Check if "Data" directory exists
            os.makedirs(data_directory)  # If not, create it
        class_files = [file for file in os.listdir("Data") if file.endswith(".csv") and file.startswith("rozklad")]

        for label in self.labels:
            label.destroy()
        for button in self.buttons:
            button.destroy()

        for idx, filename in enumerate(class_files):
            last_two_characters = filename[-6:-4]
            label_text = f"Klasa {filename}: {last_two_characters}"
            label = customtkinter.CTkLabel(self.scrollable_frame, text=label_text)
            label.grid(row=idx, column=0, padx=20, pady=10, sticky="nsew")
            self.labels.append(label)

            delete_button = customtkinter.CTkButton(self.scrollable_frame, text="Usuń", width=60,
                                                    command=lambda f=filename: self.delete_file(f))
            delete_button.grid(row=idx, column=2, padx=10, pady=10, sticky="nsew")
            self.buttons.append(delete_button)

            edit_button = customtkinter.CTkButton(self.scrollable_frame, text="Edytuj", width=60,
                                                  command=lambda f=filename: self.edit_file(f))
            edit_button.grid(row=idx, column=3, padx=10, pady=10, sticky="nsew")
            self.buttons.append(edit_button)

    def delete_file(self, filename):
        filepath = os.path.join("Data", filename)
        try:
            os.remove(filepath)
            self.refresh_file_list()  # Refresh the list of files after deletion
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił nieoczekiwany błąd przy usuwaniu {filename}: {e}")

    def edit_file(self, filename):
        data_array = []
        filepath = os.path.join("Data", filename)
        with open(filepath, 'r') as file:
            lines = file.readlines()

            for line in lines:
                row = line.strip().split(',')
                data_array.append(row)

        last_two_characters = filename[-6:-4]
        data_array.append(last_two_characters)
        self.open_toplevel_class(data_array)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        if new_appearance_mode == "Jasny":
            new_appearance_mode = "Light"
        else:
            new_appearance_mode = "Dark"
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        global current_scale
        current_scale = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(current_scale)

    def open_toplevel_class(self, data_array):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ClassScheduleWindow(self, data_array)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    # def open_toplevel_teacher(self):
    #     if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
    #         self.toplevel_window = TeacherScheduleWindow(self)
    #     else:
    #         self.toplevel_window.focus()

    def open_toplevel_day_hours(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DayHoursWindow(self)
        else:
            self.toplevel_window.focus()

    def start_algorithm(self):
        global file_path
        file_path = save_file_dialog()
        self.start()
    
def save_file_dialog():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Zapisz harmonogram jako...",
            initialfile="harmonogram.xlsx"
        )
        return file_path

def start_graphic_user_interface(start):
    app = App(start)
    app.mainloop()