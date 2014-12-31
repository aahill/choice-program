import os
import random
from Intro import Intro
from GroupedScene import *
from DataRecorder import DataRecorder
from TrialData import *
from IsolatedScene import IsolatedScene
from ContextScene import ContextScene


class Experiment:

    def __init__(self):
        self.master = Tk.Tk()
        self.curr_trial = 0
        self.trial_list = self.get_trial_data()
        self.canvasWidth = self.master.winfo_screenwidth()
        self.canvasHeight = self.master.winfo_screenheight()
        self.master.overrideredirect(1)
        self.master.geometry("%dx%d+0+0" % (self.canvasWidth, self.canvasHeight))
        self.master.focus_set()  # <-- move focus to this widget
        #quit button
        self.master.bind("<Escape>", lambda _: self.master.destroy())
        self.canvas = Tk.Canvas(self.master,
                                width=self.canvasWidth,
                                height=self.canvasHeight,
                                background='white')
        self.canvas.pack()
        self.main()

    def get_trial_data(self):
        """
        retrieves all JPEG and PNG pictures from all subdirectories relative to the
        script, as well as an attributes file that *MUST* be .txt
        :return a trialData object, which contains the attributes for a trial
        """
        #The path to the images - currently set to the current working directory (where you're running the script from)
        directory = os.getcwd()
        trial_list = []
        #find subdirectories, then delete root folder
        subdirectories = [x[0] for x in os.walk(directory)]
        del subdirectories[0]
        assert len(subdirectories) > 0, "there were no subdirectories found"

        for directory in subdirectories:
            if 'trial'in directory: #directory.lower().startswith("trial"): #[-6:-1].startswith("trial"):
                directory_images = []
                image_scale_pos_list = []
                trial_data = TrialData()
                for file_path in os.listdir(directory):
                    #normalize filenames to lower case, check for .jpg or .png extension
                    if file_path.lower().endswith(".jpg") or file_path.lower().endswith(".png"):
                        #If the file is a jpg or png, add it to our list of images
                        #directory_images.append(directory+'\\'+file_path)
                        directory_images.append(os.path.join(directory, file_path))    # <-- OS INDEPENDENT

                        #get image scale position
                        #print file_path
                        last_char = file_path[:-4][-1:]
                        #print last_char
                        if last_char.isdigit():
                            image_scale_pos_list.append(last_char)
                        else:
                            raise NameError("FILENAMES MUST END WITH A DIGIT. Ex -> 'somepicture5.jpg")

                    ##PARSE TEXT FILE
                    if file_path.lower().endswith(".txt"):
                        with open(os.path.join(directory, file_path), 'r') as trialAttributes:
                            for line in trialAttributes:
                                #remove whitespace from line
                                normed = "".join(line.lower().split())
                                if normed[:11] == "adjective1=":
                                    #trial_data.setAdjective1(normed[11:])
                                    trial_data.adjective1 = normed[11:]
                                elif normed[:11] == 'adjective2=':
                                    #trial_data.setAdjective2(normed[11:])
                                    trial_data.adjective2 = normed[11:]
                                elif normed[:5] == 'type=':
                                    #trial_data.setType(normed[5:])
                                    trial_data.type = normed[5:]
                                elif normed[:7] == 'prompt=':
                                    #extract non-normalized prompt
                                    for i in range(len(line)):
                                        if line[i] == '=':
                                            #trial_data.setPrompt(line[i+1:])
                                            trial_data.prompt = line[i+1:]
                                elif normed[:8] == 'trialid=':
                                    #trial_data.setTrialID(normed[8:])
                                    trial_data.trialID = normed[8:]
                                elif normed[:14] == 'adjectivetype=':
                                    # adjective type must be either relative, absolute, or filler
                                    if normed[14:] not in ['relative', 'absolute', 'filler']:
                                        raise IOError("""adjective type must be one of the following:
                                        relative, absolute, or filler""")
                                    else:
                                        trial_data.adjective_type = normed[14:]
                                else:
                                    if normed == "":
                                        pass
                                    else:
                                        print "Unexpected line in instruction text, as shown below. please revise"
                                        print normed
                                        #raise TypeError

                trial_data.setStimuli(directory_images)
                trial_data.image_scale_pos_list = image_scale_pos_list
                #assertions to ensure all necessary data was collected, with appropriate error messages
                assert trial_data.type is not None, """
                NO TRIAL TYPE WAS SPECIFIED IN THE FILE
                ENSURE ALL LINES ARE SPELLED CORRECTLY IN THE FILE. USE \'type=\'(without quotes)
                FOLLOWED BY ANY OF THE FOLLOWING (WITHOUT QUOTES): \'isolated\', \'grouped\', \'context\'
                """
                assert trial_data.trialID is not None, """
                NO TRIAL ID WAS SPECIFIED IN THE FILE
                ENSURE ALL LINES ARE SPELLED CORRECTLY IN THE FILE. USE \'TrialId=\' (without quotes)
                FOLLOWED BY A NUMBER
                """
                assert trial_data.adjective1 is not None, """
                NO ADJECTIVE1 WAS SPECIFIED IN THE FILE
                ENSURE ALL LINES ARE SPELLED CORRECTLY IN THE FILE. USE \'adjective1=\' (without quotes)
                FOLLOWED BY AN ADJECTIVE. AT LEAST ONE ADJECTIVE MUST BE DEFINED FOR EACH TRIAL
                """
                trial_list.append(trial_data)


        #Randomize our image sets - NOTE: IS THIS WORKING?
        random.shuffle(trial_list)
        return trial_list

    def main(self):
        """
        initiates the experiment
        """

        trial_data = self.get_trial_data()
        #if no trials were found while scanning the folders, raise an error
        if len(trial_data) == 0:
            raise IOError("no trial setup data was gathered")
        trial_recorder = DataRecorder()
        #intro = Intro(trial_recorder)
        trial_counter = 1
        #wait for the intro to close before continuing
        #self.master.wait_window(intro)
        #for every trial found, determine its trial type, display the appropriate window
        for trialSetupData in trial_data:
            trialSetupData.trial_pos = trial_counter
            trial_counter += 1
            win = None
            trial_type = str(trialSetupData.type).lower()
            if trial_type == 'grouped':
                win = GroupedScene(trialSetupData, trial_recorder, master=self.master)

            elif trial_type == 'isolated':
                win = IsolatedScene(trialSetupData, trial_recorder)
            elif trial_type == 'context':
                win = ContextScene(trialSetupData, trial_recorder)
            self.master.wait_window(win)
        #once all trials are completed, write the data file and close the experiment window
        trial_recorder.write_to_file()
        self.master.destroy()

Experiment()