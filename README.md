choice-program
==============

This survey program tests and records the adjectives the user associates with a series of images. 

Images are presented either in groups or as isolated single images and prompts the user to click on a 
radio button corresponding to one of two different adjectives relating to the image. 

A 'trial' consists of a file located in a internal directory, and consists of:

  - 1 or more images to be presented on the screen at one time
  - a .txt file named "attributes" containing the following
    - "adjective 1": the adjective to be given to the first radio button of each image
    - "adjective 2": the adjective to be given to the second radio button of each image
    - "type": the 'trial type', which is described below. The current types are "isolated", "grouped", "relatived"
    - "trialid": the trial's ordering in a list of trials (i.e. 1 corresponds to the first trial, 2 corresponds to the second, etc.)
    


This program scans all internal directories for these trial folders. Their specific presentation on screen depends 
mostly on the trial's specific type.

*~to be updated~*
