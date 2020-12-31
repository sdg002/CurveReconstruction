import unittest
from Algorithm import RansacAlgorithm
from Algorithm import PatchByPatchRansac
from Algorithm import PatchByPatchLineAggregator
from Algorithm import PatchByPatchStatisticalFilter
from skimage import io
from Common import Util
from Common import RansacLineInfo
from Common import ConnectedLines
import numpy as np
import skimage
import os
from typing import Union, Any, List, Optional, cast
import math



class Test_PatchByPatchLineAggregator(unittest.TestCase):
    """unit tests for the class  PatchByPatchLineAggregator."""

    def test_ConstructorTests(self):
        some_array=np.ones((4,4))
        sut=PatchByPatchLineAggregator(some_array)
        self.assertTrue(np.array_equal(some_array, sut.patches), 'the property patches must have been set')
        self.assertEqual(sut.theta_threshold,0)
        self.assertEqual(sut.rho_threshold,0)
        pass        

    def test_Using_LargeFile_With_1ProminentLine_And_2X2_patches_Then_ShouldReturn_1_Cluster(self):
        """ We are doing a basic test with just 1 set of 4 patches"""
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/PatchByPatchLineAggregator","LargeDiagonalLine.png")
        algo = PatchByPatchRansac(file_test_image)
        algo.Dimension=120
        algo.ransac_threshold_distance=7
        array_of_patches:np.ndarray=algo.run1()
        self.assertEqual(2,array_of_patches.shape[0] , 'The shape of the array must be equal to the number of cells along Y axis')
        self.assertEqual(2,array_of_patches.shape[1] , 'The shape of the array must be equal to the number of cells along Y axis')

        filter_handler=PatchByPatchStatisticalFilter(array_of_patches)
        filtered_array_of_patches=filter_handler.null_filter()

        patch_aggregator=PatchByPatchLineAggregator(filtered_array_of_patches)
        patch_aggregator.rho_threshold=algo.ransac_threshold_distance
        patch_aggregator.theta_threshold= 10 * math.pi/180 #10 degrees        
        array_of_patches=patch_aggregator.find_connected_lines_in_adjacent_patches()
        flat_array_of_patches=array_of_patches.flatten()

        self.assertEqual(1, len(flat_array_of_patches), '1 resulting patch = (2-1)*(2-1)')
        for clusters in flat_array_of_patches:
            for cluster in clusters:
                for rasac_line in cluster.ransac_lines:
                    slope=-rasac_line.line.A/rasac_line.line.B
                    angle=math.atan(slope) * 180/math.pi
                    self.assertGreaterEqual(angle,44,"The slope should be about 45 degrees")
                    self.assertLessEqual(angle,46,"The slope should be about 45 degrees")

    def test_Using_LargeFile_With_1ProminentLine_And_3X3_patches_Then_ShouldReturn_1_Cluster(self):
        """ We are doing a expanding on the basic test by testing on 3X3 patches """
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/PatchByPatchLineAggregator","LargeDiagonalLine.png")
        algo = PatchByPatchRansac(file_test_image)
        algo.Dimension=80
        algo.ransac_threshold_distance=2
        array_of_patches:np.ndarray=algo.run1()
        self.assertEqual(3,array_of_patches.shape[0] , 'The shape of the array must be equal to the number of cells along Y axis')
        self.assertEqual(3,array_of_patches.shape[1] , 'The shape of the array must be equal to the number of cells along Y axis')

        filter_handler=PatchByPatchStatisticalFilter(array_of_patches)
        filtered_array_of_patches=filter_handler.null_filter()

        patch_aggregator=PatchByPatchLineAggregator(filtered_array_of_patches)
        patch_aggregator.rho_threshold=algo.ransac_threshold_distance
        patch_aggregator.theta_threshold= 5 * math.pi/180 #5 degrees
        array_of_patches=patch_aggregator.find_connected_lines_in_adjacent_patches()
        array_of_patches=array_of_patches.flatten()

        self.assertEqual(4, len(array_of_patches), '4 resulting patches = (3-1)*(3-1)')
        for clusters in array_of_patches:
            self.assertEqual(1, len(clusters), 'We expect only 1 cluster of lines, i.e. the prominent large line')
            for cluster in clusters:
                for rasac_line in cluster.ransac_lines:
                    slope=-rasac_line.line.A/rasac_line.line.B
                    angle=math.atan(slope) * 180/math.pi
                    self.assertGreaterEqual(angle,44,"The slope should be about 45 degrees")
                    self.assertLessEqual(angle,55,"The slope should be about 45 degrees")

    def test_Using_LargeFile_With_1ProminentLine_And_1ShortLine_And_2X2_patches_Then_ShouldReturn_1_Cluster(self):
        """ 
        We are testing on a picture which has 1 prominent diagnoal line and 1 small line 
        We should expect 2 clusters of lines.
        """
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/PatchByPatchLineAggregator","LargeDiagonalLine_1ShortLine.png")
        algo = PatchByPatchRansac(file_test_image)
        algo.Dimension=120
        algo.ransac_threshold_distance=2
        array_of_patches:np.ndarray=algo.run1()
        self.assertEqual(2,array_of_patches.shape[0] , 'The shape of the array must be equal to the number of cells along Y axis')
        self.assertEqual(2,array_of_patches.shape[1] , 'The shape of the array must be equal to the number of cells along Y axis')

        filter_handler=PatchByPatchStatisticalFilter(array_of_patches)
        filtered_array_of_patches=filter_handler.filter_using_median_distributionindex()

        patch_aggregator=PatchByPatchLineAggregator(filtered_array_of_patches)
        patch_aggregator.rho_threshold=algo.ransac_threshold_distance
        patch_aggregator.theta_threshold= 10 * math.pi/180 #10 degrees
        array_of_patches=patch_aggregator.find_connected_lines_in_adjacent_patches()
        flat_array_of_patches=array_of_patches.flatten()

        self.assertEqual(1, len(flat_array_of_patches), '1 resulting patches = (2-1)*(2-1)')
        for clusters in flat_array_of_patches:
            self.assertEqual(2, len(clusters), 'We expect 2 cluster of lines, i.e. a cluster with prominent large line and a cluster with the shorter line')
            cluster_with_max_inliers= clusters[0] if len(clusters[0].ransac_lines[0].inliers) > len(clusters[1].ransac_lines[0].inliers) else clusters[1]
            for rasac_line in cluster_with_max_inliers.ransac_lines:
                slope=-rasac_line.line.A/rasac_line.line.B
                angle=math.atan(slope) * 180/math.pi
                self.assertGreaterEqual(angle,44,"The slope should be about 45 degrees")
                self.assertLessEqual(angle,46,"The slope should be about 45 degrees")
            
    @unittest.skip("To be done")
    def test_Using_LargeFile_With_2ProminentLines_And_2X2_patches_Then_ShouldReturn_1_Cluster(self):
        raise Exception("Not yet implemented")

if __name__ == '__main__':
    unittest.main()
