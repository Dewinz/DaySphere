import customtkinter
from PIL import Image


class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, bg_color="black", fg_color="black")
        
        from GUI.main import MainPage, SettingsPageFrame
        from GUI.terminal import TerminalPageFrame
        from GUI.calendar import CalendarPage
        
        self.grid_rowconfigure(3, weight=1)
        
        # Displays the home button.
        self.home_button = customtkinter.CTkButton(self, command=lambda: master.master.switch_view(MainPage), hover_color="black",
                                                   image=customtkinter.CTkImage(light_image=Image.open("assets/logo@4x.png"),
                                                                                dark_image=Image.open("assets/logo@4x.png"),
                                                                                size=(80, 80)), height=120,
                                                   fg_color="black", bg_color="black", text="")
        self.home_button.grid(row=0, column=0)

        self.terminal_button = customtkinter.CTkButton(self, command=lambda: master.master.switch_view(TerminalPageFrame), hover_color="black",
                                                       image=customtkinter.CTkImage(light_image=Image.open("assets/terminal_white.png"),
                                                                                    dark_image=Image.open("assets/terminal_white.png"),
                                                                                    size=(40, 40)), height=80,
                                                       fg_color="black", bg_color="black", text="")
        self.terminal_button.grid(row=1, column=0)
        
        self.calendar_button = customtkinter.CTkButton(self, command=lambda: master.master.switch_view(CalendarPage), hover_color="black",
                                                       image=customtkinter.CTkImage(light_image=Image.open("assets/calendar_white.png"),
                                                                                    dark_image=Image.open("assets/calendar_white.png"),
                                                                                    size=(45, 45)), height=80,
                                                       fg_color="black", bg_color="black", text="")
        self.calendar_button.grid(row=2, column=0)
        
        self.offset_label = customtkinter.CTkLabel(self, text="")
        self.offset_label.grid(row=3, column=0)
        
        self.settings_button = customtkinter.CTkButton(self, command=lambda: master.master.switch_view(SettingsPageFrame), hover_color="black",
                                                       image=customtkinter.CTkImage(light_image=Image.open("assets/gear_white.png"),
                                                                                    dark_image=Image.open("assets/gear_white.png"),
                                                                                    size=(40, 40)),  height=80,
                                                       fg_color="black", bg_color="black", text="")
        self.settings_button.grid(row=4, column=0, pady=(0, 10))