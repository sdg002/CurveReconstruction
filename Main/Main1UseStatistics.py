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

#
#to be done - use the median calculation of Main1 and plot only "high valued" lines
#


def run(inputfilename:str,patchdimension:int):
    print("Start")    
    print("----------------------------")

    folder_script=os.path.dirname(__file__)
    absolute_path=os.path.join(folder_script,"./in/",inputfilename)

    patch_algo=PatchByPatchRansac(absolute_path)
    patch_algo.Dimension=patchdimension
    patch_algo.ransac_threshold_distance=2
    patch_results:List[RansacPatchInfo]=patch_algo.run()
    all_ransac_lines:[]=flatten_all_ransac_lines_from_patches(patch_results)
    median=compute_median_distribution_coefficient(all_ransac_lines)
    overlay_lines_on_original_image(absolute_path,patch_results,median)

    print("%s" % (inputfilename))
    print("Complete")    
    print("----------------------------")

def flatten_all_ransac_lines_from_patches(patches:List[RansacPatchInfo])->List[RansacLineInfo]:
    results=[]
    for patch_result in patches:
        print("\tpatch %s" % (patch_result))
        for ransac_line in patch_result.ransacinfo:
            print("\t\tline %s density:%f length:%f  distribution_index:%f" % (ransac_line, ransac_line.density, ransac_line.length, ransac_line.inlier_distribution_index))
            results.append(ransac_line)
    return results

def compute_median_distribution_coefficient(ransac_lines:List[RansacLineInfo])->float:
    all_coefficients=list(map(lambda  l: l.inlier_distribution_index, ransac_lines))
    return statistics.median(all_coefficients)

def overlay_lines_on_original_image(filename:str,patch_results:List[RansacPatchInfo], distribution_threshold:float):
    """ This function will render lines which have a distribution coefficient value above the specified threshold """
    np_input_image=io.imread(filename,as_gray=True)

    patch_result:RansacPatchInfo
    all_projections:List[Point]=list()
    count_of_lines_drawn=0
    count_of_lines_skipped=0
    for patch_result in patch_results:
        for ransac_line in patch_result.ransacinfo:

            if (ransac_line.inlier_distribution_index < distribution_threshold):
                count_of_lines_skipped+=1
                continue

            projected_inliers=ransac_line.projected_inliers
            all_projections.extend(projected_inliers)  
            count_of_lines_drawn+=1
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
