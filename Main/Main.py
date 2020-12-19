from Algorithm import ImagePatchExtractor
import os
import skimage
from Common import Util


print("hello world")

def run(inputfilename:str,patchdimension:int):
    stride:int=int(patchdimension/2)

    folder_script=os.path.dirname(__file__)
    file_noisy_curve=os.path.join(folder_script,"./in/",inputfilename)
    np_image=skimage.io.imread(file_noisy_curve,as_gray=True)

    xtractor=ImagePatchExtractor(np_image,patchdimension,stride)
    patch_results:PatchResults=xtractor.extract_patches();
    patchcount_x=patch_results.patch_indices.shape[1]
    patchcount_y=patch_results.patch_indices.shape[0]
    good_patches:List[_PatchAnalysis]=list()
    for x in range(0,patchcount_x):
        for y in range(0,patchcount_y):
            patchinfo:PatchInfo=patch_results.get_patch_xy(x,y)
            img_patchregion=patchinfo.image
            lst_all_points=Util.create_points_from_numpyimage(img_patchregion)
            #line=self.find_line_using_ransac(lst_all_points,img_patchregion)
            #if (line  == None):
            #    continue
            #print("Got a line X=%d Y=%d , line=%s" % (x,y, str(line)))
            ##add to a collection of patch regions+ransacline
            #patch_analysis_result=_PatchAnalysis(patchinfo,lst_all_points,line)
            #good_patches.append(patch_analysis_result)
    pass

run("Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png", patchdimension=25)