__author__ = 'Aaron'


class TrialData:
    def __init__(self, type=None, adjective1=None, adjective2=None, trial_pos = None,
                 prompt="this item is...", stimuli=None, responseList=None, trialID=None, adjective_type = None):
        self.type = type
        self.adjective1 = adjective1
        self.adjective2 = adjective2
        #newline character added to separate prompt from picture during presentation
        self.prompt = prompt+'\n'
        self.stimuli = stimuli
        self.image_scale_pos_list = None
        self.responseList = responseList
        self.trialID = None
        self.adjective_type = None
        self.trial_pos = None

    def getTrial_pos_list(self):
        return self.image_scale_pos_list

    def setType(self, newType):
        """
        :param newType:
        change the trial type (isolated, grouped, etc.) for the given trial
        """
        self.type = newType

    def getType(self):
        return self.type

    def getAdjective1(self):
        return self.adjective1

    def getAdjective2(self):
        return self.adjective2

    def getPrompt(self):
        return self.prompt

    def getStimuli(self):
        return self.stimuli

    def getResponses(self):
        return self.responseList

    def getTrialID(self):
        return self.trialID

    def setAdjective1(self, newAdjective):
        """
        change the first adjective (if there is one)
        :param newAdjective:
        """
        self.adjective1 = newAdjective

    def setAdjective2(self, newAdjective):
        self.adjective2 = newAdjective

    def setStimuli(self, newStimuli):
        """
        change the header (text at the top of the screen)
        :param newStimuli:
        """
        self.stimuli = newStimuli

    def setPrompt(self, newPrompt):
        self.prompt = newPrompt

    def setResponses(self, responses):
        self.responseList = responses

    def setTrialID(self, newTrialID):
        self.trialID = newTrialID

    def stimuliLength(self):
        """
        returns the length of the stimuli list for the trial
        :return: an int, representing the number of stimuli presented
        """
        return len(self.stimuli)