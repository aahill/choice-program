__author__ = 'Aaron'

import Tkinter as Tk
from YesNoStimulus import YesNoStimulus


class ContextScene(Tk.Toplevel):

    def __init__(self, setup_data, recorder, *args, **kwargs):
        """
        :param setup_data: a TrialData object containing all necessary info to run the trial
        :param recorder: a DataRecorder object that will store the results of the trial
        """
        Tk.Toplevel.__init__(self, *args, **kwargs)
        self.recorder = recorder
        self.setupData = setup_data
        #the list of images to process into stimuli
        self.imageList = setup_data.stimuli
        assert len(self.imageList) > 0
        #question to be posed to subject
        self.prompt = setup_data.prompt
        #adjective to be tested
        self.adjective1 = setup_data.adjective1
        assert not self.adjective1 is None, "missing adjective 1"
        #will store the stimulus objects after initialization
        self.stimulusObjects = []
        #will store user responses
        self.initialize()

    def initialize(self):
        """
        sets up and creates a grouped scene
        """
        #window settings
        self.overrideredirect(1)
        self.wm_attributes("-topmost", 1)
        self.configure(background='white')

        frame = Tk.Frame(self, bd=16, relief='sunken')
        frame.grid()

        #the prompt presented as a label
        Tk.Label(self,
                 text=self.prompt,
                 font=("Helvetica", 13),
                 wraplength=400,
                 justify="left",
                 anchor="w",
                 background='white',
                 padx=20).grid(row=0, column=(len(self.imageList)-1)/2)

        isolated_stimulus = YesNoStimulus(self.imageList[0], self, 0, self.adjective1)

        end_button = Tk.Button(self, text="continue",
                               command=lambda: self.quit_trial(isolated_stimulus))
        end_button.grid(row=5)

        #CODE TO CENTER WINDOW ON SCREEN
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

    def quit_trial(self, stimulus):
        """
        gathers responses from stimulus objects and checks to ensure a selection was made for each
        :return:
        """
        #response wrapped in list for standardized data processing
        response = [stimulus.response]
        if not None in response:
            self.setupData.responseList = response
            self.recorder.add_data(self.setupData)
            self.destroy()
        else:
            pass