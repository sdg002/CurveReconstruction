import unittest
from Algorithm import PatchByPatchRansac
import os
from Common import RansacPatchInfo
from Common import RansacLineInfo
from typing import Union, Any, List, Optional, cast
from Common import Point

class Test_PatchByPatchRansac(unittest.TestCase):
    def test_Constructor(self):
        algo = PatchByPatchRansac("somefile")
        self.assertEqual(algo.Dimension, 0, 'Dimension of the patch must be initialized to zero')
        pass

    def test_WithLargeFile(self):
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/","Large.SampleWith1ProminentLine.png")
        algo = PatchByPatchRansac(file_test_image)
        algo.Dimension=80
        ransac_patches=algo.run()
        self.assertEqual(len(ransac_patches), 12, '12 patches expected when image dimensions are 200X150 and patch size is 80')

        #all_projections:List[Point]=list()
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

        line_withmax_inliers:RansacLineInfo=max(ransac_patches[11].ransacinfo,key=lambda l: len(l.inliers))
        x_intercept=-line_withmax_inliers.line.C/line_withmax_inliers.line.A
        y_intercept=-line_withmax_inliers.line.C/line_withmax_inliers.line.B
        self.assertGreaterEqual(x_intercept,100, 'The X intercept should be correct')
        self.assertLessEqual(x_intercept,110, 'The X intercept should be correct')
        self.assertLess(y_intercept,0, "Y intercept should be negative")


        pass
    
if __name__ == '__main__':
    unittest.main()
