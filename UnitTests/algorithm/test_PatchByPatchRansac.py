import unittest
from Algorithm import PatchByPatchRansac
from Common import RansacPatchInfo
from Common import RansacLineInfo
from Common import Point
from typing import Union, Any, List, Optional, cast
import os
import numpy as np


class Test_PatchByPatchRansac(unittest.TestCase):
    def test_Constructor(self):
        algo = PatchByPatchRansac("somefile")
        self.assertEqual(algo.Dimension, 0, 'Dimension of the patch must be initialized to zero')
        pass

    def test_WithLargeFile(self):
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/PatchByPatchRansac","Large.SampleWith1ProminentLine.png")
        algo = PatchByPatchRansac(file_test_image)
        algo.Dimension=80
        algo.ransac_threshold_distance=7
        ransac_patches=algo.run()
        self.assertEqual(len(ransac_patches), 12, '12 patches expected when image dimensions are 200X150 and patch size is 80')

        all_inliers:List[Point]=list()
        for patch_result in ransac_patches:
            for ransac_line in patch_result.ransacinfo:
                #projected_inliers=ransac_line.projected_inliers
                #all_projections.extend(projected_inliers)
                all_inliers.extend(ransac_line.inliers)


        all_Y=list(map(lambda point: point.Y, all_inliers))
        all_X=list(map(lambda point: point.X, all_inliers))

        self.assertGreaterEqual(min(all_X), 100, 'All ransac inliers must be greater than this value')
        self.assertLessEqual(max(all_X), 200, 'All ransac inliers must be less than this value')

        self.assertGreaterEqual(min(all_Y), 0, 'All ransac inliers must be greater than this value')
        self.assertLessEqual(max(all_Y), 70, 'All ransac inliers must be less than this value')

        #Repeat the above assetions with projected inliers
        all_projections:List[Point]=list()
        for patch_result in ransac_patches:
            for ransac_line in patch_result.ransacinfo:
                all_projections.extend(ransac_line.projected_inliers)

        all_Y=list(map(lambda point: point.Y, all_projections))
        all_X=list(map(lambda point: point.X, all_projections))

        self.assertGreaterEqual(min(all_X), 100, 'All projected points must be greater than this value')
        self.assertLessEqual(max(all_X), 200, 'All projected points must be less than this value')

        self.assertGreaterEqual(min(all_Y), 0, 'All projected points must be greater than this value')
        self.assertLessEqual(max(all_Y), 70, 'All projected points must be less than this value')


        #The ransac line must be correctly identified
        line_withmax_inliers:RansacLineInfo=max(ransac_patches[11].ransacinfo,key=lambda l: len(l.inliers))
        x_intercept=-line_withmax_inliers.line.C/line_withmax_inliers.line.A
        y_intercept=-line_withmax_inliers.line.C/line_withmax_inliers.line.B
        self.assertGreaterEqual(x_intercept,100, 'The X intercept should be correct')
        self.assertLessEqual(x_intercept,110, 'The X intercept should be correct')
        self.assertLess(y_intercept,0, "Y intercept should be negative")
        pass

    def test_WithLargeFile_3HorizontalPoints(self):
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/PatchByPatchRansac","Large.Samplewith1HorLine.png")
        algo = PatchByPatchRansac(file_test_image)
        algo.Dimension=80
        algo.ransac_threshold_distance=7
        ransac_patches=algo.run()
        self.assertEqual(len(ransac_patches), 4, '4 patches expected when image dimensions are 100X100 and patch size is 80')

        one_only_one_line = ransac_patches[3].ransacinfo[0]
        self.assertEqual(len(one_only_one_line.inliers), 3, '3 inlier points expected')
        self.assertLessEqual(abs(one_only_one_line.line.A),0.001,"The one and only one line is horizontal")

    def test_WithLargeFile_3VerticalPoints(self):
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/PatchByPatchRansac","Large.Samplewith1VertLine.png")
        algo = PatchByPatchRansac(file_test_image)
        algo.Dimension=80
        algo.ransac_threshold_distance=7
        ransac_patches=algo.run()
        self.assertEqual(len(ransac_patches), 4, '4 patches expected when image dimensions are 100X100 and patch size is 80')

        one_only_one_line = ransac_patches[3].ransacinfo[0]
        self.assertEqual(len(one_only_one_line.inliers), 3, '3 inlier points expected')
        self.assertLessEqual(abs(one_only_one_line.line.B),0.001,"The one and only one line is vertical")

    def test_method_run1_using_LargeFile_pathcdimension_80(self):
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/PatchByPatchRansac","Large.SampleWith1ProminentLine.png")
        algo = PatchByPatchRansac(file_test_image)
        algo.Dimension=80
        algo.ransac_threshold_distance=7
        arr:np.ndarray=algo.run1()
        self.assertEqual(3,arr.shape[0] , 'The shape of the array must be equal to the number of cells along Y axis')
        self.assertEqual(4,arr.shape[1] , 'The shape of the array must be equal to the number of cells along Y axis')

    def test_method_run1_using_LargeFile_pathcdimension_100(self):
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/PatchByPatchRansac","Large.SampleWith1ProminentLine.png")
        algo = PatchByPatchRansac(file_test_image)
        algo.Dimension=100
        algo.ransac_threshold_distance=7
        arr:np.ndarray=algo.run1()
        self.assertEqual(2,arr.shape[0] , 'The shape of the array must be equal to the number of cells along Y axis')
        self.assertEqual(3,arr.shape[1] , 'The shape of the array must be equal to the number of cells along Y axis')


if __name__ == '__main__':
    unittest.main()
