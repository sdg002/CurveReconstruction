import numpy as np
import statistics
from typing import Union, Any, List, Optional, cast, Dict
from Common import RansacPatchInfo

class PatchByPatchStatisticalFilter():
    """
    Filter the results of PatchByPatchRansac to eliminate noisy ransac lines.
    The broader objective of this class is to have a place holder with different means of filtering
    """
    def __init__(self, array_of_patches:np.ndarray):
        """
        array_of_patches: 2 dimensional numpy array containing instances of 'RansacPatchInfo' class
        """
        self.__array_of_patches=array_of_patches
        self.__flattened_array=None
        self.__flattened_ransac_lines=None
        
    def null_filter(self)->np.ndarray:
        """
        Null filter - Does not filter. Returns a new 2d numpy array with the same shape as input
        The array members is a list of RansacLineInfo instances
        """
        y_max=self.__array_of_patches.shape[0]
        x_max=self.__array_of_patches.shape[1]
        result=np.empty((y_max,x_max),dtype='object')

        for x in range(0,x_max):
            for y in range(0,y_max):
                current_patch:RansacPatchInfo  =self.__array_of_patches[y][x]
                result[y][x]=current_patch.ransacinfo
        return result

    def filter_using_median_distributionindex(self)->np.ndarray:
        """
        Returns a new 2d numpy array with the same shape as the input
        However, the array members are just list of RansacLineInfo instances which meet the criteria
        """
        all_coefficients=list(map(lambda  l: l.inlier_distribution_index, self.flattened_ransac_lines))
        if (len(all_coefficients)==0):
            return 0
        median=statistics.median(all_coefficients)

        y_max=self.__array_of_patches.shape[0]
        x_max=self.__array_of_patches.shape[1]
        result=np.empty((y_max,x_max),dtype='object')

        for x in range(0,x_max):
            for y in range(0,y_max):
                current_patch:RansacPatchInfo  =self.__array_of_patches[y][x]
                existing_ransac_lines=current_patch.ransacinfo
                good_ransac_lines=list(filter(lambda  l: l.inlier_distribution_index >= median, existing_ransac_lines))
                result[y][x]=good_ransac_lines

        return result

    @property
    def flattened_patches(self):
        """Returns a flat list of RansacPatchInfo instances."""
        if (self.__flattened_array != None):
            return self.__flattened_array
        self.__flattened_array=list(self.__array_of_patches.flatten())
        return self.__flattened_array
        
    @property
    def flattened_ransac_lines(self):
        """All ransac lines from all the patches collected in a single List."""
        if (self.__flattened_ransac_lines != None):
            return self.__flattened_ransac_lines
        results=[]
        for patch_result in self.flattened_patches:
            for ransac_line in patch_result.ransacinfo:
                results.append(ransac_line)

        self.__flattened_ransac_lines=results        
        return self.__flattened_ransac_lines
