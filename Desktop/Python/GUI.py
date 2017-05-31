#### Some extra libraries and functions are imported as they were used at some point in the code while its development.

import time
start_time = time.time()
import cv2
import cv
import random
import sys
import os
import numpy as np
import math
import scipy.misc
import PIL
import matplotlib 
import Tkinter
import pprint
import vispy
import subprocess
import matlab.engine
import shutil

from distutils.dir_util import copy_tree
from Tkinter import *
from vispy import app
from vispy import gloo
from vispy.plot import Fig
from Tkinter import Tk
from os import listdir
from os.path import isfile, join
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


#### stringroot is the root folder taken from GUI Input by user, for ex: /Users/anveshjadon/Desktop or F:/Data/Boris
#### stringsubj is the name of subject taken from GUI Input by user, for ex: bws, ago
#### stringtask is the task that was performed taken from GUI Input by user, for ex: cafe1

#### In case your folder structure changes, do the following ->
#### 1) Run a individual function at a time. For ex - calibrate_cameras
#### 2) Check which files or folders are missing from its error and create them there or copy them.
#### 3) Keep in mind an extra '/' after root folder path as we need to access inside it.
####    	Correct root folder path - /Users/username/desktop/Boris_Data/cameras/
#### 4) For matlab codes, you need your data in the folder where your scripts are located so create it in the name of data/
####    	Have a look at below given google link and you can see how and where all the folders and data is.

#### An example of how to make folder path or directories is available on the following google link for Boris_Cafe1 task - 
#### Unzip the folder and paste the folders name Boris_Data on your desktop. Run the GUI.py script from terminal.

#### Functions for doing different tasks
#### cmd is the command that we need to run on our terminal
#### Example - If we need to cd a folder in Dekstop/Python and then run a script, out commands be like -
#### -> cd Desktop/Python
#### -> python script.py
#### Similairly, we firs change directory to our folder which contains the script and then run the script, using '\n' as Return Operator.
#### Then we call the script using python as -> python script.py with required inputs.

#### Calibrating Cameras
def Calibrate_Cameras():
	cmd = "cd /Users/anveshjadon/Desktop/Boris_Data/cameras/stereo_calibration/scripts \n python stereo_calibration.py %sstereo_calibration/data/BWS/calibration_frames/ 250"%stringroot
	os.system(cmd)
	print "Calibration of Cameras - Done!\n"

#### Rectifying Images
def Rectifying_Images():
	cmd = "cd /Users/anveshjadon/Desktop/Boris_Data/cameras/image_rectification/scripts \n python GENERAL_rectifyframes_task.py %s %s %s"%(stringroot, stringsubj, stringtask) 
	os.system(cmd)
	print "Rectification of Images - Done!\n"

#### Computing Refernce Frame Transformation
def Comp_Ref_fram():
	cmd = "cd /Users/anveshjadon/Desktop/Boris_Data/cameras/camera_registration/scripts \n python register_camera.py %s %s %s 1"%(stringroot, stringsubj, stringtask)
	os.system(cmd)
	print "Reference frame Transformation - Computed!\n"

#### In below functions we have used a matlab code instead of python and we have used a different root folder. The data is saved in a folder named data in the scripts folder.
#### For ex - in the case of that drive link, data is saved in /eyes/data_processing/scripts/data.
#### Then the folder data is copied to our root folder inside subj, subjtask folder.

#### Refining Eye Track Data
def Refining_eye_track():
	eng = matlab.engine.start_matlab()
	eng.cd(r'/Users/anveshjadon/Desktop/Boris_Data/eyes/data_processing/scripts')
	print "Eye Tracking Data - Loaded!\n"
	eng.ET_parse('data/', '%s'%stringsubj, '%s'%stringtask,nargout=0)
	print "Eye tracking data - Refined!\n"
	if not Thumbling_task.get():
		copy_tree('/Users/anveshjadon/Desktop/Boris_Data/eyes/data_processing/scripts/data','%s%s/%s%s/eye_data'%(stringroot,stringsubj,stringsubj,stringtask))
		print("Eye Data Copied to Root")

#### Computing Dispairty and Depth Maps
def Compute_Disparity_Depth():
	os.system(" cd /Users/anveshjadon/Desktop/Boris_Data/cameras/disparity_estimation/scripts \n python disp_depth.py %s %s %s"%(stringroot,stringsubj,stringtask))
	print "Disparity - Computed! and Depth Map - Computed!\n"

#### Here also we have used a matlab code and data is saved in data/ folder in scripts folder.
#### Processing eye data and syncing it.
def Thumbling_Task():
	eng = matlab.engine.start_matlab()
	eng.cd(r'/Users/anveshjadon/Desktop/Boris_Data/eyes/data_processing/scripts')
	eng.ET_process('data/','%s'%stringsubj, '%s'%stringtask,nargout=0)
	print("\nEye Data Processed!\n")
	eng.ET_frame_sync_task('data/','%s'%stringsubj,'%s'%stringtask,nargout=0)
	print "Eye Data Synced!\n"
	copy_tree('/Users/anveshjadon/Desktop/Boris_Data/eyes/data_processing/scripts/data','%s%s/%s%s/eye_data'%(stringroot,stringsubj,stringsubj,stringtask))
	print("Eye Data Copied to Root")

#### Computing 3d Reprojection of data
def d3_projection():
	cmd = "cd /Users/anveshjadon/Desktop/Boris_Data/cameras/3d_reprojection/scripts \n python GENERAL_camera_to_eye_task.py %s %s %s"%(stringroot, stringsubj, stringtask)
	os.system(cmd)
	print "3d Reprojection Without Gaze check - Done!\n"

#### Have to add codes for following two functions.
#### Checking the eye data
def gaze_check():
	print "Gaze Data Check - Done!\n"

#### 3d Reprojection after a check on eye data
def d3_projection_2():
	print "3d Reprojection after Gaze Check - Done!\n"


#### Main function that runs on button being pressed.
def button():
    print("Running.....\n\n")
	# Taking input of Subject, task and root folder from User
    global stringsubj
    global stringtask
    global stringroot
    stringsubj = subj.get()
    stringtask = tas.get()
    stringroot = root.get()
    print("%s"%stringroot)
    print("Subject is - %s" %stringsubj)
    print("\nTask is - %s" %stringtask)
    print("\nRoot folder is - %s" %stringroot)
    print("\n\n\nFollowing task is ongoing - \n")
    # Functions are called if you have chosen that option in GUI.
    if Calib_Camera.get():
    	print "Calbirating the Cameras....\n"
    	Calibrate_Cameras()
    if Rectify_Images.get():
    	print "Rectifying the images....\n"
    	Rectifying_Images()
    if Ref_fram.get():
    	print "Computing Reference frame Transformation....\n"
    	Comp_Ref_fram()
    if Refine_eye_track.get():
    	print "Refining eye Tracking data....\n"
    	Refining_eye_track()
    if Disparity_comp.get():
    	print("Computing Disparity and Depth Map....\n")
    	Compute_Disparity_Depth()
    if Thumbling_task.get():
    	print("Checking for Thumbling Task Targets....\n")
    	Thumbling_Task()
    if threed_1.get():
    	print("Computing 3d Reprojection without Gaze Correction....\n")
    	d3_projection()
    if Correct.get():
    	print("Correcting Gaze Data....\n")
    	gaze_check()
    if threed_2.get():
    	print("Computing 3d Reprojection with Gaze Correction....\n")
    	d3_projection_2()
    print("\n\n\nJob Completed!!!! --- in %s seconds --- \n\n\n" %(time.time() - start_time))


#### For managing GUI, dig below ------------------
GUI = Tk()
GUI.title("Post-Processing")

#### Widgets for labelling and taking input from user. w is for label and subj is for giving input.
w = Label(GUI, text="Subject Name - ")
w.pack()
subj = Entry(GUI)
subj.insert(END,'bws')
subj.pack()
a = Label(GUI, text = "Task -")
a.pack()
tas = Entry(GUI)
tas.insert(END,'cafe1')
tas.pack()
b = Label(GUI, text = "Root Folder -")
b.pack()
root = Entry(GUI)
root.insert(END,'/Users/anveshjadon/Desktop/Boris_Data/cameras/')
root.pack()

#### If you wish to add any checkbox and its function, you can do the following -
#### 1) Add the variable name
#### 2) Define the checkbox using the same arguments and expression and change them as you need
#### 3) Define a function for it in main function i.e. Button Function.
#### 4) Define its function, for ex - calibrate_cameras or rectifying_images.


#### Variables for Checkboxes
Calib_Camera = IntVar()
Rectify_Images = IntVar()
Ref_fram = IntVar()
Refine_eye_track = IntVar()
Disparity_comp = IntVar()
Thumbling_task = IntVar()
threed_1 = IntVar()
Correct = IntVar()
threed_2 = IntVar()

#### Declaring checkboxes.
Calib_1 = Checkbutton(GUI, text = "Calibrate the Cameras", variable = Calib_Camera, onvalue = True, offvalue = False, height=2, width = 20)
Calib_1.pack()
Rectify_1 = Checkbutton(GUI, text = "Rectify the Images", variable = Rectify_Images, onvalue = 1, offvalue = 0, height=2, width = 20)
Rectify_1.pack()
Ref_fram_1 = Checkbutton(GUI, text = "Compute Refernce Frame Transformation", variable = Ref_fram, onvalue = 1, offvalue = 0, height=2, width = 20)
Ref_fram_1.pack()
Refine_eye_track_1 = Checkbutton(GUI, text = "Refine eye Tracking", variable = Refine_eye_track, onvalue = 1, offvalue = 0, height=2, width = 20)
Refine_eye_track_1.pack()
Disparity_comp_1 = Checkbutton(GUI, text = "Compute Disparity and Depth map", variable = Disparity_comp, onvalue = 1, offvalue = 0, height=2, width = 20)
Disparity_comp_1.pack()
Thumbling_task_1 = Checkbutton(GUI, text = "Check Targets", variable = Thumbling_task, onvalue = 1, offvalue = 0, height=2, width = 20)
Thumbling_task_1.pack()
threed_1_1 = Checkbutton(GUI, text = "3d Reconstruction", variable = threed_1, onvalue = 1, offvalue = 0, height=2, width = 20)
threed_1_1.pack()
Correct_1 = Checkbutton(GUI, text = "Correct Gaze", variable = Correct, onvalue = 1, offvalue = 0, height=2, width = 20)
Correct_1.pack()
threed_2_1 = Checkbutton(GUI, text = "3d Reconstruction Corrected", variable = threed_2, onvalue = 1, offvalue = 0, height=2, width = 20)
threed_2_1.pack()


#### Declaring the run button and giving the command it has to run after pressing.
b = Button(GUI, text="RUN", command=lambda:button())
b.pack()

GUI.mainloop()