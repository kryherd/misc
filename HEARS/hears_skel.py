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
myDlg.addField('Order:')
myDlg.addField('Computer Type:', choices=["PC", "Mac"])
myDlg.addField('Experiment Type:', choices=["Full", "Clipped"])
myDlg.show()#show dialog and wait for OK or Cancel
if gui.OK:#then the user pressed OK
    info = myDlg.data
else: 
    print 'user cancelled'

# create variables based on dialog
subject = info[0]
order = int(info[1])
computer = info[2]
exp_type = info[3]

# If the order is not valid, throw an error
if order < 1 or order > 2:
    errordlg = gui.Dlg(title = "Error")
    errordlg.addText("Invalid order selected.")
    errordlg.show()
    core.quit()

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
    stim_length = "stim.csv"
elif exp_type == 'Clipped':
    stim_length = "stim_clip.csv"
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
                    color = "black",
                    fullscr = True, allowGUI=False,
                    units = "pix")

############################# 4AFC TASK

# select block
if order == 1:
    block = {1: "silent", 2: "noise"}
elif order == 2:
    block = {1: "noise", 2: "silent"}
else:
    print("\n-----------\nInvalid Order Selected. Please Try Again.\n-----------\n")
    win.close()
    core.quit()


# set up text windows
instruct_txt = visual.TextStim(win, text = "HERE YOU CAN CHANGE INSTRUCTION TEXT." ,
                        pos = [0.0,0.0],
                        color = "white",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)
                        

instruct_txt2 = visual.TextStim(win, text = "THIS IS INSTRUCTION TEXT PAGE 2." ,
                        pos = [0.0,0.0],
                        color = "white",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

instruct_txt3 = visual.TextStim(win, text = "THIS IS INSTRUCTION TEXT PAGE 3." ,
                        pos = [0.0,0.0],
                        color = "white",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

diff_txt = visual.TextStim(win, text = "THIS IS INSTRUCTION TEXT IN BETWEEN BLOCKS." ,
                        pos = [0.0,0.0],
                        color = "white",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

FinalThankYou_txt = visual.TextStim(win, text = "Thank you!",
                        pos = [0.0,0.0],
                        color = "white",
                        height = 50,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        autoLog=True)

# set up example sounds
ba_redu = sound.Sound(parent_dir + "audio" + slash + "ba_redu_audio.wav")
ba_base = sound.Sound(parent_dir + "audio" + slash + "ba_base_audio.wav")

# header for data log
data = np.hstack(("Subject", "BlockNum", "BlockType", "Trial", "StimType", "Sound","CorImg", "RespImg","ACC", "RT"))

# set positions for images
positions = [[0.0, -250], [0.0, 250], [-400, 0.0], [400, 0.0]]
directions = {"[0.0, -250]": "up", "[0.0, 250]": "down", "[-400, 0.0]": "left", "[400, 0.0]": "right"}
# create indices for randomizing image placement
indices = [0, 1, 2, 3]

##### RUN EXPERIMENT
# time when experiment started
t0 = globalClock.getTime()
# run through the blocks in order
for i in range(1, 3):
    # for the first block, show the instructions
#    if i == 1:
#        instruct_txt.draw()
#        win.flip()
#        # when space is pressed...
#        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
#        # ... play the A sound
#        ba_redu.play()
#        core.wait(2)
#        instruct_txt2.draw()
#        win.flip()
#        # when space is pressed...
#        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
#        # ... play the BA sound
#        ba_base.play()
#        core.wait(2)
#        instruct_txt3.draw()
#        win.flip()
#        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
    # for the other blocks, show the other block instructions  
#    if i > 1:
#        diff_txt.draw()
#        win.flip()
#        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
    # name the block
    blockName = block[i]
    # load in trials and randomize them
    TRIAL_LIST = psychopy.data.importConditions(fileName = parent_dir + "stim" + slash + "%s_" % (blockName) + stim_length)
    totalTrials = len(TRIAL_LIST)
    TRIAL_LIST_RAND = TRIAL_LIST
    random.shuffle(TRIAL_LIST_RAND)
    # set trial counter
    Trial = 0
    # run through trials
    for index in range(len(TRIAL_LIST_RAND)):
        # randomize location of images
        random.shuffle(indices)
        img1pos = positions[indices[0]]
        img2pos = positions[indices[1]]
        img3pos = positions[indices[2]]
        img4pos = positions[indices[3]]
        CorImgPos = directions[''.join(str(positions[indices[TRIAL_LIST_RAND[index]['CorrectImage']-1]]))]
        # set up image stimuli
        img1 = visual.ImageStim(win, pos = img1pos,
                    size = [300,300], image = parent_dir + "pictures" + slash + TRIAL_LIST_RAND[index]['Image1'])
        img2 = visual.ImageStim(win, pos = img2pos,
                    size = [300,300], image = parent_dir + "pictures" + slash + TRIAL_LIST_RAND[index]['Image2'])
        img3 = visual.ImageStim(win, pos = img3pos,
                    size = [300,300], image = parent_dir + "pictures" + slash + TRIAL_LIST_RAND[index]['Image3'])
        img4 = visual.ImageStim(win, pos = img4pos,
                    size = [300,300], image = parent_dir + "pictures" + slash + TRIAL_LIST_RAND[index]['Image4'])
        # timestamp right as images show up
        t1 = globalClock.getTime()
        # draw images
        img1.draw()
        img2.draw()
        img3.draw()
        img4.draw()
        # show screen
        win.flip()
        while globalClock.getTime() - t1 < 10:
            KEY = get_keypress()
            # if a key was pressed
            if KEY != None:
                RESP = KEY[0][0] # save key that was pressed
                RT = KEY[0][1] - t1 # calculate RT
                break
                if RESP == "up":
                    RespImg = 1
                elif RESP == 'j':
                    SOUND = 'BA'
                else:
                    SOUND = 'none'
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
        # save data
        data = np.vstack((data, np.hstack((subject,
        i,
        blockName,
        Trial,
        TRIAL_LIST_RAND[index]['StimType'],
        TRIAL_LIST_RAND[index]['Sound'],
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