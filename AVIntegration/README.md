# Audio-Visual Integration

This folder contains the point-light PsychoPy version of the AV Integration experiment (for more info on the paradigm, see [Irwin et al., (2016)](https://asa.scitation.org/doi/abs/10.1121/1.4971110) and [Irwin et al., (2018)](http://booksandjournals.brillonline.com/content/journals/10.1163/22134808-00002580).

### Contents:
* `AV_Int_pointLight.py` - this is the PsychoPy experiment.
* `face_stim.csv` - stim listing for the face block
* `pl_stim.csv` - stim listing for the point-light block
* `face_stim_clip.csv` - stim listing for face block, only 10 trials
* `pl_stim_clip.csv` - stim listing for point-light block, only 10 trials

**Note:** If you want to test the experiment, change the `"%s_stim.csv"` in line 143 to `"%s_stim_clip.csv"`. This will use the shorter stimuli lists, making testing a lot easier.

## How to Run

0. Make sure you have [PsychoPy](http://psychopy.org/installation.html) up an running on your computer. This will include installing Python 2.7.   
1. Download the `misc` respository by going to [this](https://github.com/kryherd/misc) page and clicking Clone or Download (green button).
2. Copy the `AVIntegration` folder into your desired location. (You can delete the other folders).
3. Open PsychoPy.
4. Click View > Open Coder View.
5. Click File > Open... and select the `AV_Int_pointLight.py` file.
6. Click the little green man to run. **IMPORTANT:** Make sure you are running from the **CODER** view, **not** the Builder view. You should see the code pop up in Coder View before you run. See below.

![Click on the coder view](./coder.png)

7. A dialog box should pop up (like the one below). Enter the participant number under ID Number. Use the Order box to counterbalance the three blocks.

| Order Number 	|   Block 1   	|   Block 2   	|   Block 3   	|
|:------------:	|:-----------:	|:-----------:	|:-----------:	|
|       1      	|     Face    	| Point-light 	|  Pixelated  	|
|       2      	|     Face    	|  Pixelated  	| Point-light 	|
|       3      	| Point-light 	|     Face    	|  Pixelated  	|
|       4      	| Point-light 	|  Pixelated  	|     Face    	|
|       5      	|  Pixelated  	|     Face    	| Point-light 	|
|       6      	|  Pixelated  	| Point-light 	|     Face    	|

![Dialog box](./startup.png)

8. From there the experiment should run pretty smoothly. Read through the instructions with the participant.

Contact me at [kayleigh.ryherd@uconn.edu](mailto:kayleigh.ryherd@uconn.edu) if you have any issues.

## Troubleshooting

A lot of the errors that happen in this experiment come because the laptop we are using is very old and has a (relatively) small amount of memory. The main thing you should focus on is not overloading the machine. Ways to do this include:

* **Restart the computer between participants**: If you try to run the task too many times, you might see a blank screen between trials. This means that the experiment is dropping frames. Restart the computer and try again.
* **Give the computer time to boot up**: If you try to open PsychoPy right as the computer is starting, it will not appear to open. Give the computer solidly 5 minutes to boot.

These are the issues that I have run into. If you have any more, let me know and I'll try to fix them.