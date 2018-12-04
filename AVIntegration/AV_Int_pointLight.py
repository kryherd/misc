#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PsychoPy experiment by Kayleigh Ryherd, last updated 12/4/2018
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
parent_dir = ".\\"

#get some startup information from the user
info = {'ID Number':''}
dlg = gui.DlgFromDict(info, title='AV Int')
if not dlg.OK:
    core.quit()

#### EXPERIMENT SETUP
#set log prefixes
prefix = 'sub-%s' % (info['ID Number'])
#logging data 
errorLog=logging.LogFile(parent_dir + "results\\" + prefix + "_errorlog.log", level=logging.DATA, filemode='w')

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
win = visual.Window(size = [1280,800],
                    color = "black",
                    fullscr = True, allowGUI=False,
                    units = "pix")

# header for data log
data = np.hstack(("Subject", "Trial", "StimType", "StimCategory","Stimulus", "ACC","KEY", "RT"))


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

goodness = visual.TextStim(win, text = "Think about the BAs you heard.\nPlease press the key corresponding to how\nstrong and clear the B sounds in them were overall.\n\n1 - strong B sound\n\n2- medium B sound\n\n3 - weak B sound\n\n4 - did not hear any BAs " ,
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

# set up A sound
ba_redu = sound.backend_pygame.SoundPygame(parent_dir + "audio\\ba_redu_audio.wav")
ba_base = sound.backend_pygame.SoundPygame(parent_dir + "audio\\ba_base_audio.wav")

##### RUN EXPERIMENT
# time when experiment started
t0 = globalClock.getTime()
## show instructions
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
# load in trials and randomize them
TRIAL_LIST = psychopy.data.importConditions(fileName = "twoAFC_stim_clip.csv")
totalTrials = len(TRIAL_LIST)
TRIAL_LIST_RAND = TRIAL_LIST
random.shuffle(TRIAL_LIST_RAND)
# set trial counter
Trial = 0
# run through trials
for index in range(len(TRIAL_LIST_RAND)):
    check_exit()
    # set up video stimulus
    mov = visual.MovieStim3(win, parent_dir + 'video\\' + TRIAL_LIST_RAND[index]['Stimulus'],
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
    KEY = event.getKeys(timeStamped=globalClock)
    # if a key was pressed
    if KEY != []:
        RESP = KEY[0][0] # save key that was pressed
        RT = KEY[0][1] - t1
    # if nothing was pressed
    elif KEY == []:
        RESP = 'none'
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
    # add trial-level data
    data = np.vstack((data, np.hstack((info['ID Number'],
            Trial,
            TRIAL_LIST_RAND[index]['StimType'],
            TRIAL_LIST_RAND[index]['StimCategory'],
            TRIAL_LIST_RAND[index]['Stimulus'], 
            ACC,
            RESP,
            "%.3f" %RT))))
# save results document
np.savetxt(parent_dir + "results\\" + "AVInt_PointLight_" + prefix + ".tsv", data, fmt='%s', delimiter='\t', newline='\n', header='', footer='', comments='# ')

### Goodness judgment
goodness.draw()
win.flip()
goodKey = event.waitKeys(keyList=['1','2','3','4'])

with open("results\\gj.txt","a") as gj:
    gj.write(info['ID Number'] + "\t" + goodKey[0] + "\n")


#display a Thank You message
FinalThankYou_txt.draw()
win.flip()
core.wait(2)
win.flip()

# close everything
win.close()
core.quit()