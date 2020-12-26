from Algorithm import ImagePatchExtractor
import os
import skimage
from skimage import io
from Common import Util
from Common import LineModel
from Common import Point
from skimage.measure import LineModelND, ransac
import numpy as np
from Common import PatchInfo
from Common import RansacLineInfo
from Common import RansacPatchInfo
from Common import PatchResults
from Algorithm import RansacAlgorithm
from typing import Union, Any, List, Optional, cast
import datetime

print("hello world")

def run(inputfilename:str,patchdimension:int):
    stride:int=int(patchdimension/2)

    folder_script=os.path.dirname(__file__)
    file_noisy_curve=os.path.join(folder_script,"./in/",inputfilename)
    np_image=io.imread(file_noisy_curve,as_gray=True)

    xtractor=ImagePatchExtractor(np_image,patchdimension,stride)
    patch_results:PatchResults=xtractor.extract_patches()
    patchcount_x=patch_results.patch_indices.shape[1]
    patchcount_y=patch_results.patch_indices.shape[0]
    ransac_patches:List[RansacPatchInfo]=list()
    for x in range(0,patchcount_x):
        for y in range(0,patchcount_y):
            patchinfo:PatchInfo=patch_results.get_patch_xy(x,y)
            ransac_patch:RansacPatchInfo=process_patch2(patchinfo)            
            ransac_patches.append(ransac_patch)
            print("\tpatch, x=%d, y=%d info=%s" % (x,y,ransac_patch))
    overlay_results(inputfilename,ransac_patches)
    pass

def process_patch2(patchinfo:PatchInfo):
    img_patchregion=patchinfo.image
    height=img_patchregion.shape[0]
    width=img_patchregion.shape[1]
    points=Util.create_points_from_numpyimage(img_patchregion)
    algo=RansacAlgorithm(width,height,points)
    ransac_lines:RansacLineInfo=algo.run()
    new_patchinfo=RansacPatchInfo(patchinfo.topleft.X,patchinfo.topleft.Y,patchinfo.bottomright.X,patchinfo.bottomright.Y )
    new_patchinfo.ransacinfo=ransac_lines  #you were here
    return new_patchinfo

def overlay_results(inputfilename:str,ransac_patches:List[RansacPatchInfo]):
    folder_script=os.path.dirname(__file__)
    file_noisy_curve=os.path.join(folder_script,"./in/",inputfilename)
    np_input_image=io.imread(file_noisy_curve,as_gray=True)

    now=datetime.datetime.now()
    filename_result=("ransac.result-%s.png") % (now.strftime("%Y-%m-%d-%H-%M-%S"))
    file_result=os.path.join(folder_script,"./out/",filename_result)

    lst_allpoints_from_all_patches:List[Point]=list()
    #
    #loop here
    #
    image_height=np_input_image.shape[0]
    ransac_patch:RansacPatchInfo
    for ransac_patch in ransac_patches:
        ransac_line:RansacLineInfo
        patch_height= ransac_patch.bottomright.Y-ransac_patch.topleft.Y
        for ransac_line in ransac_patch.ransacinfo:          
            plottable_points=Util.generate_plottable_points_from_projection_of_points(ransac_line.line,ransac_line.inliers)
            for plottable_point in plottable_points:
                new_x=ransac_patch.topleft.X + plottable_point.X
                new_y=(image_height-ransac_patch.topleft.Y-patch_height) + plottable_point.Y
                translated_point=Point(new_x,new_y)
                lst_allpoints_from_all_patches.append(translated_point)

    np_superimposed_patches=Util.superimpose_points_on_image(np_input_image,lst_allpoints_from_all_patches,100,255,100)
    skimage.io.imsave(file_result,np_superimposed_patches)
    print("Results save to file:%s" % (file_result))

    pass

#run("Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png", patchdimension=50)
#run("Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png", patchdimension=100)
run("Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png", patchdimension=200)
#run("Cubic-W=500.H=200.MAXD=15.SP=0.90.3.png.3.png", patchdimension=50)

