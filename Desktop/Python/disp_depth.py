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
import fnmatch
import matplotlib.pyplot as plt
import Tkinter
import pprint

from tqdm import tqdm
from matplotlib.pyplot import imshow
from Tkinter import Tk
from os import listdir
from os.path import isfile, join

#### Function for estimating disparity and depth with root folder, subject and task input.
def disp_depth(root, subj, task):
	
	#Declaring_Images_Arrays
	images1 = []
	images2 = []
	disparity = []
	random_images = range(100)
	random_image = range(10)
	#Taking_Input_of_Images_from_first_camera_in_Arrays
	mypath=root+subj+'/'+subj+task+'/'+subj+task+'_images'+'/'+'task1/'
	print(mypath)
	for n in range(2000,2099):
		for i in range(0,9):
			filename1 = mypath + 'cam1_frame_'+str(n)+str(i)+'.bmp'
			filename2 = mypath + 'cam2_frame_'+str(n)+str(i)+'.bmp'
			if os.path.exists(filename1) and os.path.exists(filename2):
				images1.append(cv2.imread(filename1))
				images2.append(cv2.imread(filename2))
	
	#Declaring_disparity_parameters.  --- # Values are original values, you can optimize them according to you
										  # code but start with these.
	min_disparity = 0 #0
	block_size = [5, 15, 17] #[5 15 17]
	disp_12_Max_Diff = 1 #2
	pre_Filter_Cap = 0 #0
	uniqueness_Ratio = 10 #10
	speckle_Window_Size = 0 #100
	speckle_range = 0 #32
	num_disparities = 16 #16
	
	#Declaring_Variables
	Size = (3,3)

	#Disp2Depth matrix
	Q = np.asarray(cv.Load("%s%s/%s%s/calibration_frames/Disp2depth_matrix.xml"%(root,subj,subj,task)))


	#Loops for finding disparities in images
	for n in range(0,len(images2)):
		disp_list = []
		depth_list = []
		a = []
		for siz in range(0,len(block_size)):
			#Another method to create compute frame -> stereo = cv2.StereoSGBM_create(minDisparity=min_disparity,numDisparities=num_disparities, blockSize=block_size[siz])
			#Disparity Variables oonly, depends on frame.
			P_1 = 6*block_size[siz]*block_size[siz]
			P_2 = 30*block_size[siz]*block_size[siz]
			
			#Compute frame for disparity
			stereo1 = cv2.StereoSGBM(minDisparity=min_disparity,numDisparities=num_disparities, SADWindowSize=block_size[siz], 
				P1=P_1,P2=P_2, disp12MaxDiff=disp_12_Max_Diff, preFilterCap = pre_Filter_Cap,uniquenessRatio=uniqueness_Ratio,
			 	 speckleWindowSize = speckle_Window_Size, speckleRange=speckle_range)
			#Computing disparity map for a particular window size
			disparity=(stereo1.compute(images1[n],images2[n]))
			if disparity!= None:
				#To overcome negative values.
				disparity = disparity+16
				#Structuring_Element and my_dilate function
				kernel = cv2.getStructuringElement(cv2.MORPH_RECT, Size)
				# Dilating the disparity graph, you can play with iterations but time increases with iterations.
				disparity = cv2.dilate(disparity,kernel,iterations=1)
				#Closing Small Holes
				disparity = cv2.morphologyEx(disparity, cv2.MORPH_CLOSE, kernel,iterations=0)
				# Computing depth map
				a = cv2.reprojectImageTo3D(disparity,Q,handleMissingValues=False)
				# Appending disparity for three window sizes
				disp_list.append(disparity)
			if a!= None:
				#Appending depth map for three window sizes
				depth_list.append(a)
		# Taking mean along z axis for three window sizes
		disp_list=np.mean(disp_list, axis=0)
		depth_list=np.mean(depth_list, axis =0)
		#Cutting of error values for depth_Map
		depth_list[depth_list<-60] = None
		depth_list[depth_list>90] = None
		#Saving maps
		scipy.misc.imsave("%s%s/%s%s/new_depth/depth_frame_%d.bmp"%(root,subj,subj,task,n), depth_list)
		scipy.misc.imsave("%s%s/%s%s/new_disp/disp_frame_%d.bmp"%(root,subj,subj,task,n), disp_list)
	#Time for completing the task.
	print("--- %s seconds ---" % (time.time() - start_time))
	
	return None

if __name__=="__main__":
    root = str(sys.argv[1])
    subj = str(sys.argv[2])
    task = str(sys.argv[3])
    disp_depth(root, subj, task)