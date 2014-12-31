from TrialData import *
import csv
import os


class DataRecorder:

    def __init__(self):
        """
        initializes a recorder
        """
        #stores the data belonging to the trials
        self.data = []
        #the following store subject information
        self.userAge = None
        self.userNatLang = None
        self.userGender = None
        self.userNumber = None
        #name of the directory (folder) to hold all experiment info
        self.data_directory_name = 'experiment_data'

    def add_data(self, trial_data):
        """
        adds a trial's setup and response data to self.data as a tuple
        :param trial_data: the TrialData object containing the trial's attributes and responses
        """
        assert isinstance(trial_data, TrialData)
        self.data.append(trial_data)

    def find_longest_stimuli_list(self):
        """
        finds the longest list of stimuli in the data set, and returns it.
        Used to format the csv since trials have differing numbers of stimuli.
        :return: an int representing the longest list of stimuli of the list of TrialData objects
        contained in the data set
        """
        longest = 0
        for dataObject in self.data:
            if dataObject.stimuliLength() > longest:
                longest = dataObject.stimuliLength()
        return longest

    def find_duplicate_files(self, filename_to_match):
        """
        determines if there are duplicate file names in the given directory
        :param filename_to_match:
        :return:
        """
        duplicate = False
        directory_files = os.listdir(self.data_directory_name)
        for f in directory_files:
            if filename_to_match == f:
                duplicate = True
        return duplicate

    def ensure_directory(self):
        """
        checks to see if a folder has been created in the current working directory to hold subject data.
        if there is no folder created, the program will create one
        :return: a folder named 'subject_data' will be created in the current working directory
        """
        #check if 'subject_data' exists as a folder
        if not os.path.isdir(self.data_directory_name):
            try:
                #if not, try to make the folder
                os.makedirs(self.data_directory_name)
            except OSError:
                #The folder might have been made due to a Race condition since the last check
                if os.path.exists(self.data_directory_name):
                    pass
                else:
                    #otherwise, the folder couldn't be created due to permission problems, full-disk, etc.
                    raise OSError("cannot create folder for unknown reason. May be permission problems, or full disk.")

    def make_filename(self):
        #used in case of duplicate file names; a number will be appended to the file name to avoid file name conflicts
        duplicate_num = 0
        data_filename = "subject %s results.csv" % self.userNumber
        #loop until valid filename is found
        while True:
            if self.find_duplicate_files(data_filename):
                duplicate_num += 1
                data_filename = "subject %s_%s results.csv" % (self.userNumber, duplicate_num)
            else:
                return data_filename

    def write_to_file(self):
        self.ensure_directory()
        data_filename = self.make_filename()

        with open(os.path.join(os.getcwd(), self.data_directory_name, data_filename), "wb") as newFile:
            out = csv.writer(newFile, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)

            #data for writing subject info to file
            subject_data_header = ['ID', 'age', 'gender', 'Native language']
            subject_data = [self.userNumber, self.userAge, self.userGender, self.userNatLang]
            assert len(subject_data_header) == len(subject_data)

            #data header for writing to file
            trial_data_header = ['Trial pos', 'Trial ID', 'scene type', 'Adjective1', 'Adjective2', 'adjective type',
                                 'prompt'] + (
                # write this multiple times, to match the length of the longest stimuli
                ['stimulus file', 'scale pos', 'response'] * self.find_longest_stimuli_list())

            #separator equal to the length of the header, for writing the trial data separate from the user data
            separator = ['' for _ in range(len(subject_data_header))]

            out.writerow(subject_data_header+trial_data_header)
            out.writerow(subject_data)
            #write trial results
            for trial in self.data:
                #compile stimuli and their respective responses into one list
                zipped = zip(trial.getStimuli(), trial.getTrial_pos_list(), trial.getResponses())
                #flatten zipped into a single list for concatenation
                flattened = [item for sublist in zipped for item in sublist]
                out.writerow(separator + [trial.trial_pos, trial.getTrialID(), trial.getType(), trial.getAdjective1(),
                                          trial.getAdjective2(), trial.adjective_type, trial.getPrompt()] + flattened)
            newFile.flush()
            newFile.close()
