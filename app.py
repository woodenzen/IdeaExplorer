import customtkinter

customtkinter.set_appearance_mode("dark")

class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
        # self.label = customtkinter.CTkLabel(self)
        # self.label.grid(row=0, column=0, padx=20)
        
class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Idea Storm")
        self.add("Tag Map")
        self.add("Subatomic")

        # add widgets on tabs
        self.label = customtkinter.CTkLabel(self.tab("Idea Storm"))
        self.label.grid(row=0, column=0, padx=20, pady=10)
        self.label = customtkinter.CTkLabel(self.tab("Tag Map"))
        self.label.grid(row=0, column=0, padx=20, pady=10)
        self.label = customtkinter.CTkLabel(self.tab("Subatomic"))
        # self.label.grid(row=0, column=0, padx=20, pady=10)
        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("1000x250")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        

        # self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        # self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        # self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        # self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=2, column=0, padx=10, pady=10)
        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="ews")
        self.my_frame = MyFrame(master=self, width=300, height=200, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=1, column=0, sticky="nsew")

        # add widgets onto the frame...
    def button_callback(self):
        print("button pressed")
        
app = App()
app.mainloop()