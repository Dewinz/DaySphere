import customtkinter
from communication.client import login, create_account, save_remember_me
from PIL import ImageTk, Image
import os

# TODO
# Refactor the naming to more concise.
# - MainPage should be MainPage.
# For example the LoginPage isn't really a page but a menu.
# It's parent, LoginPageFrame however is a page.
# Accessibility page?
# Backgrounds?

# Notes:
# For password hiding the assets open_white.png is being used universally since open_black.png doens't look like what it's supposed to.
# remembered is the variable to determine if client side should immediately go to MainPage or LoginPageFrame.
# remembered should be changed to read a json file to immediately log in.
remembered = False


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
    print(box_state)


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
    # TODO
    # Make an error appear rather than outright disabling the button.
    
    # Horrid line of code, wish I could wrap the text.
    if app_instance.password.get() == app_instance.ver_password.get() and app_instance.username.get() != "" and app_instance.password.get() != "" and app_instance.ver_password.get() != "" and len(app_instance.username.get()) > 5  and len(app_instance.password.get()) > 5  and len(app_instance.ver_password.get()) > 5:
        app_instance.create_account_button.configure(state="normal")
    else:
        app_instance.create_account_button.configure(state="disabled")

    
# =========== Front-End ===========
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Sets the titlebar icon.
        self.iconpath = ImageTk.PhotoImage(file=os.path.join("assets","logo@4x.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        
        # Sets the titlebar name.
        self.title("DaySphere")
        
        # Defines the on boot up resolution, would like to change it to be dynamic based off of previous session.
        # AKA if closed on second screen while windowed last session, keep it the same on next startup.
        self.geometry("1000x750")

        # Define a private variable which contains the view.
        self._view = None
        
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
        if view == MainPage:
            self._view.grid(sticky="nesw")
        else:
            self._view.grid(sticky="nesw")


# Likely the first screen you see on startup, unless if "remembere me" was True, where you should be send to MainPage.
class LoginPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        # TODO
        # Add refresh connection to server button in bottom right.
        
        # Displays "Log in" text.
        self.login_label = customtkinter.CTkLabel(self, text="Log in", font=customtkinter.CTkFont(self, size=20))
        self.login_label.grid(row=1, column=0, padx=20, pady=20)

        # Displays "Password" text.
        self.password_label = customtkinter.CTkLabel(self, text="Password", font=customtkinter.CTkFont(self, size=12))
        self.password_label.grid(row=4, column=0, padx=20, pady=0)

        # Entry that takes in the password info.
        self.pass_entry = customtkinter.CTkEntry(self, placeholder_text="", show='*')
        self.pass_entry.grid(row=5, column=0, padx=20, pady=(0, 8))
        self.pass_entry.bind("<Return>", command=lambda x: [save_remember_me(box_state),
                                                                     master.master.switch_view(MainPage) if login(self.user_entry.get(), self.pass_entry.get())
                                                                     else master.error_label.grid(row=1, column=0)])
        
        # Displays "Username" text.
        self.username_label = customtkinter.CTkLabel(self, text="Username", font=customtkinter.CTkFont(self, size=12))
        self.username_label.grid(row=2, column=0, padx=20, pady=0)
        
        # Entry that takes in the username info.
        self.user_entry = customtkinter.CTkEntry(self, placeholder_text="")
        self.user_entry.grid(row=3, column=0, padx=20, pady=(0, 8))
        self.user_entry.bind("<Return>", command=lambda x: self.pass_entry.focus_set())
        self.user_entry.focus_set()

        # Checkbox to find whether the log in information should be saved.
        # check_box_state should be in the same state as box_state.
        if box_state: check_box_state = customtkinter.StringVar(value="on")
        else: check_box_state = customtkinter.StringVar(value="off")
        self.remember_me_checkbox = customtkinter.CTkCheckBox(self, text="Remember me", command=checkbox_event, variable=check_box_state, onvalue="on", offvalue="off")
        self.remember_me_checkbox.grid(row=6, column=0, padx= 12, pady=12)

        # Button that toggles if the password is shown or hidden.
        self.hide_pass_button = customtkinter.CTkButton(self, text="", width=0, command=lambda: toggle_hidden_login(self),
                                                        image=customtkinter.CTkImage(light_image=Image.open("assets/hidden_white.png"),
                                                                                     dark_image=Image.open("assets/hidden_black.png")),
                                                                                     fg_color="transparent")
        self.hide_pass_button.grid(row=4, column=0, padx=12, pady=4, sticky="e")
        
        # The basic user log in button.
        # Lambda is used because it won't cause the login() to invoke on startup but on buttonpress.
        self.login_button = customtkinter.CTkButton(self, text="Log in",
                                                    command=lambda: [save_remember_me(box_state),
                                                                     master.master.switch_view(MainPage) if login(self.user_entry.get(), self.pass_entry.get())
                                                                     else master.error_label.grid(row=2, column=0), master.error_label_offset.grid(row=0, column=0)])
        self.login_button.grid(row=7, column=0, padx=20, pady=8)

        # (TEMPORARY) admin log in button.
        self.login_button = customtkinter.CTkButton(self, text="Admin Log in", command=lambda: admin_login(master.master))
        self.login_button.grid(row=8, column=0, padx=20, pady=8)
        
        # Create account button.
        self.acc_creation_menu_button = customtkinter.CTkButton(self, text="Create account", command=lambda: master.master.switch_view(AccountCreationPageFrame),
                                                             fg_color="transparent", hover_color="green")
        self.acc_creation_menu_button.grid(row=9, column=0, padx=20, pady=(12, 20))
        

# Boxes our view LoginPage into a nice Frame, which is the border containing all LoginPage elements.
# So the Frame takes up the entire view, and the LoginPage is centered inside.
# LoginPage's parent is LoginPageFrame, therefore master.master is used in LoginPage.
class LoginPageFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.login_page_view = LoginPage(self)
        self.login_page_view.grid(row=1, column=0)
        
        self.error_label = ErrorLabel(self, "Username or password is incorrect.")
        self.error_label_offset = customtkinter.CTkLabel(self, height=28, text="")


# Page for everything account creation.
class AccountCreationPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        # TODO
        # Remove "remember me" based on if it's needed.
        
        # Defines traces that will update every time the variable is changed.
        self.username = customtkinter.StringVar()
        self.username.trace_add("write", lambda x, y, z: password_verification(self))
        self.password = customtkinter.StringVar()
        self.password.trace_add("write", lambda x, y, z: password_verification(self))
        self.ver_password = customtkinter.StringVar()
        self.ver_password.trace_add("write", lambda x, y, z: password_verification(self))

        # Displays "Account Creation" text.
        self.acc_creation_label = customtkinter.CTkLabel(self, text="Account Creation", font=customtkinter.CTkFont(self, size=20))
        self.acc_creation_label.grid(row=0, column = 0, padx=10, pady=(20, 0))
        
        # Entry that takes in the username info.
        self.user_entry = customtkinter.CTkEntry(self, placeholder_text="Username", textvariable=self.username)
        self.user_entry.grid(row=1, column=0, padx=20, pady=(20, 8))

        # Entry that takes in the password info.
        self.pass_entry = customtkinter.CTkEntry(self, placeholder_text="Password", show='*', textvariable=self.password)
        self.pass_entry.grid(row=2, column=0, padx=20, pady=8)
        
        # Entry that takes in the password info again to verify.
        self.pass_ver_entry = customtkinter.CTkEntry(self, placeholder_text="Verify password", show='*', textvariable=self.ver_password)
        self.pass_ver_entry.grid(row=3, column=0, padx=20, pady=8)
        
        # Checkbox to find whether the log in information should be saved.
        # check_box_state should be in the same state as box_state.
        if box_state: check_box_state = customtkinter.StringVar(value="on")
        else: check_box_state = customtkinter.StringVar(value="off")
        self.remember_me_checkbox = customtkinter.CTkCheckBox(self, text="Remember me", command=checkbox_event, variable=check_box_state, onvalue="on", offvalue="off")
        self.remember_me_checkbox.grid(row=4, column=0, padx=20, pady=12, sticky="w")
        
        # Button that toggles if the password is shown or hidden.
        self.hide_pass_button = customtkinter.CTkButton(self, text="", width=0, command=lambda: toggle_hidden_creation(self),
                                                        image=customtkinter.CTkImage(light_image=Image.open("assets/hidden_white.png"),
                                                                                     dark_image=Image.open("assets/hidden_black.png")),
                                                                                     fg_color="transparent")
        self.hide_pass_button.grid(row=4, column=0, padx=12, pady=4, sticky="e")
        
        # Button that will call the logic to make an account.
        self.create_account_button = customtkinter.CTkButton(self, text="Create Account", state="disabled", 
                                                             command=lambda: [master.master.switch_view(MainPage)
                                                             if create_account(self.user_entry.get(), self.pass_entry.get()) else master.error_label.grid(row=2, column=0),
                                                             master.error_label_offset.grid(row=0, column=0)])
        self.create_account_button.grid(row=5, column=0, padx=20, pady=(8, 8))
        
        # Button to go back to login view.
        self.go_back_to_login_button = customtkinter.CTkButton(self, text="Go back", command=lambda: master.master.switch_view(LoginPageFrame),
                                                               fg_color="transparent", hover_color="red")
        self.go_back_to_login_button.grid(row=6, column=0, padx=20, pady=(12,20))


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
        
        self.error_label = ErrorLabel(self, "Account name is already in use.")
        self.error_label_offset = customtkinter.CTkLabel(self, height=28, text="")


class ErrorLabel(customtkinter.CTkFrame):
    def __init__(self, master, error):
        customtkinter.CTkFrame.__init__(self, master, fg_color="red", border_width=8, border_color="black")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # TODO
        # Beautify in general.
        
        self.error_label = customtkinter.CTkLabel(self, text=error, height=28)
        self.error_label.grid(row=0, column=0)


class SettingsPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        # TODO
        # The logout_button should also log out server side.
        
        self.acc_creation_label = customtkinter.CTkLabel(self, text="Settings", font=customtkinter.CTkFont(self, size=20))
        self.acc_creation_label.grid(row=0, column = 0, padx=10, pady=(20, 0))
        
        self.logout_button = customtkinter.CTkButton(self, text="Log out", command=lambda: master.master.switch_view(LoginPage))
        self.logout_button.grid(row=1, column=0, padx=10, pady=20)


# Boxes our view SettingsPage into a nice Frame, which is the border containing all LoginPage elements.
# So the Frame takes up the entire view, and the SettingsPage is centered inside.
# SettingsPage's parent is SettingsPageFrame, therefore master.master is used in SettingsPage.
class SettingsPageFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.account_creation_page = SettingsPage(self)
        self.account_creation_page.grid(row=1, column=0)


# The MainPage where all functions can be found and navigated to.
class MainPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.settings_menu_button = customtkinter.CTkButton(self, command=lambda: master.switch_view(SettingsPageFrame), text="", width=20, height=20,
                                                         image=customtkinter.CTkImage(light_image=Image.open("assets/gear.jpg"),
                                                                                     dark_image=Image.open("assets/gear.jpg")),
                                                                                     fg_color=None)
        self.settings_menu_button.grid(row=2, column=0, padx=20, pady=20, sticky="sw")
        
        self.button1 = customtkinter.CTkButton(self, text="Open page one", command=lambda: master.switch_view(LoginPageFrame))
        self.button1.grid(row=0, column=1, padx=20, pady=8)
        
        self.button2 = customtkinter.CTkButton(self, text="Open page two", command=lambda: master.switch_view(SettingsPage))
        self.button2.grid(row=1, column=1, padx=20, pady=8)


app = App()
app.mainloop()