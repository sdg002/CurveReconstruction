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

def run(inputfilename:str,patchdimension:int):
    folder_script=os.path.dirname(__file__)
    file_noisy_curve=os.path.join(folder_script,"./in/",inputfilename)

    patch_algo=PatchByPatchRansac(file_noisy_curve)
    patch_algo.Dimension=patchdimension
    patch_algo.ransac_threshold_distance=2
    patch_results:List[RansacPatchInfo]=patch_algo.run()
    dump_info(patch_results)
    overlay_lines_on_original_image(file_noisy_curve,patch_results, min_density=0.085246)
    
    

def overlay_lines_on_original_image(filename:str,patch_results:List[RansacPatchInfo], min_density=0):
    np_input_image=io.imread(filename,as_gray=True)

    patch_result:RansacPatchInfo
    all_projections:List[Point]=list()
    count_of_lines=0
    for patch_result in patch_results:
        for ransac_line in patch_result.ransacinfo:
            if (ransac_line.density < min_density):
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
    print("Count of ransac lines=%d" % (count_of_lines))

def dump_info(patch_results):
    print(("Found %d ransac patches") % (len(patch_results)))
    ransac_density=[]
    for patch_result in patch_results:
        print("\tpatch %s" % (patch_result))
        for ransac_line in patch_result.ransacinfo:
            print("\t\tline %s density:%f" % (ransac_line, ransac_line.density))
            ransac_density.append(ransac_line.density)
    print("max ransac density=%f" % (max(ransac_density)))
    print("min ransac density=%f" % (min(ransac_density)))
    print("median ransac density=%f" % (statistics.median(ransac_density)))
    pass


run("Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png", patchdimension=100)
#run("Large.SampleWith1ProminentLine.png", patchdimension=100)

