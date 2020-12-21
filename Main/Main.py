from Algorithm import ImagePatchExtractor
import os
import skimage
from skimage import io
from Common import Util
from Common import LineModel
from skimage.measure import LineModelND, ransac
import numpy as np
from Common import PatchInfo
from Common import RansacLineInfo
from Common import RansacPatchInfo
from Common import PatchResults
from Algorithm import RansacAlgorithm
from typing import Union, Any, List, Optional, cast

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
    
    pass

def process_patch2(patchinfo:PatchInfo):
    img_patchregion=patchinfo.image
    points=Util.create_points_from_numpyimage(img_patchregion)
    algo=RansacAlgorithm(points)
    ransac_lines:RansacLineInfo=algo.run()
    new_patchinfo=RansacPatchInfo(patchinfo.topleft.X,patchinfo.topleft.Y,patchinfo.bottomright.X,patchinfo.bottomright.Y )
    new_patchinfo.ransacinfo=ransac_lines  #you were here
    return new_patchinfo


run("Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png", patchdimension=25)