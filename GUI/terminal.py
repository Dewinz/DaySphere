import customtkinter
from tkinter import END

# Notes:
# auto_complete and auto_completion are separate, since auto_complete should show an example of what it will be auto completed to.
# And auto_completion will actually input that.


# TODO
# Decide if the TerminalPage is even required.
# Add Speech Recognition.


# A class containing the Terminal, other functionality should not be needed.
class TerminalPage(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")
        
        # Traces the text entered into the terminal_entry, this allows for possible autocomplete.
        terminal_command = customtkinter.StringVar()
        terminal_command.trace_add("write", lambda x, y, z: auto_complete(self, self.terminal_entry.get()))
        
        # Defines the entry and binds it to keys for accessibility.
        self.terminal_entry = customtkinter.CTkEntry(self, width=800, height=40, textvariable=terminal_command, font=customtkinter.CTkFont(self, size=20))
        self.terminal_entry.grid(row=1, column=0, padx=0, pady=40)
        self.terminal_entry.bind("<Tab>", command=lambda x: [auto_completion(self), self.terminal_entry.focus_set()])
        self.terminal_entry.bind("<Return>", command=lambda x: feedback(self, self.terminal_entry.get()) if auto_completed_text == "" else auto_completion(self))
        self.terminal_entry.focus_set()
        
        # Previews auto completion text.
        self.preview_label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(self, size=20), text_color="grey",
                                                    bg_color="#343638" if master.master._get_appearance_mode() == "dark" else "#F9F9FA")
        self.preview_label.grid(row=0, column=0, padx=7, pady=10, sticky="w")

        # Displays the previous used command.
        self.command_label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(self, size=16), text_color="grey",)
        self.command_label.grid(row=0, column=0)



# Fits the TerminalPage to the entire view.
class TerminalPageFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master, fg_color="transparent")
        
        from GUI.sidebar import Sidebar
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, rowspan=2, column=0, stick="ns")
        
        self.terminal_page = TerminalPage(self)
        self.terminal_page.grid(row=1, column=1)


# Will contain the logic to autocomplete text.
auto_completed_text = ""
updating = False
def auto_complete(app_instance, terminal_command):
    global auto_completed_text
    global updating
    
    if updating: return
    elif terminal_command.lower() == "auto":
        auto_completed_text = "Auto-completed"
        print(f"auto_completed_text: {auto_completed_text}")
    else:
        auto_completed_text = ""
    app_instance.preview_label.configure(text=auto_completed_text)


# Will actually autocomplete text.
def auto_completion(app_instance):
    global auto_completed_text
    global updating
    updating = True
    if auto_completed_text == "": return
    else:
        app_instance.preview_label.configure(text="")
        app_instance.terminal_entry.delete(0, END)
        print(auto_completed_text)
        app_instance.terminal_entry.insert(0, auto_completed_text)
        auto_completed_text = ""
        updating = False


# Will contain the logic to write to the screen through TerminalPageFrame.
# TerminalPageFrame can be accessed through app_instance.master.
def feedback(app_instance, terminal_command):
    # TODO debate on having a separate file for this logic, seeing as it should be able to do ALL the possible functions.
    # Add configure to command_label.
    
    if terminal_command == "": return
    print(f"Returned: {terminal_command}")
    app_instance.terminal_entry.delete(0, END)
    app_instance.command_label.configure(text=terminal_command)