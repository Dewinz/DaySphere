from tkinter import *
from PIL import Image, ImageTk

# root = Tk()
# root.geometry('600x600')

# min_w = 50 # Minimum width of the frame
# max_w = 200 # Maximum width of the frame
# cur_width = min_w # Increasing width of the frame
# expanded = False # Check if it is completely exanded

# def expand():
#     global cur_width, expanded
#     cur_width += 10 # Increase the width by 10
#     rep = root.after(5,expand) # Repeat this func every 5 ms
#     frame.config(width=cur_width) # Change the width to new increase width
#     if cur_width >= max_w: # If width is greater than maximum width 
#         expanded = True # Frame is expended
#         root.after_cancel(rep) # Stop repeating the func
#         fill()

# def contract():
#     global cur_width, expanded
#     cur_width -= 10 # Reduce the width by 10 
#     rep = root.after(5,contract) # Call this func every 5 ms
#     frame.config(width=cur_width) # Change the width to new reduced width
#     if cur_width <= min_w: # If it is back to normal width
#         expanded = False # Frame is not expanded
#         root.after_cancel(rep) # Stop repeating the func
#         fill()

# def fill():
#     if expanded: # If the frame is exanded
#         # Show a text, and remove the image
#         home_b.config(text='Home',image='',font=(0,21))
#         set_b.config(text='Settings',image='',font=(0,21))
#         ring_b.config(text='Bell Icon',image='',font=(0,21))
#     else:
#         # Bring the image back
#         home_b.config(image=home,font=(0,21))
#         set_b.config(image=settings,font=(0,21))
#         ring_b.config(image=ring,font=(0,21))

# # Define the icons to be shown and resize it
# home = ImageTk.PhotoImage(Image.open('assets/logo@4x.png').resize((40,40), Image.LANCZOS))
# settings = ImageTk.PhotoImage(Image.open('assets/gear.jpg').resize((40,40),Image.LANCZOS))
# ring = ImageTk.PhotoImage(Image.open('assets/refresh.png').resize((40,40),Image.LANCZOS))

# root.update() # For the width to get updated
# frame = Frame(root,bg='orange',width=50,height=root.winfo_height())
# frame.grid(row=0,column=0) 

# # Make the buttons with the icons to be shown
# home_b = Button(frame,image=home,bg='orange',relief='flat')
# set_b = Button(frame,image=settings,bg='orange',relief='flat')
# ring_b = Button(frame,image=ring,bg='orange',relief='flat')

# # Put them on the frame
# home_b.grid(row=0,column=0,pady=10)
# set_b.grid(row=1,column=0,pady=50)
# ring_b.grid(row=2,column=0)

# # Bind to the frame, if entered or left
# frame.bind('<Enter>',lambda e: expand())
# frame.bind('<Leave>',lambda e: contract())

# # So that it does not depend on the widgets inside the frame
# frame.grid_propagate(False)

# root.mainloop()

import customtkinter


class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, bg_color="black", fg_color="black")
        
        from GUI.main import app, MainPage, SettingsPageFrame
        from GUI.terminal import TerminalPageFrame
        # from GUI.calendar import CalendarPageFrame
        
        self.grid_rowconfigure(3, weight=1)
        
        # Displays the home button.
        self.home_button = customtkinter.CTkButton(self, command=lambda: app.switch_view(MainPage), hover_color="black",
                                                   image=customtkinter.CTkImage(light_image=Image.open("assets/logo@4x.png"),
                                                                                dark_image=Image.open("assets/logo@4x.png"),
                                                                                size=(80, 80)), height=120,
                                                   fg_color="black", bg_color="black", text="")
        self.home_button.grid(row=0, column=0, pady=(0, 0))

        self.terminal_button = customtkinter.CTkButton(self, command=lambda: app.switch_view(TerminalPageFrame), hover_color="black",
                                                       image=customtkinter.CTkImage(light_image=Image.open("assets/terminal_black.png"),
                                                                                    dark_image=Image.open("assets/terminal_white.png"),
                                                                                    size=(40, 40)), height=80,
                                                       fg_color="black", bg_color="black", text="")
        self.terminal_button.grid(row=1, column=0)
        
        self.calendar_button = customtkinter.CTkButton(self, command=lambda: app.switch_view(CalendarPageFrame), hover_color="black",
                                                       image=customtkinter.CTkImage(light_image=Image.open("assets/calendar_black.png"),
                                                                                    dark_image=Image.open("assets/calendar_white.png"),
                                                                                    size=(45, 45)), height=80,
                                                       fg_color="black", bg_color="black", text="")
        self.calendar_button.grid(row=2, column=0)
        
        self.offset_label = customtkinter.CTkLabel(self, text="")
        self.offset_label.grid(row=3, column=0)
        
        self.settings_button = customtkinter.CTkButton(self, command=lambda: app.switch_view(SettingsPageFrame), hover_color="black",
                                                       image=customtkinter.CTkImage(light_image=Image.open("assets/gear_black.jpg"),
                                                                                    dark_image=Image.open("assets/gear_white.png"),
                                                                                    size=(40, 40)),  height=80,
                                                       fg_color="black", bg_color="black", text="")
        self.settings_button.grid(row=4, column=0)