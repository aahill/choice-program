import Tkinter as Tk
from PIL import Image, ImageTk


class SpecifiedStimulus(Tk.Frame):
    """
    @param: image, a filename
    @param: master, the call to the Tkinter root
    @param: index, the vertical column to format widgets to.
    NOTE: index also performs as the stimulus' ID number for data storage
    """
    def __init__(self, image, master, column_index, row_index, adjective1, adjective2):
        """
        :param image: a filename for the stimulus
        :param master: a Tk master/root object
        :param column_index: the virtical column to format widgets to
        :param adjective1: the first adjective to be presented as a radio button below the stimulus
        :param adjective2: the second adjective to be presented as a radio button below the stimulus
        """
        Tk.Frame.__init__(self, master)
        self.image = image
        self.master = master
        self.column_index = column_index
        self.row_index = row_index
        self.adjective1 = adjective1
        self.adjective2 = adjective2
        self.response = None
        self.scale_pos = self.get_scale_pos()
        self.v = Tk.IntVar()
        #Tkinter only supports .gif format. Must use PIL to convert jpg files
        #to a readable format
        self.tkImage = ImageTk.PhotoImage(Image.open(self.image))
        # make new label for the picture, and store it
        self.label = Tk.Label(self.master, image=self.tkImage)
        self.label.image = self.tkImage
        #button definitions
        self.yesButton = Tk.Radiobutton(self.master,
                                        text=self.adjective1,
                                        padx=20,
                                        val=1,
                                        variable=self.v,
                                        command=lambda: self.set_response(1),
                                        anchor='e',
                                        background='white')

        self.noButton = Tk.Radiobutton(self.master,
                                       text=self.adjective2,
                                       padx=20,
                                       val=0,
                                       variable=self.v,
                                       command=lambda: self.set_response(2),
                                       anchor='e',
                                       background='white')

        self.neitherButton = Tk.Radiobutton(self.master,
                                            text="neither %s or %s" % (self.adjective1, self.adjective2),
                                            padx=20,
                                            val=3,
                                            variable=self.v,
                                            command=lambda: self.set_response(3),
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
        frame = Tk.Frame(self.master, bd=16, relief='sunken', background='white')
        frame.grid()
        #set variable to None so no radio buttons are selected
        self.v.set(None)
        self.v.set(None)
        #using Tkinter layout grid manager
        #start at row_index+1 to leave space for prompt
        self.label.grid(row=self.row_index, column=self.column_index)
        self.yesButton.grid(row=self.row_index+1, column=self.column_index)
        self.noButton.grid(row=self.row_index+2, column=self.column_index)
        self.neitherButton.grid(row=self.row_index+3, column=self.column_index)

    def set_response(self, newResponse):
        self.response = newResponse