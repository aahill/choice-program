import Tkinter as Tk


class Intro(Tk.Toplevel):
    def __init__(self, data_recorder, *args, **kwargs):
        Tk.Toplevel.__init__(self, *args, **kwargs)
        #self.master = Tk.Tk()
        self.frame = Tk.Frame(bd=16, relief='sunken')
        self.natLangVar = Tk.StringVar()
        self.ageVar = Tk.StringVar()
        self.genderVar = Tk.StringVar()
        self.userNumberVar = Tk.StringVar()
        self.data_recorder = data_recorder
        self.initialize()

    def initialize(self):
        """
        sets up and creates an introduction
        :type self: an intro Tkinter window
        """

        self.overrideredirect(1)
        self.wm_attributes("-topmost", 1)
        self.configure(background='white')

        #message definitions
        message1 = Tk.Label(self,
                            text="For each image shown, indicate which of the 3 provided categories",
                            font="arial",
                            justify="center",
                            anchor="center",
                            padx=20,
                            background='white')

        message2 = Tk.Label(self,
                            text="the image falls into.\n",
                            font="arial",
                            justify="center",
                            anchor="center",
                            padx=20,
                            background='white')

        message3 = Tk.Label(self,
                            text="PLEASE NOTE: you must complete every item, and fill in info below\n",
                            font="arial",
                            justify="center",
                            anchor="center",
                            padx=20,
                            background='white')

        subject_num_prompt = Tk.Label(self,
                                      text="Enter the subject number",
                                      font="arial",
                                      justify="center",
                                      anchor="center",
                                      padx=20,
                                      background='white')

        lang_prompt = Tk.Label(self,
                               text="\n enter your native language",
                               font="arial",
                               justify="left",
                               padx=20,
                               background='white')

        age_prompt = Tk.Label(self,
                              text="\n enter your age as a number",
                              font="arial",
                              justify="left",
                              padx=20,
                              background='white')

        gender_prompt = Tk.Label(self,
                                 text="\n enter your gender",
                                 font="arial",
                                 justify="left",
                                 padx=20,
                                 background='white')

        #entry/button definitions
        native_lang = Tk.Entry(self, textvariable=self.natLangVar)
        user_age = Tk.Entry(self, textvariable=self.ageVar)
        user_gender = Tk.Entry(self, textvariable=self.genderVar)
        user_number = Tk.Entry(self, textvariable=self.userNumberVar)
        end_button = Tk.Button(self, text="next",
                               command=lambda: self.quit_intro(
                                   self.natLangVar.get(),
                                   self.genderVar.get(),
                                   self.ageVar.get(),
                                   self.userNumberVar.get()))
        #grid settings
        message1.grid(row=1, column=0, sticky='w')
        message2.grid(row=2, column=0, sticky='w')
        message3.grid(row=3, column=0, sticky='w')
        subject_num_prompt.grid(row=4, column=0, sticky='w')
        user_number.grid(row=5, column=0, sticky='w')
        lang_prompt.grid(row=6, column=0, sticky='w')
        native_lang.grid(row=7, column=0, sticky='w')
        age_prompt.grid(row=8, column=0, sticky='w')
        user_age.grid(row=9, column=0, sticky='w')
        gender_prompt.grid(row=10, column=0, sticky='w')
        user_gender.grid(row=11, column=0, sticky='w')
        end_button.grid(row=12)

        #CODE TO CENTER WINDOW ON SCREEN
        self.withdraw()
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        master_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        master_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - master_width // 2
        y = self.winfo_screenheight() // 2 - master_height // 2
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        if self.attributes('-alpha') == 0:
            self.attributes('-alpha', 1.0)
        self.deiconify()

    def quit_intro(self, nat_lang_var, gender_var, age_var, user_number_var):
        try:
            if (not nat_lang_var == "" and
                    not gender_var == "" and
                    isinstance(int(age_var), (int, long))and
                    isinstance(int(user_number_var), (int, long))):
                self.data_recorder.userAge = age_var
                self.data_recorder.userNumber = user_number_var
                self.data_recorder.userNatLang = nat_lang_var
                self.data_recorder.userGender = gender_var
                self.destroy()

        except ValueError:
            pass