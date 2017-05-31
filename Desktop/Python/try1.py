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
#import Image
import PIL
import matplotlib
import Tkinter
import pprint
import vispy

from vispy import app
from vispy import gloo
from vispy.plot import Fig
from matplotlib.pyplot import imshow
from Tkinter import Tk
from os import listdir
from os.path import isfile, join
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

#Appending_Path_to_images
#sys.path.append("/Users/anveshjadon/Desktop/Python/task2")



#Declaring_Images_Arrays
images1 = []
images2 = []

#Taking_Input_of_Images_from_first_camera_in_Arrays
mypath='/Users/anveshjadon/Desktop/Python/task1/1'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = np.empty(len(onlyfiles), dtype=object)
#for n in range(1, len(onlyfiles)):
images1.append(cv2.imread( join(mypath,onlyfiles[1])) )
RGB = np.asarray(np.zeros((480,640,3), dtype=np.float))

RGB[:,:,0] = images1[0][:,:,0]
RGB[:,:,1] = images1[0][:,:,1]
RGB[:,:,2] = images1[0][:,:,2]

#Taking_Input_of_Images_from_second_camera_in_Arrays
mypath='/Users/anveshjadon/Desktop/Python/task1/2'
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

num_disparities = 16 #16
#Declaring_Variables
disparity = []

Size = (3,3)


Q = np.asarray(cv.Load("/Users/anveshjadon/Downloads/EXAMPLE_ANVESH-2/DATA/AGO/AGO_WI2/calibration_frames/Disp2depth_matrix.xml"))
Distortion_cam1 = (cv.Load("/Users/anveshjadon/Downloads/EXAMPLE_ANVESH-2/DATA/AGO/AGO_WI2/calibration_frames/Distortion_cam1.xml"))
Distortion_cam2 = (cv.Load("/Users/anveshjadon/Downloads/EXAMPLE_ANVESH-2/DATA/AGO/AGO_WI2/calibration_frames/Distortion_cam2.xml"))
Rotation_matrix = np.asarray(cv.Load("/Users/anveshjadon/Downloads/EXAMPLE_ANVESH-2/DATA/AGO/AGO_WI2/calibration_frames/Rotation_matrix.xml"))
Transalation_matrix = np.asarray(cv.Load("/Users/anveshjadon/Downloads/EXAMPLE_ANVESH-2/DATA/AGO/AGO_WI2/calibration_frames/Translation_vector.xml"))
Rectification_1 = np.asarray(cv.Load("/Users/anveshjadon/Downloads/EXAMPLE_ANVESH-2/DATA/AGO/AGO_WI2/calibration_frames/Rectification_transform_cam1.xml"))
Rectification_2 = np.asarray(cv.Load("/Users/anveshjadon/Downloads/EXAMPLE_ANVESH-2/DATA/AGO/AGO_WI2/calibration_frames/Rectification_transform_cam2.xml"))
Projection_1 = np.asarray(cv.Load("/Users/anveshjadon/Downloads/EXAMPLE_ANVESH-2/DATA/AGO/AGO_WI2/calibration_frames/Projection_matrix_cam1.xml"))
Projection_2 = np.asarray(cv.Load("/Users/anveshjadon/Downloads/EXAMPLE_ANVESH-2/DATA/AGO/AGO_WI2/calibration_frames/Projection_matrix_cam2.xml"))
imageSize = np.asarray([480,480])
#Q = np.asarray([[1, 0 , 0, -287.49],[0 ,1, 0 ,-214.67],[0,0,0,410.7725],[0,0,-0.14988,0]])

#Loops for finding disparities in images


