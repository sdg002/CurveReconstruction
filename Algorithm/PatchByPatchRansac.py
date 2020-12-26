from Common import RansacPatchInfo
from Algorithm import ImagePatchExtractor
from skimage import io
from Common import PatchResults
from typing import Union, Any, List, Optional, cast
from Common import PatchInfo
from Common import Util
from Common import Point
from Common import LineModel
from Algorithm import RansacAlgorithm
from Common import RansacLineInfo

class PatchByPatchRansac(object):
    """Implements Ransacl algorithm by splitting a large image into patches"""
    def __init__(self, inputfile):
        self._inputfile = inputfile
        self._Dimension=0
        self._np_image=None
        self._image_width=float(0)
        self._image_height=float(0)

    @property
    def Dimension(self)->int:
        """The size of the patch."""
        return self._Dimension

    @Dimension.setter
    def Dimension(self, value:int):
        self._Dimension = int(value)

    def __read_image(self):
        self._np_image=io.imread(self._inputfile,as_gray=True)
        self._image_height=self._np_image.shape[0]
        self._image_width=self._np_image.shape[1]

    def run(self)->List[RansacPatchInfo]:
        if (self.Dimension <= 0):
            raise ValueError("The Dimension should be a positive value")
        self.__read_image()
        stride=int(self.Dimension/2)
        xtractor=ImagePatchExtractor(self._np_image,self.Dimension,stride)
        patch_results:PatchResults=xtractor.extract_patches()
        patchcount_x=patch_results.patch_indices.shape[1]
        patchcount_y=patch_results.patch_indices.shape[0]
        ransac_patches:List[RansacPatchInfo]=list()
        for x in range(0,patchcount_x):
            for y in range(0,patchcount_y):
                patchinfo:PatchInfo=patch_results.get_patch_xy(x,y)
                ransac_patch:RansacPatchInfo=self.__find_ransac_lines(patchinfo)
                ransac_patches.append(ransac_patch)
                print("\tpatch, x=%d, y=%d info=%s" % (x,y,ransac_patch))
        return self.__translate_from_patch_coordinate2parent(ransac_patches)

    def __translate_from_patch_coordinate2parent(self,raw_patches:List[RansacPatchInfo])->List[RansacPatchInfo]:
        #
        #see the working on paper - 
        #what are we doing? The coordinate system still remains Cartesian. We are only translating the origin from Patch to Main image
        #
        results:List[RansacPatchInfo]=[]
        for original_patch_info in raw_patches:
            new_patchinfo=RansacPatchInfo(original_patch_info.topleft.X,original_patch_info.topleft.Y,original_patch_info.bottomright.X,original_patch_info.bottomright.Y)
            new_ransaclines:List[RansacLineInfo]=[]
            for orginal_line in original_patch_info.ransacinfo:
                new_ransacline:RansacLineInfo=RansacLineInfo()
                new_inliers:List[Point]=[]
                for original_inlier in orginal_line.inliers:
                    new_X=new_patchinfo.topleft.X+original_inlier.X
                    new_Y= (self._image_height - new_patchinfo.bottomright.Y) + original_inlier.Y
                    new_inlier:Point=Point(new_X, new_Y)
                    new_inliers.append(new_inlier)
                new_line_model=self.__translate_line_model_to_parent_coordinates(orginal_line.line,original_patch_info)
                new_ransacline.line=new_line_model
                new_ransacline.inliers=new_inliers
                #Step 1 - you will need to handle the Line translation otherwise projected points will give inacurate results
                #Step 2 - all original points should be translated too, write a reusable function
                new_ransaclines.append(new_ransacline)
            new_patchinfo.ransacinfo=new_ransaclines
            results.append(new_patchinfo)
        return results

    def __translate_line_model_to_parent_coordinates(self, old_model:LineModel,patch:RansacPatchInfo)->LineModel:
        """
        Translates a ransac line from the reference frame of the patch to that of the parent image
        """
        if (old_model.B ==0):
            #perpendicular line
            b_new=0
            a_new=1
            delta_origin_x = patch.topleft.X
            old_xintercept=-old_model.C/old_model.A
            c_new=-(delta_origin_x +old_xintercept)
            return LineModel(a_new, b_new, c_new)
        else:
            new_xintercept= (-old_model.C/old_model.A) + patch.topleft.X
            new_xintercept_y=(self._image_height - patch.bottomright.Y)

            new_yintercept= (-old_model.C/old_model.B) + (self._image_height - patch.bottomright.Y)
            new_yintercept_x = patch.topleft.X
            return LineModel.create_line_from_2points(new_xintercept,new_xintercept_y, new_yintercept_x,new_yintercept)
        pass
    def __find_ransac_lines(self,patchinfo:PatchInfo)->RansacPatchInfo:
        img_patchregion=patchinfo.image
        height=img_patchregion.shape[0]
        width=img_patchregion.shape[1]
        points=Util.create_points_from_numpyimage(img_patchregion)
        algo=RansacAlgorithm(width,height,points)
        ransac_lines:List[RansacLineInfo]=algo.run()
        new_patchinfo:RansacPatchInfo=RansacPatchInfo(patchinfo.topleft.X,patchinfo.topleft.Y,patchinfo.bottomright.X,patchinfo.bottomright.Y )
        new_patchinfo.ransacinfo=ransac_lines
        new_patchinfo.allpoints=points
        return new_patchinfo
