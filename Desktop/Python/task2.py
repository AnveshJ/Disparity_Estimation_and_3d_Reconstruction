import time
start_time = time.time()
import cv2
import random
import sys
import os
import numpy as np
import math
import scipy.misc
#import Image
#import PIL
import matplotlib.pyplot as plt
import Tkinter
import pprint

from matplotlib.pyplot import imshow
from Tkinter import Tk
from os import listdir
from os.path import isfile, join

#Appending_Path_to_images
#sys.path.append("/Users/anveshjadon/Desktop/Python/task2")

#Declaring_Images_Arrays
images1 = []
images2 = []

#Taking_Input_of_Images_from_first_camera_in_Arrays
mypath='/Users/anveshjadon/Desktop/Python/task2/1'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = np.empty(len(onlyfiles), dtype=object)
#for n in range(1, len(onlyfiles)):
images1.append(cv2.imread( join(mypath,onlyfiles[1])) )

#Taking_Input_of_Images_from_second_camera_in_Arrays
mypath='/Users/anveshjadon/Desktop/Python/task2/2'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = np.empty(len(onlyfiles), dtype=object)
#for n in range(1, len(onlyfiles)):
images2.append(cv2.imread( join(mypath,onlyfiles[1])) )

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


#Loops for finding disparities in images
for n in range(0,len(images1)):
		disp_list = []
		for siz in range(0,len(block_size)):
			#stereo = cv2.StereoSGBM_create(minDisparity=min_disparity,numDisparities=num_disparities, blockSize=block_size[siz])
			P_1 = 6*block_size[siz]*block_size[siz]
			P_2 = 30*block_size[siz]*block_size[siz]
			stereo1 = cv2.StereoSGBM(minDisparity=min_disparity,numDisparities=num_disparities, SADWindowSize=block_size[siz], 
				P1=P_1,P2=P_2, disp12MaxDiff=disp_12_Max_Diff, preFilterCap = pre_Filter_Cap,uniquenessRatio=uniqueness_Ratio,
			 	 speckleWindowSize = speckle_Window_Size, speckleRange=speckle_range)
			disparity=(stereo1.compute(images1[n],images2[n]))
			disparity = disparity+16
			if disparity!= None:
				#Structuring_Element and my_dilate function
				kernel = cv2.getStructuringElement(cv2.MORPH_RECT, Size)
				disparity = cv2.dilate(disparity,kernel,iterations=1)
				#Closing Small Holes
				disparity = cv2.morphologyEx(disparity, cv2.MORPH_CLOSE, kernel,iterations=5)

			disp_list.append(disparity)
		###Takin mean of values
		disp_list=np.mean(disp_list, axis=0)
		
		# Final Disparity Display
		imshow(disp_list)
		print("--- %s seconds ---" % (time.time() - start_time))
		plt.show()