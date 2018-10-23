#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PsychoPy experiment by Kayleigh Ryherd, 10/23/2018
"""

### IMPORTANT:
### Under psychopy preferences/general
### (1) change the audio driver to "portaudio" (otherwise the program won't stop running when it's done)
### (2) change the audio library to "pygame" (otherwise the audio won't stop playing when the video stops)

# import psychopy modules
import psychopy
from psychopy import visual, core, event, sound, gui, data, logging
import math
import numpy as np 
import random
import pandas as pd

#set parent directory
parent_dir = "./"

#get some startup information from the user
info = {'ID Number':'', 'Order':''}
dlg = gui.DlgFromDict(info, title='AV Int')
if not dlg.OK:
    core.quit()

#### EXPERIMENT SETUP
#set log prefixes
prefix = 'sub-%s_order%s' % (info['ID Number'], info['Order'])
#logging data 
errorLog=logging.LogFile(parent_dir + "results/" + prefix + "_errorlog.log", level=logging.DATA, filemode='w')

def check_exit():
#abort if esc was pressed
    if event.getKeys('escape'):
        win.close()
        core.quit()

#create clock
globalClock = core.Clock()
logging.setDefaultClock(globalClock)

#info about the screen
## change to match your resolution
win = visual.Window(size = [1440,900],
                    color = "white",
                    fullscr = True, allowGUI=False,
                    units = "pix")

# header for data log
data = np.hstack(("Subject", "Block", "Trial", "StimType", "Stimulus", "KEY", "RT"))

# select block
if info['Order'] == '1':
    block = {1: "face", 2: "pl"}
elif info['Order'] == '2':
    block = {1: "pl", 2: "face"}
else:
    print "\n-----------\nInvalid Order Selected. Please Try Again.\n-----------\n"
    win.close()
    core.quit()


# set up text windows
instruct_txt = visual.TextStim(win, text = "In this experiment you will be watching videos and hearing sounds.\n\nYou will respond every time you hear A.\n\nPress SPACE now to hear an example of A." ,
                        pos = [0.0,0.0],
                        color = "black",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

great_txt = visual.TextStim(win, text = "Great. Every time you hear A, press SPACE. \n \n \nPress SPACE to begin." ,
                        pos = [0.0,0.0],
                        color = "black",
                        height = 32,
                        alignHoriz='center',
                        alignVert='center',
                        font = "Arial",
                        wrapWidth= 1400,
                        autoLog=True)

diff_txt = visual.TextStim(win, text = "Let's try it again with some different videos.\nRemember, every time you hear A, press SPACE. \n \n \nPress SPACE to begin." ,
                        pos = [0.0,0.0],
                        color = "black",
                        height = 32,
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

# set up A sound
ba_redu = sound.SoundPygame(parent_dir + "audio/ba_redu_audio.wav")

##### RUN EXPERIMENT
# time when experiment started
t0 = globalClock.getTime()
# run through the blocks in order
for i in range(1, 3):
	# for the first block, show the instructions
    if i == 1:
        instruct_txt.draw()
        win.flip()
        # when space is pressed...
        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
        # ... play the A sound
        ba_redu.play()
        core.wait(2)
        great_txt.draw()
        win.flip()
        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
    # for the second block, show the second block instructions    
    if i == 2:
        diff_txt.draw()
        win.flip()
        keys = event.waitKeys(keyList=['space'], timeStamped=globalClock)
    blockName = block[i]
    # load in trials and randomize them
    TRIAL_LIST = psychopy.data.importConditions(fileName = "%s_stim.csv" % (blockName))
    totalTrials = len(TRIAL_LIST)
    TRIAL_LIST_RAND = TRIAL_LIST
    random.shuffle(TRIAL_LIST_RAND)
    # set trial counter
    Trial = 0
    # run through trials
    for index in range(len(TRIAL_LIST_RAND)):
        check_exit()
        # set up video stimulus
        mov = visual.MovieStim3(win, parent_dir + 'video/' + TRIAL_LIST_RAND[index]['Stimulus'],
                        size = (640, 480),
                        flipVert = False,
                        flipHoriz = False,
                        loop = False)
        # timestamp right as movie is started
        t1 = globalClock.getTime()
        while mov.status != visual.FINISHED:
            mov.draw()
            win.flip()
        core.wait(0.5)
        KEY = event.getKeys(keyList=["space"],timeStamped=globalClock)
        # if space was not pressed...
        if KEY == []:
            RESP = 'none'
            RT = 999
        # if space was pressed...
        elif KEY != []:
            RESP = 'space'
            RT = KEY[0][1] - t1
        Trial = Trial + 1
        # add trial-level data
        data = np.vstack((data, np.hstack((info['ID Number'],
                blockName, 
                Trial,
                TRIAL_LIST_RAND[index]['StimType'],
                TRIAL_LIST_RAND[index]['Stimulus'], 
                RESP,
                "%.3f" %RT))))
# save results document
np.savetxt(parent_dir + "results/" + "AVInt_PointLight_" + prefix + ".tsv", data, fmt='%s', delimiter='\t', newline='\n', header='', footer='', comments='# ')

#display a Thank You message
FinalThankYou_txt.draw()
win.flip()
core.wait(2)
win.flip()

# close everything
win.close()
core.quit()