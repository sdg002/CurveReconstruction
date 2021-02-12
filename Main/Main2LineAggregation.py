from Algorithm import RansacAlgorithm
from Algorithm import PatchByPatchRansac
from Common import RansacPatchInfo
from typing import Union, Any, List, Optional, cast
from Common import Util
from Common import RansacLineInfo
from Common import Point
import os
from skimage import io
import datetime
import statistics
import numpy as np
from Algorithm import PatchByPatchLineAggregator
from Common import ConnectedLines
from Algorithm import PatchByPatchStatisticalFilter
import math
from os import listdir
from os.path import join

#
#In this script, 
#   Step 1 - the median value of the distribution coefficient is first calculated and only lines which are above this value are selected
#   Step 2 - Similar lines from adjacent patches are discovered and an attempt is made to connect these lines
#


def process_single_file(inputfilename:str,patchdimension:int):
    print("Start")
    print("----------------------------")
    print(inputfilename)
    print("----------------------------")

    folder_script=os.path.dirname(__file__)
    absolute_path=os.path.join(folder_script,"./in/",inputfilename)

    patch_algo=PatchByPatchRansac(absolute_path)
    patch_algo.Dimension=patchdimension
    patch_algo.ransac_threshold_distance=2 #use 1 for smaller images
    arr_patches=patch_algo.run1()


    filter_handler=PatchByPatchStatisticalFilter(arr_patches)
    filtered_array_of_patches=filter_handler.filter_using_median_distributionindex()

    patch_aggregator=PatchByPatchLineAggregator(filtered_array_of_patches,patch_algo.image_width, patch_algo.image_height)
    patch_aggregator.rho_threshold=patch_algo.ransac_threshold_distance
    patch_aggregator.theta_threshold= 10 * math.pi/180 #10 degrees
    array_of_patches=patch_aggregator.find_connected_lines_in_adjacent_patches()
    overall_clusters=patch_aggregator.find_connected_lines_in_across_all_patches(array_of_patches)



    # all_ransac_lines:[]=flatten_all_ransac_lines_from_patches(patch_results)
    # median=compute_median_distribution_coefficient(all_ransac_lines)
    
    overlay_lines_on_original_image(absolute_path,overall_clusters)

    #aggregate_lines_and_overlay(absolute_path,filtered_array_of_patches,median)

    print("%s" % (inputfilename))
    print("Complete")    
    print("----------------------------")


def overlay_lines_on_original_image(filename:str,clusters:[]):
    colors=["blue","green", "orange"]
    np_input_image=io.imread(filename,as_gray=True)
    list_of_cluster_points=[]
    for cluster in clusters:
        cluster_points=[]
        for ransac_line in cluster.ransac_lines:
            projected_inliers=ransac_line.projected_inliers
            cluster_points.extend(projected_inliers)
        list_of_cluster_points.append(cluster_points)
    np_superimposed_patches=Util.superimpose_points_on_image2(np_input_image,list_of_cluster_points,colors)

    folder_script=os.path.dirname(__file__)
    now=datetime.datetime.now()    
    #filename_result=("%s-%s.png") % (os.path.basename(filename),now.strftime("%Y-%m-%d-%H-%M-%S"))
    filename_result=("%s-%s.png") % (os.path.basename(filename),"result")
    file_result=os.path.join(folder_script,"./out/",filename_result)
    io.imsave(file_result,np_superimposed_patches)
    print("Results saved to file:%s" % (file_result))
    print("Count of clusters=%d" % (len(clusters)))

        
def overlay_lines_on_original_image_0(filename:str,clusters:[]):
    """ This function will render lines which have a distribution coefficient value above the specified threshold """
    np_input_image=io.imread(filename,as_gray=True)

    all_projections:List[Point]=list()
    count_of_lines_drawn=0
    count_of_lines_skipped=0
    for cluster in clusters:
        for ransac_line in cluster.ransac_lines:
            projected_inliers=ransac_line.projected_inliers
            all_projections.extend(projected_inliers)  
            count_of_lines_drawn+=1
            #you were here, you got 2 clusters with sine curve
            #Why two? Why so much noise? Plot every cluster with different color?
            #rotate the colors  colors.to_rgba("red")


    np_superimposed_patches=Util.superimpose_points_on_image(np_input_image,all_projections,100,255,100)

    folder_script=os.path.dirname(__file__)
    now=datetime.datetime.now()    
    filename_result=("%s-%s.png") % (os.path.basename(filename)[0:5],now.strftime("%Y-%m-%d-%H-%M-%S"))
    file_result=os.path.join(folder_script,"./out/",filename_result)
    io.imsave(file_result,np_superimposed_patches)
    print("Results saved to file:%s" % (file_result))
    print("Count of ransac lines displayed=%d" % (count_of_lines_drawn))
    print("Count of ransac lines skipped=%d" % (count_of_lines_skipped))
    pass

def process_all_files_in_folder(folder:str,patchdimension:int):
    files=listdir(folder)
    count=0
    for file in files:
        extension=os.path.splitext(files[0])[1]
        if (extension.lower() != '.png'):
            continue
        absolutepath=join(folder,file)
        process_single_file(absolutepath,patchdimension=patchdimension)
        count+=1
    print("Resized %d files" % (count))
    pass


#run("Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png", patchdimension=100)
"""
sine curve
    patchdimension=50, 30+ clusters, too many independent lines
    patchdimension=150, 5+ clusters, looks promising, but missed out the extreme left and extreme right parts of the curve. Padding might help
"""


#run("Cosine-W=500.H=200.MAXD=20.SP=0.95.9.png", patchdimension=100)
"""
cosine curve
    patchdimension=50, 50 clusters, too many noisy lines detected, full curve also detected
    patchdimension=150, 5 clusters, looks very good, no noise, full curve was detected
"""
# run("Large.SampleWith1ProminentLine.png", patchdimension=100)
#run("Cubic-W=500.H=200.MAXD=15.SP=0.90.8.png.8.png", patchdimension=100)

#run("Sine-50-percent.png", patchdimension=25) #too many lines, but the actual lines are also present
#run("Sine-50-percent.png", patchdimension=40) #better than 25
#run("Sine-50-percent.png", patchdimension=50) #gives far better results than 25 and 40
#run("Sine-50-percent.png", patchdimension=100) #No clusters were identified

process_all_files_in_folder("C:/Users/saurabhd/MyTrials/MachineLearnings-2/CurveReconstruction/Main/in/circle",patchdimension=50)