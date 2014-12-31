__author__ = 'Aaron'

import Tkinter
from PIL import Image, ImageTk


class YesNoStimulus(Tkinter.Frame):
    """
    @param: image, a filename
    @param: master, the call to the Tkinter root
    @param: index, the vertical column to format widgets to.
    NOTE: index also performs as the stimulus' ID number for data storage
    """
    def __init__(self, image, master, index, adjective1):
        Tkinter.Frame.__init__(self, master)
        self.image = image
        self.master = master
        self.index = index
        self.adjective1 = adjective1
        self.response = None
        self.scale_pos = self.get_scale_pos()
        #stores the user's response as an integer
        self.v = Tkinter.IntVar()

        #Tkinter only supports .gif format. Must use PIL to convert jpg files
        #to a readable format
        self.tkImage = ImageTk.PhotoImage(Image.open(self.image))

        # make new label for the picture, and store it
        self.label = Tkinter.Label(self.master, image=self.tkImage)
        self.label.image = self.tkImage
        self.label.configure(background='white')
        #label for context question
        self.question = Tkinter.Label(self.master,
                                      text='this item is %s:' % self.adjective1,
                                      padx=20,
                                      background='white')

        #button definitions
        self.yesButton = Tkinter.Radiobutton(self.master,
                                             text='yes',
                                             padx=20,
                                             val=1,
                                             variable=self.v,
                                             command=lambda: self.set_response(1),
                                             anchor='e',
                                             background='white')

        self.noButton = Tkinter.Radiobutton(self.master,
                                            text='no',
                                            padx=20,
                                            val=0,
                                            variable=self.v,
                                            command=lambda: self.set_response(2),
                                            anchor='e',
                                            background='white')
        self.construct()

    def get_scale_pos(self):
        """
        gets the scale position of the image from the image file
        """
        # take off file extention from image name and get the last character from the resulting string
        last_char = self.image[:-4][-1:]
        if last_char.isdigit():
            self.scale_pos = last_char
        else:
            raise NameError("FILENAMES MUST END WITH A DIGIT. Ex -> 'somepicture5.jpg")

    def construct(self):
        """
        initializes the stimulus object
        """
        #frame to house widgets in
        #outer = Tkinter.Frame(self.master, bd=16, relief='sunken')
        #self.configure(background='white')

        frame = Tkinter.Frame(self.master, bd=16, relief='sunken')
        frame.grid()

        #set variable to None so no radio buttons are selected
        self.v.set(None)
        self.v.set(None)
        #using Tkinter layout grid manager
        self.label.grid(row=1, column=self.index)
        self.question.grid(row=2, column=self.index)
        self.yesButton.grid(row=3, column=self.index)
        self.noButton.grid(row=4, column=self.index)

    # following must be a function to be passed anonymously to the stimulus' radio buttons
    def set_response(self, new_response):
        self.response = new_response