import customtkinter
from PIL import Image
import datetime
from communication.client import request_data, save_data

selected_date = [1, 11, 2023]

month_offset = 0

original_month = 0
original_year = 1900

instance = 0

def switch_day_view(date):
    global selected_date
    selected_date = date


def divisible(x, y):
    times = 0
    while True:
        if (x - y >= 0):
            times += 1
            x = x - y
        else:
            break
    return times


def get_starting_day(month, year):
    weekday = datetime.datetime(year, month, 1).weekday()
    if weekday == 0:
        return 0
    else:
        if month % 2 == 0:
            return 30 - weekday
        else:
            return 31 - weekday


class Date():
    def __init__(self):
        global month_offset, original_month, original_year
        self.month = datetime.datetime.now().month
        self.year  = datetime.datetime.now().year
        if self.month + month_offset > 12:
            self.year += divisible(self.month + month_offset, 12)
            original_year = self.year
            self.month = (self.month + month_offset) % 12
            original_month = self.month
        elif self.month + month_offset < 1:
            self.year += divisible(self.month + month_offset, 12) - 1
            original_year = self.year
            self.month = (self.month + month_offset) % 12
            if (self.month == 0):
                self.month = 12
            original_month = self.month
        else:
            original_year = self.year
            self.month += month_offset
            original_month = self.month
        self.day = get_starting_day(self.month, self.year)
        if self.day != 0:
            self.month -= 1

counter = 35

# Determines the proper day and month for the CalendarDay class.
def get_calendar_day():
    global date, counter
    # If get_calendar_day has been called for an entire view amount of times (35), reset to initial day, month and year.
    if counter == 35:
        date = Date()
        counter = 0
    if date.month == 2:
        if date.year % 4 == 0:
            if date.day + 1 > 29:
                date.month += 1
                date.day = 1
            else:
                date.day += 1
        else:
            if date.day + 1 > 28:
                date.month += 1
                date.day = 1
            else:
                date.day += 1
    elif date.month % 2 == 0:
        if date.day + 1 > 31:
            if date.month + 1 > 12:
                date.year += 1
                date.month = 1
                date.day = 1
            else:
                date.month += 1
                date.day = 1
        else:
            date.day += 1
    else:
        if date.day + 1 > 30:
            date.month += 1
            date.day = 1
        else:
            date.day += 1
    # Counts how many times get_calendar_day() has been called.
    counter += 1
    return [date.day, date.month, date.year]


class CalendarDay(customtkinter.CTkButton):
    def __init__(self, master):
        # Specify the background for a calendar day, should be adaptive on lightmode or darkmode.
        customtkinter.CTkButton.__init__(self, master, hover=False, fg_color="black" if master.master.master.master._get_appearance_mode() == "dark" else "white",
                                         border_width=3, border_color="black" if master.master.master.master._get_appearance_mode() == "light" else "white",
                                         corner_radius=0, text="", width=254, height=201, border_spacing=0, command=lambda: [switch_day_view(self.date), master.master.master.master.switch_view(DayViewPage)])

        # Allows outside functions to interact with the current CalendarDay.
        self.date = get_calendar_day()
        
        global original_month, information
        
        self.configure(fg_color="#222222" if self.date[1] != original_month and master.master.master.master._get_appearance_mode() == "dark"
                       else "#CCCCCC" if self.date[1] != original_month and master.master.master.master._get_appearance_mode() == "light"
                       else "black" if master.master.master.master._get_appearance_mode() == "dark" else "white")

        try:
            self.day_label = customtkinter.CTkButton(self, text=f"{self.date[0]} •" if information[f"{self.date[0]}/{self.date[1]}/{self.date[2]}"][0] else self.date, font=customtkinter.CTkFont(size=30), fg_color="transparent", text_color="#1976D2" if datetime.datetime.now().day == self.date[0] and datetime.datetime.now().month == self.date[1] and datetime.datetime.now().year == self.date[2] else "white" if master.master.master.master._get_appearance_mode() == "dark" else "black", hover=False, width=30, command=lambda: [switch_day_view(self.date), master.master.master.master.switch_view(DayViewPage)])
        except:
            self.day_label = customtkinter.CTkButton(self, text=self.date[0], font=customtkinter.CTkFont(size=30), fg_color="transparent", text_color="#1976D2" if datetime.datetime.now().day == self.date[0] and datetime.datetime.now().month == self.date[1] and datetime.datetime.now().year == self.date[2] else "white" if master.master.master.master._get_appearance_mode() == "dark" else "black", hover=False, width=30, command=lambda: [switch_day_view(self.date), master.master.master.master.switch_view(DayViewPage)])
        self.day_label.grid(row=0, column=0, sticky="nw", padx=(12, 0), pady=(8, 0))

        # Displays scheduled info for the CalendarDay.
        self.info_label1 = customtkinter.CTkButton(self, text="", font=customtkinter.CTkFont(size=16), fg_color="transparent", hover=False, command=lambda: [switch_day_view(self.date), master.master.master.master.switch_view(DayViewPage)], text_color="white" if master._get_appearance_mode() == "dark" else "black")
        self.info_label1.grid(row=1, column=0, padx=(12, 0), sticky="nw")
        
        self.info_label2 = customtkinter.CTkButton(self, text="", font=customtkinter.CTkFont(size=16), fg_color="transparent", hover=False, command=lambda: [switch_day_view(self.date), master.master.master.master.switch_view(DayViewPage)], text_color="white" if master._get_appearance_mode() == "dark" else "black")
        self.info_label2.grid(row=2, column=0, padx=(12, 0), sticky="nw")

        self.info_label3 = customtkinter.CTkButton(self, text="", font=customtkinter.CTkFont(size=16), fg_color="transparent", hover=False, command=lambda: [switch_day_view(self.date), master.master.master.master.switch_view(DayViewPage)], text_color="white" if master._get_appearance_mode() == "dark" else "black")
        self.info_label3.grid(row=3, column=0, padx=(12, 0), sticky="nw")

        self.more_info_label = customtkinter.CTkButton(self, text="", font=customtkinter.CTkFont(size=16), fg_color="transparent", hover=False, command=lambda: [switch_day_view(self.date), master.master.master.master.switch_view(DayViewPage)], text_color="white" if master._get_appearance_mode() == "dark" else "black")
        self.more_info_label.grid(row=4, column=0, padx=(12, 0), sticky="nw", pady=(0, 12))
        
        get_information(self, self.date)


# Displays an entire week of days.
class CalendarWeek(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="black")

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
        customtkinter.CTkFrame.__init__(self, master, fg_color="black" if master._get_appearance_mode() == "dark" else "white")

        self.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        if self.master.master.state() == "zoomed":
            self.view_button_left = customtkinter.CTkButton(self, width=35, height=35, text="", bg_color="black" if master._get_appearance_mode() == "dark" else "white", corner_radius=12, command=lambda: switch_months(self, -1),
                                                            image=customtkinter.CTkImage(light_image=Image.open("assets/arrow_left.png"), dark_image=Image.open("assets/arrow_left.png")))
        else:
            self.view_button_left = customtkinter.CTkButton(self, width=20, height=20, text="", bg_color="black" if master._get_appearance_mode() == "dark" else "white", corner_radius=6, command=lambda: switch_months(self, -1),
                                                            image=customtkinter.CTkImage(light_image=Image.open("assets/arrow_left.png"), dark_image=Image.open("assets/arrow_left.png")))
        self.view_button_left.grid(row=0, column=1, sticky="ne", padx=(10, 0), pady=10)

        if self.master.master.state() == "zoomed":
            self.view_button_right = customtkinter.CTkButton(self, width=35, height=35, text="", bg_color="black" if master._get_appearance_mode() == "dark" else "white", corner_radius=12, command=lambda: switch_months(self, 1),
                                                             image=customtkinter.CTkImage(light_image=Image.open("assets/arrow_right.png"), dark_image=Image.open("assets/arrow_right.png")))
        else:
            self.view_button_right = customtkinter.CTkButton(self, width=20, height=20, text="", bg_color="black" if master._get_appearance_mode() == "dark" else "white", corner_radius=6, command=lambda: switch_months(self, 1),
                                                             image=customtkinter.CTkImage(light_image=Image.open("assets/arrow_right.png"), dark_image=Image.open("assets/arrow_right.png")))
        self.view_button_right.grid(row=0, column=2, sticky="ne", padx=10, pady=10)

        self.calendar_week1 = CalendarWeek(self)
        self.calendar_week1.grid(row=1, column=0, columnspan=3)

        self.calendar_week2 = CalendarWeek(self)
        self.calendar_week2.grid(row=2, column=0, columnspan=3)

        self.calendar_week3 = CalendarWeek(self)
        self.calendar_week3.grid(row=3, column=0, columnspan=3)

        self.calendar_week4 = CalendarWeek(self)
        self.calendar_week4.grid(row=4, column=0, columnspan=3)

        self.calendar_week5 = CalendarWeek(self)
        self.calendar_week5.grid(row=5, column=0, columnspan=3)
        
        global original_month, original_year
        
        self.month_label = customtkinter.CTkLabel(self, text=f"{datetime.date(1900, original_month, 1).strftime('%B')} {original_year}", font=customtkinter.CTkFont(size=35))
        self.month_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")


# Fits the CalendarPage to the entire view.
class CalendarPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="black" if master._get_appearance_mode() == "dark" else "white")

        from GUI.sidebar import Sidebar
        
        global information
        information = request_data("Calendar")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, rowspan=2, column=0, sticky="nsw")
        
        self.calendar = Calendar(self)
        self.calendar.grid(row=0, column=1)


class DayView(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")
        
        global selected_date, instance, information

        instance = self
        
        self.back_button = customtkinter.CTkButton(self, width=60, height=60, corner_radius=20, text="←", fg_color="transparent", font=customtkinter.CTkFont(size=60), hover=False,
                                                   command=lambda: [mass_update_information(self, selected_date), master.master.switch_view(CalendarPage)], text_color="white" if master._get_appearance_mode() == "dark" else "black")
        self.back_button.grid(row=0, column=0, sticky="w", padx=(60, 20), pady=(35, 20))
        
        self.day_label = customtkinter.CTkLabel(self, text=f"{selected_date[0]} {datetime.datetime(selected_date[2], selected_date[1], 1).strftime('%B')} {selected_date[2]}", font=customtkinter.CTkFont(size=60))
        self.day_label.grid(row=0, column=1, sticky="nw", padx=0, pady=(40, 20))
        
        self.add_button = customtkinter.CTkButton(self, text="+", font=customtkinter.CTkFont(size=40), height=50, width=50, command=lambda: [mass_update_information(self, selected_date), master.master.switch_view(DayViewPage)])
        self.add_button.grid(row=1, column=0, padx=10, pady=10, rowspan=5)

        try:
            self.entry_trace1 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][0])
            self.entry_trace2 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][1])
            self.entry_trace3 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][2])
            self.entry_trace4 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][3])
            self.entry_trace5 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][4])
            self.entry_trace6 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][5])
            self.entry_trace7 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][6])
            self.entry_trace8 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][7])
            self.entry_trace9 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][8])
            self.entry_trace10 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][9])
            self.entry_trace11 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][10])
            self.entry_trace12 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][11])
            self.entry_trace13 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][12])
            self.entry_trace14 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][13])
            self.entry_trace15 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][14])
            self.entry_trace16 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][15])
            self.entry_trace17 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][16])
            self.entry_trace18 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][17])
            self.entry_trace19 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][18])
            self.entry_trace20 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][19])
            self.entry_trace21 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][20])
            self.entry_trace22 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][21])
            self.entry_trace23 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][22])
            self.entry_trace24 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][23])
            self.entry_trace25 = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][24])
        except: pass
        
        self.last_entry_index = 1
        
        try:
            self.entry1 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace1, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry1.grid(row=1, column=1, sticky="nw")
            self.entry1.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry1.get(), 0), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 2
            
            self.entry2 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace2, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry2.grid(row=2, column=1, sticky="nw")
            self.entry2.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry2.get(), 1), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 3
            
            self.entry3 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace3, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry3.grid(row=3, column=1, sticky="nw")
            self.entry3.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry3.get(), 2), master.master.switch_view(DayViewPage)])

            self.last_entry_index = 4

            self.entry4 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace4, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry4.grid(row=4, column=1, sticky="nw")
            self.entry4.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry4.get(), 3), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 5
            
            self.entry5 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace5, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry5.grid(row=5, column=1, sticky="nw")
            self.entry5.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry5.get(), 4), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 6
            
            self.entry6 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace6, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry6.grid(row=6, column=1, sticky="nw")
            self.entry6.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry6.get(), 5), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 7
            
            self.entry7 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace7, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry7.grid(row=7, column=1, sticky="nw")
            self.entry7.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry7.get(), 6), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 8
            
            self.entry8 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace8, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry8.grid(row=8, column=1, sticky="nw")
            self.entry8.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry8.get(), 7), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 9
            
            self.entry9 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace9, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry9.grid(row=9, column=1, sticky="nw")
            self.entry9.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry9.get(), 8), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 10
            
            self.entry10 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace10, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry10.grid(row=10, column=1, sticky="nw")
            self.entry10.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry10.get(), 9), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 11
            
            self.entry11 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace11, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry11.grid(row=11, column=1, sticky="nw")
            self.entry11.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry11.get(), 10), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 12
            
            self.entry12 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace12, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry12.grid(row=12, column=1, sticky="nw")
            self.entry12.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry12.get(), 11), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 13
            
            self.entry13 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace13, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry13.grid(row=13, column=1, sticky="nw")
            self.entry13.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry13.get(), 12), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 14
            
            self.entry14 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace14, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry14.grid(row=14, column=1, sticky="nw")
            self.entry14.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry14.get(), 13), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 15
            
            self.entry15 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace15, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry15.grid(row=15, column=1, sticky="nw")
            self.entry15.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry15.get(), 14), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 16
            
            self.entry16 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace16, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry16.grid(row=16, column=1, sticky="nw")
            self.entry16.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry16.get(), 15), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 17
            
            self.entry17 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace17, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry17.grid(row=17, column=1, sticky="nw")
            self.entry17.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry17.get(), 16), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 18
            
            self.entry18 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace18, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry18.grid(row=18, column=1, sticky="nw")
            self.entry18.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry18.get(), 27), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 19
            
            self.entry19 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace19, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry19.grid(row=19, column=1, sticky="nw")
            self.entry19.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry19.get(), 18), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 20
            
            self.entry20 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace20, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry20.grid(row=20, column=1, sticky="nw")
            self.entry20.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry20.get(), 19), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 21
            
            self.entry21 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace21, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry21.grid(row=21, column=1, sticky="nw")
            self.entry21.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry21.get(), 20), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 22
            
            self.entry22 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace22, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry22.grid(row=22, column=1, sticky="nw")
            self.entry22.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry22.get(), 21), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 23
            
            self.entry23 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace23, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry23.grid(row=23, column=1, sticky="nw")
            self.entry23.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry23.get(), 22), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 24
            
            self.entry24 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace24, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry24.grid(row=24, column=1, sticky="nw")
            self.entry24.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry24.get(), 23), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 25
            
            self.entry25 = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.entry_trace25, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
            self.entry25.grid(row=25, column=1, sticky="nw")
            self.entry25.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.entry25.get(), 24), master.master.switch_view(DayViewPage)])
            
            self.last_entry_index = 26
        except: pass
        
        try:
            self.last_entry_trace = customtkinter.StringVar(self, information[f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}"][self.last_entry_index - 1])
        except:
            self.last_entry_trace = customtkinter.StringVar(self)
        
        self.last_entry = customtkinter.CTkEntry(self, width=800, height=30, placeholder_text="", textvariable=self.last_entry_trace, font=customtkinter.CTkFont(size=20), fg_color="#1D1E1E" if master.master._get_appearance_mode() == "dark" else "white", border_color="Black")
        self.last_entry.grid(row=self.last_entry_index, column=1, sticky="nw")
        self.last_entry.bind("<Return>", command=lambda x: [update_information(f"{selected_date[0]}/{selected_date[1]}/{selected_date[2]}", self.last_entry.get(), self.last_entry_index - 1), master.master.switch_view(DayViewPage)])



# Fits the DayView into the entire view.
class DayViewPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")

        from GUI.sidebar import Sidebar
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, rowspan=2, column=0, sticky="nsw")
        
        self.day_view = DayView(self)
        self.day_view.grid(row=0, column=1, sticky="nesw")


def get_information(day_instance, date):
    global information
    view_param = 0
    if day_instance.master.master.master.master.state() == "zoomed":
        view_param = 11
    try:
        for day_information in information[f"{date[0]}/{date[1]}/{date[2]}"]:
            if len(day_information) > 10 + view_param:
                day_information = day_information[:10 + view_param] + "..."
            if (day_instance.info_label1._text == "" or day_instance.info_label1._text == day_information):
                    day_instance.info_label1.configure(text=day_information)
            elif (day_instance.info_label2._text == "" or day_instance.info_label2._text == day_information):
                    day_instance.info_label2.configure(text=day_information)
            elif (day_instance.info_label3._text == "" or day_instance.info_label3._text == day_information):
                    day_instance.info_label3.configure(text=day_information)
            else:
                day_instance.more_info_label.configure(text="More info...")
    except: pass


def update_information(date, new_information, index = None):
    global information
    try:
        information[date][index] = new_information
    except: 
        try:
            information[date].append(new_information)
        except:
            information[date] = [new_information]
    save_data(information, "Calendar")


def mass_update_information(day_instance, date):
    global information
    new_information = []
    try:
        if day_instance.entry1.get()!= "": new_information.append(day_instance.entry1.get())
        if day_instance.entry2.get()!= "": new_information.append(day_instance.entry2.get())
        if day_instance.entry3.get()!= "": new_information.append(day_instance.entry3.get())
        if day_instance.entry4.get()!= "": new_information.append(day_instance.entry4.get())
        if day_instance.entry5.get()!= "": new_information.append(day_instance.entry5.get())
        if day_instance.entry6.get()!= "": new_information.append(day_instance.entry6.get())
        if day_instance.entry7.get()!= "": new_information.append(day_instance.entry7.get())
        if day_instance.entry8.get()!= "": new_information.append(day_instance.entry8.get())
        if day_instance.entry9.get()!= "": new_information.append(day_instance.entry9.get())
        if day_instance.entry10.get()!= "": new_information.append(day_instance.entry10.get())
        if day_instance.entry11.get()!= "": new_information.append(day_instance.entry11.get())
        if day_instance.entry12.get()!= "": new_information.append(day_instance.entry12.get())
        if day_instance.entry13.get()!= "": new_information.append(day_instance.entry13.get())
        if day_instance.entry14.get()!= "": new_information.append(day_instance.entry14.get())
        if day_instance.entry15.get()!= "": new_information.append(day_instance.entry15.get())
        if day_instance.entry16.get()!= "": new_information.append(day_instance.entry16.get())
        if day_instance.entry17.get()!= "": new_information.append(day_instance.entry17.get())
        if day_instance.entry18.get()!= "": new_information.append(day_instance.entry18.get())
        if day_instance.entry19.get()!= "": new_information.append(day_instance.entry19.get())
        if day_instance.entry20.get()!= "": new_information.append(day_instance.entry20.get())
        if day_instance.entry21.get()!= "": new_information.append(day_instance.entry21.get())
        if day_instance.entry22.get()!= "": new_information.append(day_instance.entry22.get())
        if day_instance.entry23.get()!= "": new_information.append(day_instance.entry23.get())
        if day_instance.entry24.get()!= "": new_information.append(day_instance.entry24.get())
        if day_instance.entry25.get()!= "": new_information.append(day_instance.entry25.get())
    except: pass
    try:
        information[f"{date[0]}/{date[1]}/{date[2]}"] = new_information
    except: pass
    if day_instance.last_entry.get() != "":
        
        try: information[f"{date[0]}/{date[1]}/{date[2]}"][day_instance.last_entry_index-1] = day_instance.last_entry.get()
        except: 
            print(date)
            print(information)
            information[f"{date[0]}/{date[1]}/{date[2]}"].append(day_instance.last_entry.get())
    save_data(information, "Calendar")


def switch_months(calendar_instance, switch):
    global month_offset
    month_offset += switch
    calendar_instance.master.master.switch_view(CalendarPage)