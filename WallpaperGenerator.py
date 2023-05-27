from QuoteWallpaper import GenerateWallpaper
import customtkinter
import tkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Quote Wallpaper Generator")
        self.windowWidth = 1100
        self.windowHeight = 650
        self.geometry(f"{self.windowWidth}x{self.windowHeight}")
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebarWidth = 140
        self.sidebar_frame = customtkinter.CTkFrame(self, width=self.sidebarWidth, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Quote Wallpaper", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="nw")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=self.windowWidth-self.sidebarWidth)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(10, 0), sticky="nw")
        self.tabview.add("OpenAI")
        self.tabview.add("Free")
        self.tabview.tab("OpenAI").grid_columnconfigure(3, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Free").grid_columnconfigure(0, weight=1)
        self.categories = [] # ['business', 'change', 'character', 'competition', 'education', 'faith', 'freedom', 'friendship', 'future', 'happiness', 'history', 'honor', 'humorous', 'inspirational', 'life', 'love', 'motivational', 'nature', 'politics', 'power-quotes', 'religion', 'science', 'self-help', 'social-justice', 'sports', 'success', 'technology', 'virtue', 'wisdom']
        self.artStyle = ['Abstract', 'Anime', 'Creative', 'Oil Painting', 'Realistic', 'Sketch', 'Portrait']
        self.language_var = tkinter.StringVar(value = "")
        self.category_var = tkinter.StringVar(value="")
        self.artStyle_var = tkinter.StringVar(value="")
        self.errorStr_var = tkinter.StringVar(value="")
        self.cbSquare_var = tkinter.StringVar(value="0")
        self.cbHorizontal_var = tkinter.StringVar(value="0")
        self.cbVertical_var = tkinter.StringVar(value="0")
        self.cbCaption_var = tkinter.StringVar(value="0")
        self.cbNoCaption_var = tkinter.StringVar(value="0")
        self.cbPadded_var = tkinter.StringVar(value="0")
        
        self.optionmenu_lang_label = customtkinter.CTkLabel(self.tabview.tab("OpenAI"), text="Language: ")
        self.optionmenu_lang_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nw")
        self.optionmenu_lang = customtkinter.CTkOptionMenu(self.tabview.tab("OpenAI"), variable=self.language_var, values=["English", "Hindi"], command=self.select_language_event)
        self.optionmenu_lang.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="nw")
        self.optionmenu_1_label = customtkinter.CTkLabel(self.tabview.tab("OpenAI"), text="Category: ")
        self.optionmenu_1_label.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="nw")
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("OpenAI"), variable=self.category_var, values=self.categories)
        self.optionmenu_1.grid(row=1, column=1, padx=20, pady=(20, 10), sticky="nw")
        self.optionmenu_2_label = customtkinter.CTkLabel(self.tabview.tab("OpenAI"), text="Art Style: ")
        self.optionmenu_2_label.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="nw")
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("OpenAI"), variable=self.artStyle_var, values=self.artStyle)
        self.optionmenu_2.grid(row=2, column=1, padx=20, pady=(20, 10), sticky="nw")
        self.textbox_1_label = customtkinter.CTkLabel(self.tabview.tab("OpenAI"), text="Vibe (Optional): ")
        self.textbox_1_label.grid(row=3, column=0, padx=20, pady=(20, 0), sticky="nw")
        self.textbox_1 = customtkinter.CTkTextbox(self.tabview.tab("OpenAI"), width=self.windowWidth, height=10)
        self.textbox_1.grid(row=3, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1_label = customtkinter.CTkLabel(master=self.tabview.tab("OpenAI"), text="Export Format(s): ")
        self.checkbox_1_label.grid(row=4, column=0, padx=20, pady=(20, 0), sticky="nw")
        self.checkbox_frame = customtkinter.CTkFrame(self.tabview.tab("OpenAI"), fg_color="transparent")
        self.checkbox_frame.grid(row=4, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.checkbox_11 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text="Square", variable=self.cbSquare_var)
        self.checkbox_11.grid(row=0, column=0, pady=(0, 0), padx=20, sticky="nw")
        self.checkbox_11 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text="Blur-Padded Horizontal", variable=self.cbPadded_var)
        self.checkbox_11.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="nw")
        self.checkbox_12 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text="Horizontal", variable=self.cbHorizontal_var)
        self.checkbox_12.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="nw")
        self.checkbox_13 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text="Vertical", variable=self.cbVertical_var)
        self.checkbox_13.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="nw")
        self.checkbox_14 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text="Caption", variable=self.cbCaption_var)
        self.checkbox_14.grid(row=0, column=1, pady=(0, 0), padx=20, sticky="nw")
        self.checkbox_15 = customtkinter.CTkCheckBox(master=self.checkbox_frame, text="No Caption", variable=self.cbNoCaption_var)
        self.checkbox_15.grid(row=1, column=1, pady=(20, 0), padx=20, sticky="nw")
        self.textbox_2_label = customtkinter.CTkLabel(self.tabview.tab("OpenAI"), text="OpenAI Key: ")
        self.textbox_2_label.grid(row=5, column=0, padx=20, pady=(20, 0), sticky="nw")
        self.textbox_2 = customtkinter.CTkTextbox(self.tabview.tab("OpenAI"), width=self.windowWidth, height=10)
        self.textbox_2.grid(row=5, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        
        self.coming_soon_label = customtkinter.CTkLabel(self.tabview.tab("Free"), text="Coming Soon!!")
        self.coming_soon_label.grid(row=0, column=0, padx=20, pady=(20, 0))
        
        self.error_label = customtkinter.CTkLabel(master=self, text="", text_color='red')
        self.error_label.grid(row=2, column=1, padx=20, pady=(20, 0))        
        self.generate_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Generate", command=self.generate_button_event)
        self.generate_button_1.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # set default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        
    def select_language_event(self, langStr):
        if langStr == "English":
            categories = ['business', 'change', 'character', 'competition', 'education', 'faith', 'freedom', 'friendship', 'future', 'happiness', 'history', 'honor', 'humorous', 'inspirational', 'life', 'love', 'motivational', 'nature', 'politics', 'power-quotes', 'religion', 'science', 'self-help', 'social-justice', 'sports', 'success', 'technology', 'virtue', 'wisdom']
            self.optionmenu_1.configure(values=categories)
            self.optionmenu_1.configure()
        elif langStr == "Hindi":
            categories = ['success', 'love', 'attitude', 'positive', 'motivational']
            self.optionmenu_1.configure(values=categories)
        else:
            print("Error!")
    
    def generate_button_event(self):
        exportFormat = [self.cbSquare_var.get(), self.cbPadded_var.get(), self.cbHorizontal_var.get(), self.cbVertical_var.get(), self.cbCaption_var.get(), self.cbNoCaption_var.get()]
        if self.optionmenu_lang.get()  == "" or self.optionmenu_1.get() == "" or self.optionmenu_2.get() == "":
            self.error_label.configure(text="Please select a language, category and art style.")
        elif exportFormat[4:6] == ['0' , '0'] or exportFormat[0:4] == ['0', '0', '0', '0']:
            self.error_label.configure(text="Please check at least one format (Square, Padded, Horizontal, Vertical) and if to superimpose quote as caption on the images.")
        elif self.textbox_2.get("0.0", "end") == "\n":
            self.error_label.configure(text="Please enter API Key.")
        else:
            self.error_label.configure(text="")
            vibe = self.textbox_1.get("0.0", "end")[:-1]
            key = self.textbox_2.get("0.0", "end")[:-1]
            if self.tabview.get() == "OpenAI":
                print("OpenAI")
                GenerateWallpaper(self.category_var.get(), self.artStyle_var.get(), exportFormat, vibe, key, self.optionmenu_lang.get())
            elif self.tabview.get() == "Free":
                print("Free")
                # GenerateWallpaper(self.category_var.get(), self.artStyle_var.get(), exportFormat, vibe, key, 'hindi')
            else:
                print("Error")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

if __name__ == "__main__":
    app = App()
    app.mainloop()
