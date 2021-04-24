import numpy as np
from matplotlib import pyplot as plt
from typing import Union, Any, List, Optional, cast, Dict

from skimage.measure import LineModelND, ransac
import os
from skimage import io
import math
import datetime
import glob
from sklearn.neighbors import KDTree
import statistics

min_samples=3 #RANSAC parameter - The minimum number of data points to fit a model to.
#min_inliers_allowed=5 #Custom parameter  - A line is selected only if these many inliers are found

class RansacLineInfo(object):
    """Helper class to manage the information about the RANSAC line."""
    def __init__(self, inlier_points:np.ndarray, model:LineModelND):
        self.inliers=inlier_points #the inliers that were detected by RANSAC algo
        self.model=model    #The LinearModelND that was a result of RANSAC algo

    @property
    def unitvector(self):
        """The unitvector of the model. This is an array of 2 elements (x,y)"""
        return self.model.params[1]

def read_black_pixels(imagefilename:str):
    #returns a numpy array with shape (N,2) N points, x=[0], y=[1]
    #The coordinate system is Cartesian
    np_image=io.imread(imagefilename,as_gray=True)
    black_white_threshold=0
    if (np_image.dtype == 'float'):
        black_white_threshold=0.5
    elif (np_image.dtype == 'uint8'):
        black_white_threshold=128
    else:
        raise Exception("Invalid dtype %s " % (np_image.dtype))
    indices=np.where(np_image <= black_white_threshold)
    width=np_image.shape[1]
    height=np_image.shape[0]
    cartesian_y=height-indices[0]-1
    np_data_points=np.column_stack((indices[1],cartesian_y)) 
    return np_data_points, width,height

def extract_first_ransac_line(data_points:List, max_distance:int):
    """
    Inputs:
        Accepts a numpy array with shape N,2  N points, with coordinates x=[0],y=[1]
        max_distance - This is the RANSAC threshold distance from a line for a point to be classified as inlier
    Returns 
         A numpy array with shape (N,2), these are the inliers of the just discovered ransac line
         All data points with the inliers removed
         The model line
    """
    
    print("Doing RANSAC to get single line on image with %d points and RANSAC threshold=%f and min_samples=%d" % (data_points.shape[0],max_distance,min_samples))
    model_robust, inliers = ransac(data_points, LineModelND, min_samples=min_samples,
                                   residual_threshold=max_distance, max_trials=1000)
    results_inliers=[]
    results_inliers_removed=[]
    for i in range(0,len(data_points)):
        if (inliers[i] == False):
            #Not an inlier
            results_inliers_removed.append(data_points[i])
            continue
        x=data_points[i][0]
        y=data_points[i][1]
        results_inliers.append((x,y))
    return np.array(results_inliers), np.array(results_inliers_removed),model_robust

def generate_plottable_points_along_line(model:LineModelND, xmin:int,xmax:int, ymin:int, ymax:int):
    """
    Computes points along the specified line model
    The visual range is 
    between xmin and xmax along X axis
        and
    between ymin and ymax along Y axis
    return shape is [[x1,y1],[x2,y2]]
    """
    unit_vector=model.params[1]
    slope=abs(unit_vector[1]/unit_vector[0])
    x_values=None
    y_values=None
    if (slope > 1):
        y_values=np.arange(ymin, ymax,1)
        x_values=model.predict_x(y_values)
    else:        
        x_values=np.arange(xmin, xmax,1)
        y_values=model.predict_y(x_values)

    np_data_points=np.column_stack((x_values,y_values)) 
    return np_data_points

def superimpose_all_inliers(ransac_lines,width:float, height:float):
    #Create an RGB image array with dimension heightXwidth
    #Draw the points with various colours
    #return the array

    new_image=np.full([height,width,3],255,dtype='int')
    colors=[(0,255,0),(255,255,0),(0,0,255)]
    for line_index in range(0,len(ransac_lines)):
        color=colors[line_index % len(colors)]
        ransac_lineinfo:RansacLineInfo=ransac_lines[line_index]
        inliers=ransac_lineinfo.inliers 
        y_min=inliers[:,1].min()
        y_max=inliers[:,1].max()
        x_min=inliers[:,0].min()
        x_max=inliers[:,0].max()
        plottable_points=generate_plottable_points_along_line(ransac_lineinfo.model, xmin=x_min,xmax=x_max, ymin=y_min,ymax=y_max)
        for point in plottable_points:
            x=int(round(point[0]))
            if (x >= width) or (x < 0):
                continue
            y=int(round(point[1]))
            if (y >= height) or (y < 0):
                continue
            new_y=height-y-1
            new_image[new_y][x][0]=color[0]
            new_image[new_y][x][1]=color[1]
            new_image[new_y][x][2]=color[2]
    return new_image

def extract_multiple_lines_and_save(inputfile:str,iterations:int, min_inliers_allowed:int, threshold_factor:float):
    """
    min_inliers_allowed - a line is selected only if it has more than this inliers. The search process is halted when this condition is met
    """
    inputfilename=os.path.basename(inputfile)
    print("-----------------Processing: %s , with min_inliers_allowed=%f, threshold_factor=%f" % (inputfilename,min_inliers_allowed,threshold_factor))
    folder_script=os.path.dirname(__file__)

    results:List[RansacLineInfo]=[]
    all_black_points,width,height=read_black_pixels(inputfile)
    print("Found %d pixels in the file %s" % (len(all_black_points),inputfilename))
    starting_points=all_black_points
    for index in range(0,iterations):
        ransac_threshold=calculate_ransac_threshold_from_nearest_neighbour_estimate(starting_points) *threshold_factor
        min_needed_points=min_samples*2
        if (len(starting_points) <= min_samples*2):
            print("No more points available. Terminating search for RANSAC. Available points=%d Cutt off points count=%d" % (len(starting_points),min_needed_points))
            break
        inlier_points,inliers_removed_from_starting,model=extract_first_ransac_line(starting_points,max_distance=ransac_threshold)
        if (len(inlier_points) < min_inliers_allowed):
            print("Not sufficeint inliers found %d , threshold=%d, therefore halting" % (len(inlier_points),min_inliers_allowed))
            break
        print("Found RANSAC line with %d inliers" % (len(inlier_points)))
        starting_points=inliers_removed_from_starting
        results.append(RansacLineInfo(inlier_points,model))        
    
    superimposed_image=superimpose_all_inliers(results,width,height)
    print("Found a total of %d RANSAC lines with RANSAC threshold=%f" % (len(results), ransac_threshold))
    #Save the results
    filename_noextension=os.path.splitext(inputfilename)[0]
    folder_script=os.path.dirname(__file__)
    file_result=os.path.join(folder_script,"./out/",("sequential-ransac-%s-tfac-%.2f.png") % (filename_noextension,round(threshold_factor,2)))
    io.imsave(file_result,superimposed_image)
    print("Results saved to file %s" % (file_result))


def calculate_ransac_threshold_from_nearest_neighbour_estimate(data_points:List):
    print("Calculating RANSAC threshold from %d point " % (data_points.shape[0]))
    tree = KDTree(data_points)
    nearest_dist, nearest_ind = tree.query(data_points, k=2)
    nne_distances=list(nearest_dist[0:,1:].flatten())
    mean=statistics.mean(nne_distances)
    median=statistics.median(nne_distances)
    stdev=statistics.stdev(nne_distances)
    distance_from_line=median 
    print("Mean=%f, Median=%f, Stddev=%f calculated ransca_threshold=%f" % (mean,median,stdev,distance_from_line))
    return distance_from_line

def run_selected_filepattern(pattern:str,num_trials:int):
    folder_script=os.path.dirname(__file__)
    folder_with_files=os.path.join(folder_script,"./in/")
    matching_files=glob.glob(folder_with_files+pattern)
    print("Found %d matching files" % (len(matching_files)))
    for file in matching_files:
        extract_multiple_lines_and_save(inputfile=file,iterations= num_trials, min_inliers_allowed=3, threshold_factor=0.25)
        extract_multiple_lines_and_save(inputfile=file,iterations= num_trials, min_inliers_allowed=3, threshold_factor=0.5)
        extract_multiple_lines_and_save(inputfile=file,iterations= num_trials, min_inliers_allowed=3, threshold_factor=1.0)



#run_selected_filepattern(pattern="*parabola*.png",num_trials=10)
run_selected_filepattern(pattern="*parabola*.8*.png",num_trials=10) #tried with 5

'''
Major change in computing NND
-----------------------------
    At every sequence of RANSAC,compute the NND
    Why? You are removing the points in every iteration
    Therefore, if there was a poor quality line needing larger RANSAC threshold, then chances of that finding increase now

Lesson 1 - Size of the patch
----------------------------
    The ability to detect a valid line is dependent on the size of the patch
    You will need smaller patches
    The size of the patch should not be much larger than the valid line
    Need to find a heuristic. Example - if target length=X then patch size= is X * factor

Lesson 2 - Ransac threshold
----------------------------
    I kept num_trials=5
    I tried with various fractions of mean NND - 1.0, 0.5 and 0.25
    0.25 worked find for the curve of the parabola and it identified the arms (64X45)
    1 and 0.5 worked for the larger (200X200) and the arms were identified.
    0.25 identified the arms of (200X200) but just half the length only

Lesson 3 - How many lines to find
----------------------------------
    Tried wih num_trials=10 and NND factors of 1.0 , 0.5 and 0.25
    num_trials=5 is fine. We have lesser 

'''
