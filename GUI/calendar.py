import customtkinter


# Initializes what the first day will say and count from there.
# TODO
# Make the code less nested/more efficient.

day = 1
month = 1
year  = 1

day_number = day
month_number = month
year_number = year

counter = 0

def get_calendar_day():
    global day_number, day, month_number, month, year_number, year, counter
    if month_number == 2:
        if year_number % 4 == 0:
            if day_number + 1 > 29:
                month_number += 1
                day_number = 1
            else:
                day_number += 1
        else:
            if day_number + 1 > 28:
                month_number += 1
                day_number = 1
            else:
                day_number += 1
    elif month_number % 2 == 1:
        if day_number + 1 > 31:
            month_number += 1
            day_number = 1
        else:
            day_number += 1
    else:
        if day_number + 1 > 30:
            if month_number + 1 > 12:
                year_number += 1
                month_number = 1
                day_number = 1
            else:
                month_number += 1
                day_number = 1
        else:
            day_number += 1
    # Counts how many times get_calendar_day() has been called.
    counter += 1
    # If get_calendar_day has been called for an entire view amount of times (35), reset to initial day, month and year.
    if counter == 35:
        day_number = day
        month_number = month
        year_number - year
        counter = 0
    # Change to return the month and day_number, if month is odd from the rest, show it.
    # return day_number


# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(customtkinter.CTkCanvas):
    def __init__(self,parent,**kwargs):
        customtkinter.CTkCanvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)


class CalendarDay(ResizingCanvas):
    def __init__(self, master):
        # Specify the background for a calendar day, should be adaptive on lightmode or darkmode.
        customtkinter.CTkCanvas.__init__(self, master, bg="black" if master.master.master.master._get_appearance_mode() == "dark" else "white")

        self.day_label = customtkinter.CTkLabel(self, text=day_number, font=customtkinter.CTkFont(size=30))
        self.day_label.grid(row=0, column=0, sticky="nw", padx=8, pady=8)

        get_calendar_day()

        self.info_label = customtkinter.CTkLabel(self, text="TODO", font=customtkinter.CTkFont(size=16))
        self.info_label.grid(row=1, column=0, padx=8, pady=4, sticky="w")

        # Makes sure the CalendarDay takes up as much space as it can.
        self.offset_label = customtkinter.CTkLabel(self, text="")
        self.offset_label.grid(row=10, column=10, padx=200, pady=200)


# Displays an entire week of days.
class CalendarWeek(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        self.calendar_day1 = CalendarDay(self)
        self.calendar_day1.grid(row=0, column=0)

        self.calendar_day2 = CalendarDay(self)
        self.calendar_day2.grid(row=0, column=1)
        
        self.calendar_day3 = CalendarDay(self)
        self.calendar_day3.grid(row=0, column=2)
        
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
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, rowspan=2, column=0, stick="ns")
        
        self.calendar = Calendar(self)
        self.calendar.grid(row=0, column=1)