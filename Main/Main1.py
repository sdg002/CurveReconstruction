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

min_density:float=0
min_distribution_index:float=0

def run(inputfilename:str,patchdimension:int):
    print("Start")    
    print("----------------------------")
    print("min density:%f" % (min_density))
    print("min distribution index:%f" % (min_distribution_index))

    folder_script=os.path.dirname(__file__)
    file_noisy_curve=os.path.join(folder_script,"./in/",inputfilename)

    patch_algo=PatchByPatchRansac(file_noisy_curve)
    patch_algo.Dimension=patchdimension
    patch_algo.ransac_threshold_distance=2
    patch_results:List[RansacPatchInfo]=patch_algo.run()
    dump_info(patch_results)
    overlay_lines_on_original_image(file_noisy_curve,patch_results)

    print("%s" % (inputfilename))
    print("Complete")    
    print("----------------------------")
    

def overlay_lines_on_original_image(filename:str,patch_results:List[RansacPatchInfo]):
    np_input_image=io.imread(filename,as_gray=True)

    patch_result:RansacPatchInfo
    all_projections:List[Point]=list()
    count_of_lines=0
    for patch_result in patch_results:
        for ransac_line in patch_result.ransacinfo:

            if (ransac_line.density < min_density):
                continue

            if (ransac_line.inlier_distribution_index < min_distribution_index):
                continue

            projected_inliers=ransac_line.projected_inliers
            all_projections.extend(projected_inliers)  
            count_of_lines+=1
    np_superimposed_patches=Util.superimpose_points_on_image(np_input_image,all_projections,100,255,100)

    folder_script=os.path.dirname(__file__)
    now=datetime.datetime.now()    
    filename_result=("ransac.result-%s.png") % (now.strftime("%Y-%m-%d-%H-%M-%S"))
    file_result=os.path.join(folder_script,"./out/",filename_result)
    io.imsave(file_result,np_superimposed_patches)
    print("Results save to file:%s" % (file_result))
    print("Count of ransac lines displayed=%d" % (count_of_lines))

def dump_info(patch_results):
    print(("Found %d ransac patches") % (len(patch_results)))
    ransac_density=[]
    ransac_length=[]
    inlier_distribution_index=[]
    for patch_result in patch_results:
        print("\tpatch %s" % (patch_result))
        for ransac_line in patch_result.ransacinfo:
            print("\t\tline %s density:%f length:%f  distribution_index:%f" % (ransac_line, ransac_line.density, ransac_line.length, ransac_line.inlier_distribution_index))
            ransac_density.append(ransac_line.density)
            ransac_length.append(ransac_line.length)
            inlier_distribution_index.append(ransac_line.inlier_distribution_index)
    describe_statistics("ransac_length",ransac_length)
    describe_statistics("ransac_density",ransac_density)
    describe_statistics("inlier_distribution_index",inlier_distribution_index)

    pass

def describe_statistics(label:str,observations:[]):
    print("-----------------------")
    print("displaying statistics for: %s" % (label))
    print("max      =%f" % (max(observations)))
    print("min      =%f" % (min(observations)))
    print("median   =%f" % (statistics.median(observations)))
    print("mean     =%f" % (statistics.mean(observations)))
    print("-----------------------")


min_density=0.0
min_distribution_index=0.16667

run("Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png", patchdimension=100)
#run("Cosine-W=500.H=200.MAXD=20.SP=0.95.9.png", patchdimension=100)
#run("Large.SampleWith1ProminentLine.png", patchdimension=100)

