import customtkinter
from communication.client import login, create_account, save_remember_me
from PIL import ImageTk, Image
import os

# TODO
# Refactor the naming to more concise.
# - StartPage should be MainPage.
# For example the LoginPage isn't really a page but a menu.
# It's parent, LoginPageFrame however is a page.
# Accessibility page?
# Backgrounds?

# Notes:
# remembered is the variable to determine if client side should immediately go to StartPage or LoginPageFrame.
# remembered should be changed to read a json file to immediately log in.
remembered = True


# ============ Back-End ============

# (TEMPORARY) login logic to bypass username and password.
def admin_login(master):
    print("Admin log in attempted")
    master.switch_view(StartPage)


# Parameters cannot be passed through since it'll only run the function once then.
# Therefore we are using a global variable to get the value.
# Preferably this would be changed to be integrated into the class so that it doesn't needlessly take memory.
box_state = False
def checkbox_event():
    global box_state
    # TODO
    # Change the remember me checkbox to the corresponding state, this should also be done on startup of the loginpage.
    if box_state : box_state = False
    else : box_state = True


# Toggles the password the password between hidden and shown.
def toggle_hidden(app_instance):
    if app_instance.pass_entry.cget('show') == '':
        app_instance.pass_entry.configure(show='*')
        app_instance.hide_pass_button.configure(image=customtkinter.CTkImage(light_image=Image.open("assets/hidden_white.png"),
                                                                             dark_image=Image.open("assets/hidden_black.png")))
    else:
        app_instance.pass_entry.configure(show='')
        app_instance.hide_pass_button.configure(image=customtkinter.CTkImage(light_image=Image.open("assets/open_white.png"),
                                                                             dark_image=Image.open("assets/open_white.png")))


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
        # It currently will immediately go to StartPage.
        # But it should first actually try to log in by the server, then go to the StartPage.
        if remembered : self.switch_view(StartPage)
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
        if view == StartPage:
            self._view.grid(sticky="nesw")
        else:
            self._view.grid(sticky="nesw")


# A placeholder for the "startpage".
class StartPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        # TODO
        # Fix the login_menu_button to the very bottom left corner.
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.login_menu_button = customtkinter.CTkButton(self, text="Go back to login", command=lambda: master.switch_view(LoginPageFrame))
        self.login_menu_button.grid(column=0, padx=8, pady=8, sticky="sw")
        
        self.button1 = customtkinter.CTkButton(self, text="Open page one", command=lambda: master.switch_view(LoginPageFrame))
        self.button1.grid(row=1, column=1, padx=20, pady=8)
        
        self.button2 = customtkinter.CTkButton(self, text="Open page two", command=lambda: master.switch_view(PageTwo))
        self.button2.grid(row=5, column=1, padx=20, pady=8)


# Likely the first screen you see on startup, unless if "remembere me" was True, where you should be send to StartPage.
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
        self.pass_entry = customtkinter.CTkEntry(self, placeholder_text="")
        self.pass_entry.grid(row=5, column=0, padx=20, pady=(0, 8))
        self.pass_entry.bind("<Return>", command=lambda x: [save_remember_me(box_state),
                                                                     master.master.switch_view(StartPage) if login(self.user_entry.get(), self.pass_entry.get())
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
        check_box_state = customtkinter.StringVar(value="off")
        self.remember_me_checkbox = customtkinter.CTkCheckBox(self, text="Remember me", command=checkbox_event, variable=check_box_state, onvalue="on", offvalue="off")
        self.remember_me_checkbox.grid(row=6, column=0, padx= 12, pady=12)

        # Button that toggles if the password is shown or hidden.
        self.hide_pass_button = customtkinter.CTkButton(self, text="", width=0, command=lambda: toggle_hidden(self),
                                                        image=customtkinter.CTkImage(light_image=Image.open("assets/hidden_white.png"),
                                                                                     dark_image=Image.open("assets/hidden_black.png")),
                                                                                     fg_color="transparent")
        self.hide_pass_button.grid(row=4, column=0, padx=12, pady=4, sticky="e")
        
        # The basic user log in button.
        # Lambda is used because it won't cause the login() to invoke on startup but on buttonpress.
        self.login_button = customtkinter.CTkButton(self, text="Log in",
                                                    command=lambda: [save_remember_me(box_state),
                                                                     master.master.switch_view(StartPage) if login(self.user_entry.get(), self.pass_entry.get())
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
        
        self.error_label = ErrorLabel(self)
        self.error_label_offset = customtkinter.CTkLabel(self, height=28, text="")


# Page for everything account creation.
class AccountCreationPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        # TODO
        # Make the create_account_button be disabled at all times unless all fields are filled in and the passwords match.

        # Displays "Account Creation" text.
        self.acc_creation_label = customtkinter.CTkLabel(self, text="Account Creation", font=customtkinter.CTkFont(self, size=20))
        self.acc_creation_label.grid(row=0, column = 0, padx=10, pady=(20, 0))
        
        # Entry that takes in the username info.
        self.user_entry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.user_entry.grid(row=1, column=0, padx=20, pady=(20, 8))

        # Entry that takes in the password info.
        self.pass_entry = customtkinter.CTkEntry(self, placeholder_text="Password")
        self.pass_entry.grid(row=2, column=0, padx=20, pady=8)
        
        # Entry that takes in the password info again to verify.
        self.pass_ver_entry = customtkinter.CTkEntry(self, placeholder_text="Verify password")
        self.pass_ver_entry.grid(row=3, column=0, padx=20, pady=8)
        
        # Checkbox to find whether the log in information should be saved.
        # check_box_state should be in the same state as box_state.
        check_box_state = customtkinter.StringVar(value="off")
        self.remember_me_checkbox = customtkinter.CTkCheckBox(self, text="Remember me", command=checkbox_event, variable=check_box_state, onvalue="on", offvalue="off")
        self.remember_me_checkbox.grid(row=4, column=0, padx=20, pady=12, sticky="w")
        
        # Button that will call the logic to make an account.
        self.create_account_button = customtkinter.CTkButton(self, text="Create Account",
                                                             command=lambda: master.master.switch_view(StartPage)
                                                             if create_account(self.user_entry.get(), self.pass_entry.get()) else master.error_label.grid(row=1, column=0))
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
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.account_creation_page = AccountCreationPage(self)
        self.account_creation_page.grid(row=0, column=0)
        
        self.error_label = ErrorLabel(self)


class ErrorLabel(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="red", border_width=8, border_color="black")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # TODO
        # Change it to also have proper text="" for account creation.
        # Beautify in general.
        self.error_label = customtkinter.CTkLabel(self, text="Wrong username or password.", height=28)
        self.error_label.grid(row=0, column=0)


class PageTwo(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        customtkinter.CTkLabel(self, text="This is page two").pack(side="top", fill="x", pady=10)
        customtkinter.CTkButton(self, text="Return to start page", command=lambda: master.switch_view(StartPage)).pack()

app = App()
app.mainloop()