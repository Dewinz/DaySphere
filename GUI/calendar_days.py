import customtkinter

class CalendarDays(customtkinter.CTkFrame):
    def __init__(self, master, amount):
        super().__init__(master)

        monday_1 = customtkinter.CTkButton(self)