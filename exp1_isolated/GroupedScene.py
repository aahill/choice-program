import Tkinter as Tk
#import os,random,Tkinter
#from PIL import Image, ImageTk
from SpecifiedStimulus import SpecifiedStimulus
#from DataRecorder import *
from PIL import Image


class GroupedScene(Tk.Toplevel):

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
        assert len(self.imageList) > 0, "the number of images must be greater then 0"
        #question to be posed to subject
        self.prompt = setup_data.prompt
        self.adjective1 = setup_data.adjective1
        assert not self.adjective1 is None, "missing adjective 1"
        self.adjective2 = setup_data.adjective2
        assert not self.adjective2 is None, "missing adjective 2"
        #will store the stimulus objects after initialization
        self.stimulusObjects = []
        #will store user responses
        self.initialize()

    def initialize(self):
        """
        sets up and creates a grouped scene
        """
        self.overrideredirect(1)
        self.wm_attributes("-topmost", 1)
        self.configure(background='white')

        frame = Tk.Frame(self, bd=16, relief='sunken')
        frame.grid()

        #the prompt presented as a label
        Tk.Label(self,
                 text=self.prompt,
                 justify="left",
                 padx=20,
                 background='white').grid(row=0, column=0)
        column_index = 0
        row_index = 1
        curr_row_img_width = 0
        for img in self.imageList:
            curr_row_img_width += Image.open(img).size[0]
            if curr_row_img_width > self.winfo_screenwidth():
                row_index += 4
                curr_row_img_width = 0
                column_index = 0
            new_stimulus = SpecifiedStimulus(img, self, column_index, row_index, self.adjective1, self.adjective2)
            self.stimulusObjects.append(new_stimulus)
            column_index += 1

        end_button = Tk.Button(self, text="continue",
                               command=lambda: self.quit_trial())
        # each stimulus object takes 4 rows, end button to be placed at the very bottom
        end_button.grid(row=(row_index*4)+1)

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

    def quit_trial(self):
        """
        gathers responses from stimulus objects and checks to ensure a selection was made for each
        :return:
        """
        responses = []
        for stimulusObject in self.stimulusObjects:
            responses.append(stimulusObject.response)
        assert len(responses) == len(self.stimulusObjects), """the number of responses does not match
        the number of stimulus objects"""
        if not None in responses:
            self.setupData.responseList = responses
            self.recorder.add_data(self.setupData)
            self.destroy()
        else:
            pass