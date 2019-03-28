#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PsychoPy experiment by Kayleigh Ryherd, last updated 12/11/2018
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

myDlg = gui.Dlg(title="AV Int")
myDlg.addField('ID Number:')
myDlg.addField('Order:')
myDlg.addField('Computer Type:', choices=["PC", "Mac"])
myDlg.addField('Experiment Type:', choices=["Full", "Clipped"])
myDlg.show()#show dialog and wait for OK or Cancel
if gui.OK:#then the user pressed OK
    info = myDlg.data
else: 
    print 'user cancelled'

subject = info[0]
order = int(info[1])
computer = info[2]
exp_type = info[3]

if order < 1 or order > 6:
    errordlg = gui.Dlg(title = "Error")
    errordlg.addText("Invalid order selected.")
    errordlg.show()
    core.quit()

if computer == "PC":
    slash = "\\"
elif computer == "Mac":
    slash = "/"
else:
    print("error in computer selection")
    core.quit()

#set parent directory
parent_dir = "." + slash

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

# function for getting key presses
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
win = visual.Window(size = [1280,800],
                    color = "black",
                    fullscr = True, allowGUI=False,
                    units = "pix")

############################# 2AFC SECTION

# select block
if order == 1:
    block = {1: "face", 2: "pl", 3: "pix"}
elif order == 2:
    block = {1: "face", 2: "pix", 3: "pl"}
elif order == 3:
    block = {1: "pl", 2: "face", 3: "pix"}
elif order == 4:
    block = {1: "pl", 2: "pix", 3: "face"}
elif order == 5:
    block = {1: "pix", 2: "face", 3: "pl"}
elif order == 6:
    block = {1: "pix", 2: "pl", 3: "face"}
else:
    print("\n-----------\nInvalid Order Selected. Please Try Again.\n-----------\n")
    win.close()
    core.quit()


# set up text windows
instruct_txt = visual.TextStim(win, text = "In this experiment you will be watching videos and hearing sounds.\n\nSometimes you will hear an A.\n\nPress SPACE now to hear an example of A." ,
                        pos = [0.0,0.0],
                        color = "white",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)
                        

instruct_txt2 = visual.TextStim(win, text = "Sometimes you will hear a BA. \n \n \nPress SPACE to hear an example of BA." ,
                        pos = [0.0,0.0],
                        color = "white",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

instruct_txt3 = visual.TextStim(win, text = "Every time you hear A, press F.\n\nEvery time you hear BA, press J. \n \n \nPress SPACE to begin." ,
                        pos = [0.0,0.0],
                        color = "white",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

diff_txt = visual.TextStim(win, text = "Let's try it again with some different videos.\n\nRemember, every time you hear A, press F\nand every time you hear BA, press J. \n \n \nPress SPACE to begin." ,
                        pos = [0.0,0.0],
                        color = "white",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

keypress = visual.TextStim(win,
                            text = "F - A             J - BA",
                            pos = [0.0,-400],
                            color = "white", 
                            height = 32, 
                            alignHoriz='center', 
                            alignVert='center',
                            font = "Arial",
                            autoLog=True,
                            wrapWidth= 1200)

FinalThankYou_txt = visual.TextStim(win, text = "Thank you!",
                        pos = [0.0,0.0],
                        color = "white",
                        height = 50,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        autoLog=True)

test = parent_dir + "audio" + slash + "ba_redu_audio.wav"

print(test)
# set up example sounds
ba_redu = sound.Sound(parent_dir + "audio" + slash + "ba_redu_audio.wav")
ba_base = sound.Sound(parent_dir + "audio" + slash + "ba_base_audio.wav")


# header for data log
data = np.hstack(("Subject", "Block", "Trial", "StimType", "StimCategory","Stimulus", "ACC","RESP","Sound","RT"))


##### RUN EXPERIMENT
# time when experiment started
t0 = globalClock.getTime()
# run through the blocks in order
for i in range(1, 4):
    # for the first block, show the instructions
    if i == 1:
        instruct_txt.draw()
        win.flip()
        # when space is pressed...
        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
        # ... play the A sound
        ba_redu.play()
        core.wait(2)
        instruct_txt2.draw()
        win.flip()
        # when space is pressed...
        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
        # ... play the BA sound
        ba_base.play()
        core.wait(2)
        instruct_txt3.draw()
        win.flip()
        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
    # for the other blocks, show the other block instructions  
    if i > 1:
        diff_txt.draw()
        win.flip()
        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
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
        # set up video stimulus
        mov = visual.MovieStim3(win, parent_dir + 'video' + slash + TRIAL_LIST_RAND[index]['Stimulus'],
                        size = (TRIAL_LIST_RAND[index]['VidWidth'], TRIAL_LIST_RAND[index]['VidHeight']),
                        flipVert = False,
                        flipHoriz = False,
                        loop = False)
        # timestamp right as movie is started
        t1 = globalClock.getTime()
        while mov.status != visual.FINISHED:
            mov.draw()
            keypress.draw()
            win.flip()
        # wait for a half a second
        core.wait(0.5)
        KEY = get_keypress()
        # if a key was pressed
        if KEY != None:
            RESP = KEY[0][0] # save key that was pressed
            RT = KEY[0][1] - t1 # calculate RT
            if RESP == "f":
                SOUND = 'A'
            elif RESP == 'j':
                SOUND = 'BA'
            else:
                SOUND = 'none'
        # if nothing was pressed
        elif KEY == None:
            RESP = 'none'
            SOUND = 'none'
            RT = 999
        # set up and determine accuracy
        if TRIAL_LIST_RAND[index]['StimType'] == 'oddball':
            cor_resp = 'f'
        elif TRIAL_LIST_RAND[index]['StimType'] == 'standard':
            cor_resp = 'j'
        if cor_resp == RESP:
            ACC = 1
        else:
            ACC = 0
        Trial = Trial + 1
        # add trial-level data to numpy array
        data = np.vstack((data, np.hstack((subject,
                i,
                Trial,
                TRIAL_LIST_RAND[index]['StimType'],
                TRIAL_LIST_RAND[index]['StimCategory'],
                TRIAL_LIST_RAND[index]['Stimulus'], 
                ACC,
                RESP,
                SOUND,
                "%.3f" %RT))))

# save results document
np.savetxt(parent_dir + "results" + slash + "AVInt_2AFC_" + prefix + ".tsv", data, fmt='%s', delimiter='\t', newline='\n', header='', footer='', comments='# ')


############################# GOODNESS RATINGS SECTION

# set up text displays
goodness_txt = visual.TextStim(win, text = "Now you will hear and see many sounds and pictures.\n\nAfter each sound, judge how strong the 'b' was.\n\nFor a STRONG 'b', press 1.\n\nFor a MEDIUM 'b', press 2.\n\nFor a WEAK 'b', press 3.\n\nIf you DO NOT hear a 'b', press 4.\n\nPress SPACE to continue." ,
                        pos = [0.0,0.0],
                        color = "white",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

keypress_good = visual.TextStim(win,
                            text = "1 - Strong     2 - Medium    3 - Weak    4 - None",
                            pos = [0.0,-400],
                            color = "white", 
                            height = 32, 
                            alignHoriz='center', 
                            alignVert='center',
                            font = "Arial",
                            autoLog=True,
                            wrapWidth= 1200)

# set up data structure
data = np.hstack(("Subject", "Trial", "StimType", "StimCategory","Stimulus","KEY", "Rating", "RT"))

# start clock
t0 = globalClock.getTime()

#show instructions
goodness_txt.draw()
win.flip()
# when space is pressed, start experiment
keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)

# load in trials and randomize them
TRIAL_LIST = psychopy.data.importConditions(fileName = parent_dir + "stim" + slash + "goodness_" + stim_length)
totalTrials = len(TRIAL_LIST)
TRIAL_LIST_RAND = TRIAL_LIST
random.shuffle(TRIAL_LIST_RAND)
# set trial counter
Trial = 0
# run through trials
for index in range(len(TRIAL_LIST_RAND)):
    # set up video stimulus
    mov = visual.MovieStim3(win, parent_dir + 'video' + slash + TRIAL_LIST_RAND[index]['Stimulus'],
                size = (TRIAL_LIST_RAND[index]['VidWidth'], TRIAL_LIST_RAND[index]['VidHeight']),
                flipVert = False,
                flipHoriz = False,
                loop = False)
    t1 = globalClock.getTime()
    # give participant 10 seconds to respond
    while globalClock.getTime()-t1 <= 10:
        # play movie stimulus
        while mov.status != visual.FINISHED:
            mov.draw()
            keypress_good.draw()
            win.flip()
        # pause movie
        mov.pause()
        KEY = get_keypress()
        # if a key was pressed, move on to next trial
        if KEY != None:
            break
    if KEY != None:
        RESP = KEY[0][0] # save key that was pressed
        RT = KEY[0][1] - t1 # calculate RT
        if RESP == '1':
            RAT = 'Strong'
        elif RESP == '2':
            RAT = 'Medium'
        elif RESP == '3':
            RAT = 'Weak'
        elif RESP == '4':
            RAT = 'No B'
        else:
            RAT = 'No Rating'
    # if nothing was pressed
    elif KEY == None:
        RESP = 'none'
        RAT = 'none'
        RT = 999
    Trial = Trial + 1
    # add trial-level data
    data = np.vstack((data, np.hstack((subject,
            Trial,
            TRIAL_LIST_RAND[index]['StimType'],
            TRIAL_LIST_RAND[index]['StimCategory'],
            TRIAL_LIST_RAND[index]['Stimulus'], 
            RESP,
            RAT,
            "%.3f" %RT))))


# save results document
np.savetxt(parent_dir + "results" + slash + "AVInt_goodness_" + prefix + ".tsv", data, fmt='%s', delimiter='\t', newline='\n', header='', footer='', comments='# ')

#display a Thank You message
FinalThankYou_txt.draw()
win.flip()
core.wait(2)
win.flip()

# close everything
win.close()
core.quit()