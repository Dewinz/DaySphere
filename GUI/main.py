# TODO 
# Make function page (undetermined).
# Check is regular tkinter can be altered into a modern look. (Since CTk and Tk should be interchangeable.)
#   If so try to modernize this example: https://www.geeksforgeeks.org/python-gui-calendar-using-tkinter/

# Notes:
# login() and admin_login() are currently being used as the placeholder command to log in.
# Either change function called in Buttons or repurpose login() and admin_login()


import customtkinter

def login(username, password):
    print(f"User log in attempted with parameters.\nUsername: {username}\nPassword: {password}")

def admin_login():
    print("Admin log in attempted")

# Parameters cannot be passed through since it'll only run the function once then.
# Therefore we are using a global variable to get the value.
# Preferably this would be changed to be integrated into the class so that it doesn't needlessly take memory.
boxState = False
def checkbox_event():
        global boxState
        if boxState : boxState = False
        else : boxState = True
        print(boxState)



# App class defines everything that will be displayed.
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()  
        self.title("DaySphere")
        # Defines the on boot up resolution, would like to change it to be dynamic based off of previous session.
        # AKA if closed on second screen while windowed last session, keep it the same on next startup.
        self.geometry("1000x750")

        self.label = customtkinter.CTkLabel(self, text="", fg_color="transparent")    
        self.label.pack(padx=20, pady=120)

        # Entry that takes in the username info.
        self.userEntry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.userEntry.pack(padx=20, pady=8)

        # Entry that takes in the password info.
        self.passEntry = customtkinter.CTkEntry(self, placeholder_text="Password")
        self.passEntry.pack(padx=20, pady=8)

        # Checkbox to find whether the log in information should be saved.
        # checkBoxState should be in the same state as boxState.
        checkBoxState = customtkinter.StringVar(value="off")
        self.rememberMeCheckBox = customtkinter.CTkCheckBox(self, text="Remember me", command=checkbox_event, variable=checkBoxState, onvalue="on", offvalue="off")
        self.rememberMeCheckBox.pack(padx= 12, pady=12)

        # The basic user log in button.
        # Lambda is used because it won't cause the login() to invoke on startup but on buttonpress.
        self.loginButton = customtkinter.CTkButton(self, text="Log in", command=lambda: login(self.userEntry.get(), self.passEntry.get()))
        self.loginButton.pack(padx=20, pady=8)

        # (TEMPORARY) admin log in button.
        self.adminButton = customtkinter.CTkButton(self, text="Admin Log in", command=admin_login)
        self.adminButton.pack(padx=20, pady=8)


# Defines an instance of the app class and runs it.
# The class can not be run on it's own, it needs to be initialized.
app = App()
app.mainloop()