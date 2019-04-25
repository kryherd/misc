#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PsychoPy experiment by Kayleigh Ryherd, last updated 4/24/2019
"""

### IMPORTANT:
### Under psychopy preferences/general
### (1) change the audio driver to "portaudio" (otherwise the program won't stop running when it's done)
### (2) change the audio library to "pygame" (otherwise the audio won't stop playing when the video stops)

# import psychopy modules
import psychopy
from psychopy import visual, core, event, sound, gui, data, logging
from psychopy.sound import Sound
import math
import numpy as np 
import random
import pandas as pd

# create dialog to enter subject information
myDlg = gui.Dlg(title="HeARS")
myDlg.addField('ID Number:')
myDlg.addField('Computer Type:', choices=["PC", "Mac"])
myDlg.addField('Experiment Type:', choices=["Full", "Clipped"])
myDlg.show()#show dialog and wait for OK or Cancel
if gui.OK:#then the user pressed OK
    info = myDlg.data
else: 
    print 'user cancelled'

# create variables based on dialog
subject = info[0]
computer = info[1]
exp_type = info[2]

# Mac/PC filepaths are different
if computer == "PC":
    slash = "\\"
elif computer == "Mac":
    slash = "/"
else:
    print("error in computer selection")
    core.quit()

#set parent directory
parent_dir = "." + slash

# select stim type
if exp_type == 'Full':
    stim_length = ".csv"
elif exp_type == 'Clipped':
    stim_length = "_clip.csv"
else:
    print("error in exp type selection")
    core.quit()

#### EXPERIMENT SETUP
#set log prefixes
prefix = 'sub-%s' % (subject)
#logging data 
errorLog=logging.LogFile(parent_dir + "results" + slash + prefix + "_errorlog.log", level=logging.DATA, filemode='w')

# function for keypress
def get_keypress():
    keys = event.getKeys(timeStamped=globalClock)
    # if escape was pressed...
    if keys and keys[0][0] == 'escape':
        # save the data in a modified format named "early_quit"
        np.savetxt(parent_dir + "results" + slash + "early_quit_" + prefix + ".tsv", data, fmt='%s', delimiter='\t', newline='\n', header='', footer='', comments='# ')
        # and exit
        win.close()
        core.quit()
    # otherwise, return the keypress object
    elif keys:
        return keys
    # if no keys were pressed, return None
    else:
        return None

#create clock
globalClock = core.Clock()
logging.setDefaultClock(globalClock)

#info about the screen
# change to match your resolution
win = visual.Window(size = [1440,900],
                    color = "white",
                    fullscr = True, allowGUI=False,
                    units = "pix")

############################# 4AFC TASK

# set up text windows
instruct_txt = visual.TextStim(win, text = "Today you will hear some words and see some pictures. \n \nPress the button that for the picture that matches the word you hear. \n \nPress SPACE to continue." ,
                        pos = [0.0,0.0],
                        color = "black",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)
                        

instruct_txt2 = visual.TextStim(win, text = "Use the 4 arrow keys to pick a picture. \n \nLet's practice! \n \nPress SPACE to continue." ,
                        pos = [0.0,0.0],
                        color = "black",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

instruct_txt3 = visual.TextStim(win, text = "Now we're going to do some more. \n \nListen carefully! \n \nPress SPACE to continue." ,
                        pos = [0.0,0.0],
                        color = "black",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

prac_correct = visual.TextStim(win, text = "Correct!" ,
                        pos = [0.0,0.0],
                        color = "black",
                        height = 48,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

prac_incorrect = visual.TextStim(win, text = "Incorrect" ,
                        pos = [0.0,0.0],
                        color = "black",
                        height = 48,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

prac_slow = visual.TextStim(win, text = "Too Slow" ,
                        pos = [0.0,0.0],
                        color = "black",
                        height = 48,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

FinalThankYou_txt = visual.TextStim(win, text = "Thank you!",
                        pos = [0.0,0.0],
                        color = "black",
                        height = 50,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        autoLog=True)

# header for data log
data = np.hstack(("Subject", "StimType", "Trial", "Sound","SpeakerGender", "TargetImage", "Foil1", "Foil2", "Foil3", "CorImgLoc", "RespKey","ACC", "RT"))

# set positions for images
positions = [[0.0, -250], [0.0, 250], [-400, 0.0], [400, 0.0]]
directions = {"[0.0, -250]": "down", "[0.0, 250]": "up", "[-400, 0.0]": "left", "[400, 0.0]": "right"}
# create indices for randomizing image placement
indices = [0, 1, 2, 3]

# create gender
gender = ["Male", "Female"]

##### RUN EXPERIMENT
# time when experiment started
t0 = globalClock.getTime()
# show the instructions
instruct_txt.draw()
win.flip()
# when space is pressed...
keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
# go to the next instruction
instruct_txt2.draw()
win.flip()
# when space is pressed, move on to practice
keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
### PRACTICE TRIALS
PRACTICE_LIST = psychopy.data.importConditions(fileName = parent_dir + "stim" + slash + "practice_stim.csv")
PRACTICE_LIST_RAND = PRACTICE_LIST
random.shuffle(PRACTICE_LIST_RAND)
Trial = 0
# run through practice trials
for index in range(len(PRACTICE_LIST_RAND)):
    # randomize location of images
    random.shuffle(indices)
    targpos = positions[indices[0]]
    foil1pos = positions[indices[1]]
    foil2pos = positions[indices[2]]
    foil3pos = positions[indices[3]]
    CorImgPos = directions[''.join(str(targpos))]
    # set up image stimuli
    img1 = visual.ImageStim(win, pos = targpos,
                size = [300,300], image = parent_dir + "pictures" + slash + PRACTICE_LIST_RAND[index]['TargetImage'] + ".jpg")
    img2 = visual.ImageStim(win, pos = foil1pos,
                size = [300,300], image = parent_dir + "pictures" + slash + PRACTICE_LIST_RAND[index]['Foil1'] + ".jpg")
    img3 = visual.ImageStim(win, pos = foil2pos,
                size = [300,300], image = parent_dir + "pictures" + slash + PRACTICE_LIST_RAND[index]['Foil2'] + ".jpg")
    img4 = visual.ImageStim(win, pos = foil3pos,
                size = [300,300], image = parent_dir + "pictures" + slash + PRACTICE_LIST_RAND[index]['Foil3'] + ".jpg")
    # randomize gender
    random.shuffle(gender)
    gender_trial = gender[0]
    # set up sound 
    trial_sound = sound.Sound(parent_dir + "audio" + slash + PRACTICE_LIST_RAND[index]['StimType'] +  slash + gender_trial + slash + PRACTICE_LIST_RAND[index]['Sound'] + ".wav")
    # draw images
    img1.draw()
    img2.draw()
    img3.draw()
    img4.draw()
    # show screen
    trial_sound.play()
    win.flip()
    # timestamp right as images show up
    t1 = globalClock.getTime()
    while globalClock.getTime() - t1 < 5:
        KEY = get_keypress()
        # if a key was pressed
        if KEY != None:
            RESP = KEY[0][0] # save key that was pressed
            RT = KEY[0][1] - t1 # calculate RT
            break
        # if nothing was pressed
    if KEY == None:
        RESP = 'none'
        RT = 999
    # calculate accuracy
    if RESP == CorImgPos:
        ACC = 1
        prac_correct.draw()
        win.flip()
        core.wait(0.5)
    elif RESP == 'none':
        ACC = 0
        prac_slow.draw()
        win.flip()
        core.wait(0.5)
    else:
        ACC = 0
        prac_incorrect.draw()
        win.flip()
        core.wait(0.5)
    Trial = Trial + 1
    # save data
    data = np.vstack((data, np.hstack((subject,
    PRACTICE_LIST_RAND[index]['StimType'],
    Trial,
    PRACTICE_LIST_RAND[index]['Sound'],
    gender_trial,
    PRACTICE_LIST_RAND[index]['TargetImage'],
    PRACTICE_LIST_RAND[index]['Foil1'],
    PRACTICE_LIST_RAND[index]['Foil2'],
    PRACTICE_LIST_RAND[index]['Foil3'],
    CorImgPos, 
    RESP,
    ACC,
    "%.3f" %RT))))
instruct_txt3.draw()
win.flip()
# when space is pressed, move on to the actual task
keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
### EXPERIMENTAL TRIALS
# load in trials and randomize them
TRIAL_LIST = psychopy.data.importConditions(fileName = parent_dir + "stim" + slash + "stim_list" + stim_length)
TRIAL_LIST_RAND = TRIAL_LIST
random.shuffle(TRIAL_LIST_RAND)
# set trial counter
Trial = 0
# run through trials
for index in range(len(TRIAL_LIST_RAND)):
    # randomize location of images
    random.shuffle(indices)
    targpos = positions[indices[0]]
    foil1pos = positions[indices[1]]
    foil2pos = positions[indices[2]]
    foil3pos = positions[indices[3]]
    CorImgPos = directions[''.join(str(targpos))]
    # set up image stimuli
    img1 = visual.ImageStim(win, pos = targpos,
                size = [300,300], image = parent_dir + "pictures" + slash + TRIAL_LIST_RAND[index]['TargetImage'] + ".jpg")
    img2 = visual.ImageStim(win, pos = foil1pos,
                size = [300,300], image = parent_dir + "pictures" + slash + TRIAL_LIST_RAND[index]['Foil1'] + ".jpg")
    img3 = visual.ImageStim(win, pos = foil2pos,
                size = [300,300], image = parent_dir + "pictures" + slash + TRIAL_LIST_RAND[index]['Foil2'] + ".jpg")
    img4 = visual.ImageStim(win, pos = foil3pos,
                size = [300,300], image = parent_dir + "pictures" + slash + TRIAL_LIST_RAND[index]['Foil3'] + ".jpg")
    # randomize gender
    random.shuffle(gender)
    gender_trial = gender[0]
    # set up sound 
    trial_sound = sound.Sound(parent_dir + "audio" + slash + TRIAL_LIST_RAND[index]['StimType'] + slash + gender_trial + slash + TRIAL_LIST_RAND[index]['Sound'] + ".wav")
    # draw images
    img1.draw()
    img2.draw()
    img3.draw()
    img4.draw()
    # show screen
    trial_sound.play()
    win.flip()
    # timestamp right as images show up
    t1 = globalClock.getTime()
    while globalClock.getTime() - t1 < 5:
        KEY = get_keypress()
        # if a key was pressed
        if KEY != None:
            RESP = KEY[0][0] # save key that was pressed
            RT = KEY[0][1] - t1 # calculate RT
            break
    # if nothing was pressed
    if KEY == None:
        RESP = 'none'
        RT = 999
    # calculate accuracy
    if RESP == CorImgPos:
        ACC = 1
    else:
        ACC = 0
    Trial = Trial + 1
    win.flip()
    core.wait(0.25)
    # save data
    data = np.vstack((data, np.hstack((subject,
    TRIAL_LIST_RAND[index]['StimType'],
    Trial,
    TRIAL_LIST_RAND[index]['Sound'],
    gender_trial,
    TRIAL_LIST_RAND[index]['TargetImage'],
    TRIAL_LIST_RAND[index]['Foil1'],
    TRIAL_LIST_RAND[index]['Foil2'],
    TRIAL_LIST_RAND[index]['Foil3'],
    CorImgPos, 
    RESP,
    ACC,
    "%.3f" %RT))))

# save results document
np.savetxt(parent_dir + "results" + slash + "HeARS_" + prefix + ".tsv", data, fmt='%s', delimiter='\t', newline='\n', header='', footer='', comments='# ')

#display a Thank You message
FinalThankYou_txt.draw()
win.flip()
core.wait(2)
win.flip()

# close everything
win.close()
core.quit()