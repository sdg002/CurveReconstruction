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

def run(inputfilename:str,patchdimension:int):
    folder_script=os.path.dirname(__file__)
    file_noisy_curve=os.path.join(folder_script,"./in/",inputfilename)
    np_input_image=io.imread(file_noisy_curve,as_gray=True)

    patch_algo=PatchByPatchRansac(file_noisy_curve)
    patch_algo.Dimension=patchdimension
    patch_results:List[RansacPatchInfo]=patch_algo.run()
    dump_info(patch_results)
    patch_result:RansacPatchInfo
    all_projections:List[Point]=list()
    for patch_result in patch_results:
        for ransac_line in patch_result.ransacinfo:
            projected_inliers=ransac_line.projected_inliers
            #projected_inliers=ransac_line.inliers
            all_projections.extend(projected_inliers)  

    np_superimposed_patches=Util.superimpose_points_on_image(np_input_image,all_projections,100,255,100)
    
    now=datetime.datetime.now()    
    filename_result=("ransac.result-%s.png") % (now.strftime("%Y-%m-%d-%H-%M-%S"))
    file_result=os.path.join(folder_script,"./out/",filename_result)
    io.imsave(file_result,np_superimposed_patches)
    print("Results save to file:%s" % (file_result))
    

def dump_info(patch_results):
    print(("Found %d ransac patches") % (len(patch_results)))
    for patch_result in patch_results:
        print("\tpatch %s" % (patch_result))
        for ransac_line in patch_result.ransacinfo:
            print("\t\tline %s" % (ransac_line))
    pass


run("Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png", patchdimension=100)
run("Large.SampleWith1ProminentLine.png", patchdimension=100)

