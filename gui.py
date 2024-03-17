import customtkinter

customtkinter.set_appearance_mode("Light")  # Modes: "Dark", "Light"
customtkinter.set_default_color_theme("magenta.json")

user_manual = "Ten program służy do Ten program służy doTen program służy doTen program służy doTen program służy doTen program służy doTen program służy do"


class AddClassScheduleWindow(customtkinter.CTkToplevel): #TODO dodać forms na wprowadzanie danych
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Dodaj klasę")
        self.attributes("-topmost", True)

        self.label = customtkinter.CTkLabel(self, text="Dodaj grafik dla klasy:")
        self.label.pack(padx=20, pady=20)


class AddTeacherScheduleWindow(customtkinter.CTkToplevel): #TODO dodać forms na wprowadzanie danych
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Dodaj nauczyciela")
        self.attributes("-topmost", True)

        self.label = customtkinter.CTkLabel(self, text="Dodaj grafik dla nauczyciela:")
        self.label.pack(padx=20, pady=20)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

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
                                                        command=self.open_toplevel_class)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Dodaj nauczyciela",
                                                        command=self.open_toplevel_teacher)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
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
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main label and user manual
        self.main_frame = customtkinter.CTkFrame(self, width=960, corner_radius=40)
        self.main_frame.grid(row=0, column=1, rowspan=4, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.logo_label = customtkinter.CTkLabel(self.main_frame, text="Witaj!", text_color="#4d1535",
                                                 font=customtkinter.CTkFont(size=50, weight="bold"))
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=30, pady=10, sticky="w")
        self.logo_label = customtkinter.CTkLabel(self.main_frame, text="Insturukcja obslugi",
                                                 wraplength=400, justify="left", font=customtkinter.CTkFont(size=20))
        self.logo_label.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nw")
        self.logo_label = customtkinter.CTkLabel(self.main_frame, text=user_manual,
                                                 wraplength=400, justify="left", font=customtkinter.CTkFont(size=20))
        self.logo_label.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nw")
        self.logo_label = customtkinter.CTkLabel(self.main_frame, text="TODO",  # TODO dodać instrukcje
                                                 wraplength=400, justify="left", font=customtkinter.CTkFont(size=20))
        self.logo_label.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nw")
        self.logo_label = customtkinter.CTkLabel(self.main_frame, text="TODO",
                                                 wraplength=400, justify="left", font=customtkinter.CTkFont(size=20))
        self.logo_label.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="nw")

        # create view for entered data

        self.tabview = customtkinter.CTkTabview(self.main_frame, width=400)
        self.tabview.grid(row=0, column=3, rowspan=5, padx=20, pady=10, sticky="nsew")
        self.tabview.add("Klasy")
        self.tabview.add("Nauczyciele")
        self.tabview.tab("Klasy").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.label_tab_1 = customtkinter.CTkLabel(self.tabview.tab("Klasy"),
                                                  text="Miejsce na wprowadzone dane klas")  # TODO dodać wyświetlanie widoku
        self.label_tab_1.grid(row=0, column=0, padx=20, pady=20)
        self.tabview.tab("Nauczyciele").grid_columnconfigure(0, weight=1)
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Nauczyciele"),
                                                  text="Miejsce na wprowadzone dane nauczycieli")  # TODO dodać wyświetlanie widoku
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # #  create start algorithm button # TODO znaleźć miejsce na przycisk
        # self.main_button_1 = customtkinter.CTkButton(master=self, text="Stwórz grafik", fg_color="transparent",
        #                                              border_width=2, text_color=("gray10", "#DCE4EE"),
        #                                              command=self.start_algorithm)
        # self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        if new_appearance_mode == "Jasny":
            new_appearance_mode = "Light"
        else:
            new_appearance_mode = "Dark"
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def open_toplevel_class(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AddClassScheduleWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def open_toplevel_teacher(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AddTeacherScheduleWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def start_algorithm(self):
        # TODO backend-frontend
        print("Algorytm rozpoczęty")


if __name__ == "__main__":
    app = App()
    app.mainloop()
