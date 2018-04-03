# Haskins EEG Room Eyetracker

Here is where I will list information about using the eyetracker in the EEG room at Haskins.

**Host PC**: Labeled as "EYETRACKING COMPUTER." This is the one that you calibrate the eyetracker from.

**Display PC**: Labeled as "EPRIME COMPUTER." This is the one that you run your experimental software from (e.g., E-Prime, MATLAB, etc.)

### Updates

* **4/3/2018**: Updated software on Host PC to Eyelink 1000 v. 4.594 (right). Right version was used because the illuminator is on the right side of the eyetracker (lens is on the left).

## Details of an EEG-Eyetracking Setup

Because our setup has EEG and Eyetracking, we have changed the default IP address of the Host PC. Here are details on how to configure the Host PC once you have changed its IP address so that it can still talk to the Eyetracker.

1.  Turn on the Host pc and wait for the initial menu that prompts you to boot into Eyelink or Windows, and boot into Windows.
2. In Windows, click on Start > Computer and on the left you should find a partition called EYELINK (E:). This is the Eyelink partition on the hard drive. If you double-click on it you should see a folder called 'elcl'.
3. Go to `\elcl_old\EXE`
4. Change the "host_address" parameter in the EYENET.INI configuration file OR put the following line of command in the FINAL.INI file.

        host_address = 10.10.10.6, 255.255.255.0

The subject PC is connected to the NetStation via an Ethernet cable for sending event markers. Because the Eyelink tracker also needs an Ethernet connection to the subject PC, we use a hub/switch so that NetStation, the EyeLink Host PC, and the subject PC are all connected to the hub/switch.

## Running an Eyetracking Script in MATLAB

Since we have changed the IP address of the Host PC, our MATLAB script needs to specify the IP address. To do this, add a line of code before calling EyelinkInit(). 

```
% STEP 4
% Initialization of the connection with the Eyelink Gazetracker.
% exit program if this fails.
Eyelink('SetAddress', '10.10.10.6');
           
if ~EyelinkInit(dummymode)
   fprintf('Eyelink Init aborted.\n');
   cleanup;  % cleanup function
   return;
end            
```

## Running an Eyetracking Script in E-Prime

S-R provides example E-Prime scripts. These can be found in Start menu -> All Programs -> SR Research -> EyeLink Examples->E-Prime Examples. It's recommended to look at the Picture example, which has custom inline code that is explained below.

* We have some custom calibration/validation functions in the “User” tab of the “Script” window, which can be brought up by pressing Alt + 5. These scripts can be copied to your own scripts --  there is no need to alter these functions as they are fixed functions.
* The Inline “elConnect” helps to establish a link to the tracker, to open an eye movement data file, and to set up a few parameters, such as calibration type (Line 32), data file preamble text (Line 29), and background/foreground colours for the calibration/validation graphics (Line 13-14). This Inline generally does not need to be modified.
* The Inline “elCameraSetup” will evoke the custom calibration/validation routines at the beginning of each block.
* The Inline “startRecording” at the beginning of each trial will first send a standard “TRIALID” message to the tracker (Line 14). This message is necessary for proper trial parsing in Data Viewer (the tool we use to analyze eye movement data). Here we also send a “record_status_message” to the host PC (Line 17). This will be displayed on the host PC when the subject is performing the task, so the experimenter can easily figure out which trial is currently running.
* At the end of a single trial, we have an inline “stopRecording” to stop recording and to send trial variables to the tracker. These trial variables will show up in the “Trial Variable Manager” in Data Viewer, and they are critical for performing group-level analysis. More design variables can go here.
*  At the end of a testing session, we close the link to the tracker and grab data from the host PC. This is done in the Inline “elClose”. 

**Important**: Like in the MATLAB scripts, we need to change the IP address of the eyetracker to `10.10.10.6` for the Haskins EEG lab setup.