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
#import Image
#import PIL
import matplotlib.pyplot as plt
import Tkinter
import pprint

from matplotlib.pyplot import imshow
from Tkinter import Tk
from os import listdir
from os.path import isfile, join


def disp_depth(root, subj, task):
	#Appending_Path_to_images
	#sys.path.append("/Users/anveshjadon/Desktop/Boris_Data/cameras/raw_data/BWS_images/task")

	#Declaring_Images_Arrays
	images1 = []
	images2 = []

	#Taking_Input_of_Images_from_first_camera_in_Arrays
	mypath=root+subj+'/'+subj+task+'/'+subj+task+'_images'+'/'+'task1/'
	imlist = np.array(fnmatch.filter(os.listdir(mypath), '*.bmp'))
	for im in imlist:
		#if im.find('cam1') >0:
		im_left = cv2.imread(mypath+im, flags=0)
		im_right = cv2.imread(mypath+im.replace("cam1","cam2"),flags=0)
		images1.append(im_left)
		images2.append(im_right)

	#Declaring_disparity_parameters
	min_disparity = 0 #0
	block_size = [5, 15, 17] #[5 15 17]
	#P_1 = 0 #0
	#P_2 = 0 #0
	disp_12_Max_Diff = 1 #2
	pre_Filter_Cap = 0 #0
	#texture_threshold = 10 #10
	uniqueness_Ratio = 10 #10
	speckle_Window_Size = 0 #100
	speckle_range = 0 #32

	num_disparities = 80 #16
	#Declaring_Variables
	disparity = []

	Size = (3,3)
	Q = np.asarray(cv.Load("/Users/anveshjadon/Downloads/EXAMPLE_ANVESH-2/DATA/AGO/AGO_WI2/calibration_frames/Disp2depth_matrix.xml"))


	#Loops for finding disparities in images
	for n in range(0,len(images1)):
		disp_list = []
		depth_list = []
		a = []
		for siz in range(0,len(block_size)):
			#stereo = cv2.StereoSGBM_create(minDisparity=min_disparity,numDisparities=num_disparities, blockSize=block_size[siz])
			P_1 = 6*block_size[siz]*block_size[siz]
			P_2 = 30*block_size[siz]*block_size[siz]
			stereo1 = cv2.StereoSGBM(minDisparity=min_disparity,numDisparities=num_disparities, SADWindowSize=block_size[siz], 
				P1=P_1,P2=P_2, disp12MaxDiff=disp_12_Max_Diff, preFilterCap = pre_Filter_Cap,uniquenessRatio=uniqueness_Ratio,
			 	 speckleWindowSize = speckle_Window_Size, speckleRange=speckle_range)
			disparity=(stereo1.compute(images1[n],images2[n]))
			if disparity!= None:
				disparity = disparity+16
				#Structuring_Element and my_dilate function
				kernel = cv2.getStructuringElement(cv2.MORPH_RECT, Size)
				disparity = cv2.dilate(disparity,kernel,iterations=1)
				#Closing Small Holes
				disparity = cv2.morphologyEx(disparity, cv2.MORPH_CLOSE, kernel,iterations=0)
				
				a = cv2.reprojectImageTo3D(disparity,Q,handleMissingValues=False)
				disp_list.append(disparity)
			if a!= None:
				depth_list.append(a)
			
		disp_list=np.mean(disp_list, axis=0)
		depth_list=np.mean(depth_list, axis =0)
		depth_list[depth_list<-60] = None
		depth_list[depth_list>100] = None
		scipy.misc.imsave("%s%s/%s%s/new_depth/depth_frame_%d.bmp"%(root,subj,subj,task,n), depth_list)
		scipy.misc.imsave("%s%s/%s%s/new_disp/disp_frame_%d.bmp"%(root,subj,subj,task,n), disp_list)
		# Final Display
		#imshow(disp_list)
	print("--- %s seconds ---" % (time.time() - start_time))
		#plt.show()
	return None

if __name__=="__main__":
    root = str(sys.argv[1])
    subj = str(sys.argv[2])
    task = str(sys.argv[3])
    disp_depth(root, subj, task)