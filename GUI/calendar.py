import customtkinter

class CalendarDay(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.day_label = customtkinter.CTkLabel(self, text="DayNum", font=customtkinter.CTkFont(size=16))
        self.day_label.grid(row=0, column=0, padx=(4, 0), pady=(4, 0))


# Displays an entire week of days.
class CalendarWeek(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        self.calendar_day1 = CalendarDay(self)
        self.calendar_day1.grid(row=0, column=1)

        self.calendar_day2 = CalendarDay(self)
        self.calendar_day2.grid(row=0, column=2)
        
        self.calendar_day3 = CalendarDay(self)
        self.calendar_day3.grid(row=0, column=3)
        
        self.calendar_day4 = CalendarDay(self)
        self.calendar_day4.grid(row=0, column=3)
        
        self.calendar_day5 = CalendarDay(self)
        self.calendar_day5.grid(row=0, column=4)
        
        self.calendar_day6 = CalendarDay(self)
        self.calendar_day6.grid(row=0, column=5)
        
        self.calendar_day7 = CalendarDay(self)
        self.calendar_day7.grid(row=0, column=6)


class Calendar(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")

        self.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.calendar_week1 = CalendarWeek(self)
        self.calendar_week1.grid(row=0, column=0)
        
        self.calendar_week2 = CalendarWeek(self)
        self.calendar_week2.grid(row=1, column=0)
        
        self.calendar_week3 = CalendarWeek(self)
        self.calendar_week3.grid(row=2, column=0)
        
        self.calendar_week4 = CalendarWeek(self)
        self.calendar_week4.grid(row=3, column=0)
        
        self.calendar_week5 = CalendarWeek(self)
        self.calendar_week5.grid(row=4, column=0)
        


# Fits the CalendarPage to the entire view.
class CalendarPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")

        from GUI.sidebar import Sidebar
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, rowspan=2, column=0, stick="ns")
        
        self.calendar = Calendar(self)
        self.calendar.grid(row=0, column=1)

        self.offset_label = customtkinter.CTkLabel(self, text="")
        self.offset_label.grid(row=1, column=1)