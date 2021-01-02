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
#
#In this script, 
#   Step 1 - the median value of the distribution coefficient is first calculated and only lines which are above this value are selected
#   Step 2 - Similar lines from adjacent patches are discovered and an attempt is made to connect these lines
#


def run(inputfilename:str,patchdimension:int):
    print("Start")    
    print("----------------------------")

    folder_script=os.path.dirname(__file__)
    absolute_path=os.path.join(folder_script,"./in/",inputfilename)

    patch_algo=PatchByPatchRansac(absolute_path)
    patch_algo.Dimension=patchdimension
    patch_algo.ransac_threshold_distance=2
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


run("Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png", patchdimension=100)
run("Cosine-W=500.H=200.MAXD=20.SP=0.95.9.png", patchdimension=100)
run("Large.SampleWith1ProminentLine.png", patchdimension=100)
run("Cubic-W=500.H=200.MAXD=15.SP=0.90.8.png.8.png", patchdimension=100)
