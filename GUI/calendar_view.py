import customtkinter
import calendar


year = 2023
month = 9
cal = calendar.Calendar()
print(cal.monthdayscalendar(2023, 9))


def selected(master):
    # TODO
    # Make selected() be able to display the day of the button pressed.
    index = CalendarDays.get(master)
    print(f"Should show:\nSelected index: {index}")


class Calendar(customtkinter.CTk):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.calendar_days = CalendarDays(self)
        self.calendar_days.grid(row=0, column=0)


# Change this entire class to be a seperate file with all the day inidivually.
class CalendarDays(customtkinter.CTkFrame):
    def __init__(self, master, amount):
        super().__init__(master)
        self.amount = amount
        self.days = []

        for j, week in enumerate(self.amount):
            for i, value in enumerate(week):
                # Takes the year out of the variable and displays it.
                day = customtkinter.CTkButton(self, text=str(value)[5::], command=lambda: selected(self), height=25, width=25)
                day.grid(row=j, column=i, sticky="nesw")
                self.days.append(day)

    def get(self):
        day_values = []
        for day in self.days:
            day_values.append(day.cget("text"))
        return day_values


if __name__ == "__main__":
    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()
        
            # Defines the on boot up resolution, would like to change it to be dynamic based off of previous session.
            # AKA if closed on second screen while windowed last session, keep it the same on next startup.
            self.geometry("1000x750")

            self.day_frame_2 = CalendarDays(self, amount=cal.monthdatescalendar(2023, 9))
            self.day_frame_2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    
    
    app = App()
    app.mainloop()