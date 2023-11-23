import customtkinter
from communication.client import login, create_account, establish_connection, logout, close_program
from GUI.sidebar import Sidebar
from PIL import ImageTk, Image
from json import load, dump
import os

# TODO
# Refactor the naming to more concise.
# - MainPage should be MainPage.
# For example the LoginPage isn't really a page but a menu.
# It's parent, LoginPageFrame however is a page.
# Accessibility page?
# Backgrounds?
# Load screen (remember me handling)? For example "Connecting to servers" with DS logo that scrolls up after done.
# Package settings.

# TODAY
# Proper welcome screen.
# First time help.
# Add actual functionality to calendars.

# Notes:
# For password hiding the assets open_white.png is being used universally since open_black.png doens't look like what it's supposed to.
# remembered is the variable to determine if client side should immediately go to MainPage or LoginPageFrame.
# remembered should be changed to read a json file to immediately log in.
with open("settings.json") as file:
    settings = load(file)

# Connects the client to the server.
establish_connection()

if settings["remember_me"]:
    remembered = login()
else: remembered = False


# ============ Back-End ============

# (TEMPORARY) login logic to bypass username and password.
def admin_login(master):
    print("Admin log in attempted")
    master.switch_view(MainPage)


# Parameters cannot be passed through since it'll only run the function once then.
# Therefore we are using a global variable to get the value.
# Preferably this would be changed to be integrated into the class so that it doesn't needlessly take memory.
box_state = False
def checkbox_event():
    global box_state
    if box_state : box_state = False
    else : box_state = True


# Toggles the password between hidden and shown on LoginPage.
def toggle_hidden_login(app_instance):
    if app_instance.pass_entry.cget("show") == '':
        app_instance.pass_entry.configure(show='*')
        app_instance.hide_pass_button.configure(image=customtkinter.CTkImage(light_image=Image.open("assets/hidden_white.png"),
                                                                             dark_image=Image.open("assets/hidden_black.png")))
    else:
        app_instance.pass_entry.configure(show='')
        app_instance.hide_pass_button.configure(image=customtkinter.CTkImage(light_image=Image.open("assets/open_white.png"),
                                                                             dark_image=Image.open("assets/open_white.png")))


# Toggles the password between hidden and shown on AccountCreationPage.
def toggle_hidden_creation(app_instance):
    if app_instance.pass_entry.cget("show") == '':
        app_instance.pass_entry.configure(show='*')
        app_instance.pass_ver_entry.configure(show='*')
        app_instance.hide_pass_button.configure(image=customtkinter.CTkImage(light_image=Image.open("assets/hidden_white.png"),
                                                                             dark_image=Image.open("assets/hidden_black.png")))
    else:
        app_instance.pass_entry.configure(show='')
        app_instance.pass_ver_entry.configure(show='')
        app_instance.hide_pass_button.configure(image=customtkinter.CTkImage(light_image=Image.open("assets/open_white.png"),
                                                                             dark_image=Image.open("assets/open_white.png")))


def password_verification(app_instance):
    # Horrid line of code, wish I could wrap the text.
    if app_instance.password.get() == app_instance.ver_password.get() and app_instance.username.get() != "" and app_instance.password.get() != "" and app_instance.ver_password.get() != "" and len(app_instance.username.get()) > 5  and len(app_instance.password.get()) > 5  and len(app_instance.ver_password.get()) > 5:
        app_instance.create_account_button.configure(state="normal")
    else:
        app_instance.create_account_button.configure(state="disabled")


def theme_interprator(theme):
    # TODO Make the code more optimised by making it a dictionary.
    if theme == "Light mode":
        return "light"
    if theme == "Dark mode":
        return "dark"
    if theme == 0:
        return "light"
    if theme == 1:
        return "dark"
    if theme == "light":
        return "Light mode"
    if theme == "dark":
        return "Dark mode"

def change_theme(theme):
    global settings

    customtkinter.set_appearance_mode(theme)

    settings["appearance"] = theme_interprator(customtkinter.AppearanceModeTracker.get_mode())
    with open("settings.json", "w") as file:
        dump(settings, file)

def save():
    from GUI.calendar import mass_update_information, selected_date, instance
    try: mass_update_information(instance, selected_date)
    except: pass
    
# =========== Front-End ===========

# The App class handles the entire app, it handles primarily startup and switching views.
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        global settings
        try: customtkinter.set_appearance_mode(settings["appearance"])
        except: pass

        # Sets the titlebar icon.
        self.iconpath = ImageTk.PhotoImage(file=os.path.join("assets","logo@4x.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        
        # Sets the titlebar name.
        self.title("DaySphere")

        # Defines the on boot up resolution, would like to change it to be dynamic based off of previous session.
        # AKA if closed on second screen while windowed last session, keep it the same on next startup.
        self.geometry("1300x975")

        # Sets the constraint on window size.
        self.minsize(1300, 975)

        # Define a private variable which contains the view.
        self._view = None
        
        # Closes the connection when program is closed.
        self.protocol("WM_DELETE_WINDOW", lambda: [save(), close_program(), self.destroy()])
        
        # If you picked "remember me" on last sesssion while logging in immediately try to log in.
        # It currently will immediately go to MainPage.
        # But it should first actually try to log in by the server, then go to the MainPage.
        if remembered : self.switch_view(MainPage)
        else : self.switch_view(LoginPageFrame)


    def switch_view(self, view):
        # Destroys current frame and replaces it with a new one.
        new_view = view(self)
        if self._view is not None:
            self._view.destroy()
        self._view = new_view
        
        # Makes it so the frame (which we call view) is allowed to take up the entire screen.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Rewrites the view onto the screen.
        # Sticky makes the view take up the entire screen.
        self._view.grid(sticky="nesw")


# Likely the first screen you see on startup, unless if "remembere me" was True, where you should be send to MainPage.
class LoginPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        # Displays "Log in" text.
        self.login_label = customtkinter.CTkLabel(self, text="Log in", font=customtkinter.CTkFont(self, size=20))
        self.login_label.grid(row=1, column=0, padx=20, pady=20)
        
        # Displays "Username" text.
        self.username_label = customtkinter.CTkLabel(self, text="Username", font=customtkinter.CTkFont(self, size=12))
        self.username_label.grid(row=2, column=0, padx=20, pady=0)
        
        # Entry that takes in the username info.
        self.user_entry = customtkinter.CTkEntry(self, placeholder_text="")
        self.user_entry.grid(row=3, column=0, padx=20, pady=(0, 8))
        self.user_entry.bind("<Return>", command=lambda x: self.pass_entry.focus_set())
        self.user_entry.focus_set()

        # Displays "Password" text.
        self.password_label = customtkinter.CTkLabel(self, text="Password", font=customtkinter.CTkFont(self, size=12))
        self.password_label.grid(row=4, column=0, padx=20, pady=0)
        
        # Button that toggles if the password is shown or hidden.
        self.hide_pass_button = customtkinter.CTkButton(self, text="", width=0, command=lambda: toggle_hidden_login(self),
                                                        image=customtkinter.CTkImage(light_image=Image.open("assets/hidden_white.png"),
                                                                                     dark_image=Image.open("assets/hidden_black.png")),
                                                                                     fg_color="transparent")
        self.hide_pass_button.grid(row=4, column=0, padx=12, pady=0, sticky="e")

        # Entry that takes in the password info.
        self.pass_entry = customtkinter.CTkEntry(self, placeholder_text="", show='*')
        self.pass_entry.grid(row=5, column=0, padx=20, pady=(0, 8))
        self.pass_entry.bind("<Return>", command=lambda x: [master.master.switch_view(MainPage) if login(self.user_entry.get(), self.pass_entry.get(), box_state)
                                                                    else master.error_label.grid(row=1, column=0)])

        # Checkbox to find whether the log in information should be saved.
        # check_box_state should be in the same state as box_state.
        if box_state: check_box_state = customtkinter.StringVar(value="on")
        else: check_box_state = customtkinter.StringVar(value="off")
        self.remember_me_checkbox = customtkinter.CTkCheckBox(self, text="Remember me", command=checkbox_event, variable=check_box_state, onvalue="on", offvalue="off")
        self.remember_me_checkbox.grid(row=6, column=0, padx= 12, pady=12)
        
        # The basic user log in button.
        # Lambda is used because it won't cause the login() to invoke on startup but on buttonpress.
        self.login_button = customtkinter.CTkButton(self, text="Log in",
                                                    command=lambda: [master.master.switch_view(MainPage) if login(self.user_entry.get(), self.pass_entry.get(), box_state)
                                                                     else master.error_label.grid(row=2, column=1)])
        self.login_button.grid(row=7, column=0, padx=20, pady=8)

        # (TEMPORARY) admin log in button.
        self.admin_login_button = customtkinter.CTkButton(self, text="Admin Log in", command=lambda: admin_login(master.master))
        self.admin_login_button.grid(row=8, column=0, padx=20, pady=8)
        
        # Create account button.
        self.acc_creation_menu_button = customtkinter.CTkButton(self, text="Create account", command=lambda: master.master.switch_view(AccountCreationPageFrame),
                                                             fg_color="transparent", hover=False,
                                                             text_color="black" if master.master._get_appearance_mode() == "light" else "white")
        self.acc_creation_menu_button.grid(row=9, column=0, padx=20, pady=(12, 20))
        

# Boxes our view LoginPage into a nice Frame, which is the border containing all LoginPage elements.
# So the Frame takes up the entire view, and the LoginPage is centered inside.
# LoginPage's parent is LoginPageFrame, therefore master.master is used in LoginPage.
class LoginPageFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.login_page_view = LoginPage(self)
        self.login_page_view.grid(row=1, column=1)
        
        # An error label that only appears after a button has been pressed.
        self.error_label = customtkinter.CTkButton(self, fg_color="#B61C1C", border_width=2, border_color="black", corner_radius=20, text="Username or password is incorrect.", font=customtkinter.CTkFont(size=20), width=80, command=lambda: self.error_label.destroy(), hover=False)
        
        # Takes up row=0, allowing for everything to be centered.
        self.offset_label = customtkinter.CTkLabel(self, height=28, text="")
        self.offset_label.grid(row=0, column=1)

        # Re-establish connection with the server button.
        self.refresh_button = customtkinter.CTkButton(self, text="", command=lambda: establish_connection(), width=20, height=20,
                                                      image=customtkinter.CTkImage(light_image=Image.open("assets/refresh.png"),
                                                                                     dark_image=Image.open("assets/refresh.png")),
                                                                                     fg_color=None)
        self.refresh_button.grid(row=2, column=2, padx=20, pady=20)
        
        self.refresh_button_offset = customtkinter.CTkLabel(self, text="", width=20, height=20)
        self.refresh_button_offset.grid(row=2, column=0, padx=20, pady=20)


# Page for everything account creation.
class AccountCreationPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        # Defines traces that will update every time the variable is changed.
        self.username = customtkinter.StringVar()
        self.username.trace_add("write", lambda x, y, z: password_verification(self))
        self.password = customtkinter.StringVar()
        self.password.trace_add("write", lambda x, y, z: password_verification(self))
        self.ver_password = customtkinter.StringVar()
        self.ver_password.trace_add("write", lambda x, y, z: password_verification(self))

        # Displays "Account Creation" text.
        self.acc_creation_label = customtkinter.CTkLabel(self, text="Account Creation", font=customtkinter.CTkFont(self, size=20))
        self.acc_creation_label.grid(row=0, column = 0, padx=10, pady=20)

        # Displays "Username" text.
        self.password_label = customtkinter.CTkLabel(self, text="Username", font=customtkinter.CTkFont(self, size=12))
        self.password_label.grid(row=1, column=0, padx=20, pady=0)

        # Entry that takes in the username info.
        self.user_entry = customtkinter.CTkEntry(self, placeholder_text="", textvariable=self.username)
        self.user_entry.grid(row=2, column=0, padx=20, pady=(0, 8))
        self.user_entry.bind("<Return>", lambda x: self.pass_entry.focus_set())

        # Displays "Password" text.
        self.username_label = customtkinter.CTkLabel(self, text="Password", font=customtkinter.CTkFont(self, size=12))
        self.username_label.grid(row=3, column=0, padx=20, pady=0)

        # Entry that takes in the password info.
        self.pass_entry = customtkinter.CTkEntry(self, placeholder_text="Password", show='*', textvariable=self.password)
        self.pass_entry.grid(row=4, column=0, padx=20, pady=(0, 8))
        self.pass_entry.bind("<Return>", lambda x: self.pass_ver_entry.focus_set())
        
        # Displays "Verify password" text.
        self.pass_ver_label = customtkinter.CTkLabel(self, text="Verify password", font=customtkinter.CTkFont(self, size=12))
        self.pass_ver_label.grid(row=5, column=0)

        # Entry that takes in the password info again to verify.
        self.pass_ver_entry = customtkinter.CTkEntry(self, placeholder_text="Verify password", show='*', textvariable=self.ver_password)
        self.pass_ver_entry.grid(row=6, column=0, padx=20, pady=(0, 8))
        
        # Checkbox to find whether the log in information should be saved.
        # check_box_state should be in the same state as box_state.
        if box_state: check_box_state = customtkinter.StringVar(value="on")
        else: check_box_state = customtkinter.StringVar(value="off")
        self.remember_me_checkbox = customtkinter.CTkCheckBox(self, text="Remember me", command=checkbox_event, variable=check_box_state, onvalue="on", offvalue="off")
        self.remember_me_checkbox.grid(row=7, column=0, padx=20, pady=12, sticky="w")
        
        # Button that toggles if the password is shown or hidden.
        self.hide_pass_button = customtkinter.CTkButton(self, text="", width=0, command=lambda: toggle_hidden_creation(self),
                                                        image=customtkinter.CTkImage(light_image=Image.open("assets/hidden_white.png"),
                                                                                     dark_image=Image.open("assets/hidden_black.png")),
                                                                                     fg_color="transparent")
        self.hide_pass_button.grid(row=7, column=0, padx=12, pady=4, sticky="e")
        
        # Button that will call the logic to make an account.
        self.create_account_button = customtkinter.CTkButton(self, text="Create Account", state="disabled", 
                                                             command=lambda: [master.master.switch_view(MainPage)
                                                             if create_account(self.user_entry.get(), self.pass_entry.get(), box_state) else [master.error_label.grid(row=2, column=0, pady=(0, 12)),
                                                             master.offset_label.grid(row=0, column=0),]])
        self.create_account_button.grid(row=8, column=0, padx=20, pady=8)
        
        # Button to go back to login view.
        self.go_back_to_login_button = customtkinter.CTkButton(self, text="Go back", command=lambda: master.master.switch_view(LoginPageFrame),
                                                               fg_color="transparent", hover_color="red", text_color="black" if master.master._get_appearance_mode() == "light"
                                                                                                                                else "white")
        self.go_back_to_login_button.grid(row=9, column=0, padx=20, pady=(12,20))


# Boxes our view AccountCreationPage into a nice Frame, which is the border containing all LoginPage elements.
# So the Frame takes up the entire view, and the AccountCreationPage is centered inside.
# AccountCreationPage's parent is AccountCreationPageFrame, therefore master.master is used in AccountCreationPage.
class AccountCreationPageFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.account_creation_page = AccountCreationPage(self)
        self.account_creation_page.grid(row=1, column=0)
        
        self.error_label = customtkinter.CTkButton(self, fg_color="#B61C1C", border_width=2, border_color="black", corner_radius=20, text="Account name is already in use.", font=customtkinter.CTkFont(size=20), width=80, command=lambda: self.error_label.destroy(), hover=False)
        self.offset_label = customtkinter.CTkLabel(self, height=28, text="")


class SettingsPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        # TODO
        # The logout_button should also log out server side.
        # Add theme settings.
        
        global settings
        
        self.settings_label = customtkinter.CTkLabel(self, text="Settings", font=customtkinter.CTkFont(self, size=40))
        self.settings_label.grid(row=0, column=0, padx=20, pady=(20, 0))
        
        self.logout_button = customtkinter.CTkButton(self, text="Log out", command=lambda: [master.master.switch_view(LoginPageFrame), logout()])
        self.logout_button.grid(row=3, column=0, padx=20, pady=20)
        
        self.theme_label = customtkinter.CTkLabel(self, text="Theme", font=customtkinter.CTkFont(self, size=20))
        self.theme_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.variable = customtkinter.StringVar(self, theme_interprator(theme_interprator(customtkinter.AppearanceModeTracker.get_mode())))
        self.variable.trace_add("write", lambda x, y, z: change_theme(theme_interprator(self.theme_menu.get())))
        
        self.theme_menu = customtkinter.CTkOptionMenu(self, values=["Light mode", "Dark mode"], variable=self.variable)
        self.theme_menu.grid(row=2, column=0, padx=20, pady=(0, 10))


# Boxes our view SettingsPage into a nice Frame, which is the border containing all LoginPage elements.
# So the Frame takes up the entire view, and the SettingsPage is centered inside.
# SettingsPage's parent is SettingsPageFrame, therefore master.master is used in SettingsPage.
class SettingsPageFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        self.account_creation_page = SettingsPage(self)
        self.account_creation_page.grid(row=0, column=1)


class MainPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure([0, 2], weight=1)
        
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, rowspan=4, column=0, sticky="nsw")
        
        self.offset_label = customtkinter.CTkLabel(self, text="")
        self.offset_label.grid(row=3, column=1)

app = App()
app.mainloop()