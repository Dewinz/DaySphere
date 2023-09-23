import customtkinter
from GUI.main import MainPage

# Likely the first screen you see on startup, unless if "remembere me" was True, where you should be send to MainPage.
class LoginPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        
        # TODO
        # Place the password hide/show button on the password entry.
        
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
                                                                     else master.error_label.grid(row=2, column=1)])
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
        self.grid_columnconfigure(1, weight=1)
        
        self.login_page_view = LoginPage(self)
        self.login_page_view.grid(row=1, column=1)
        
        # An error label that only appears after a button has been pressed.
        self.error_label = ErrorLabel(self, "Username or password is incorrect.")
        
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
        
        # TODO
        # Remove "remember me" based on if it's needed.
        # Bind the return button to the entries.
        
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
                                                             master.offset_label.grid(row=0, column=0)])
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
        self.offset_label = customtkinter.CTkLabel(self, height=28, text="")


class ErrorLabel(customtkinter.CTkFrame):
    def __init__(self, master, error):
        customtkinter.CTkFrame.__init__(self, master, fg_color="red", border_width=8, border_color="black")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # TODO
        # Beautify in general.
        
        self.error_label = customtkinter.CTkLabel(self, text=error, height=28)
        self.error_label.grid(row=0, column=0)


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