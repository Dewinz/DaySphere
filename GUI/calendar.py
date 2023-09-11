import customtkinter
import calendar

cal = calendar.Calendar()
print(cal.monthdayscalendar(2023, 9))

class Calendar(customtkinter.CTk):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.calendar_days = CalendarDays(self)
        self.calendar_days.grid(row=0, column=0)
        

        
class CalendarDays(customtkinter.CTkFrame):
    def __init__(self, master, amount):
        super().__init__(master)
        self.amount = amount
        self.days = []

        for j, week in enumerate(self.amount):
            for i, value in enumerate(week):
                day = customtkinter.CTkLabel(self, text=value)
                day.grid(row=j, column=i, padx=25, pady=25, sticky="nesw")
                self.days.append(day)

    def get(self):
        pass


if __name__ == "__main__":
    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()
        
            # Defines the on boot up resolution, would like to change it to be dynamic based off of previous session.
            # AKA if closed on second screen while windowed last session, keep it the same on next startup.
            self.geometry("1000x750")

            self.checkbox_frame_2 = CalendarDays(self, amount=cal.monthdatescalendar(2023, 9))
            self.checkbox_frame_2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    
    app = App()
    app.mainloop()
