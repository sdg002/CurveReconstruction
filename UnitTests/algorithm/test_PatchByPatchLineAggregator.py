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
            
    def test_Using_LargeFile_With_2ProminentLines_And_2X2_patches_Then_ShouldReturn_2_Cluster(self):
        """
        We are testing on an image that has 2 distinct large lines
        """
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/PatchByPatchLineAggregator","SampleWith2ProminentLine.png")
        algo = PatchByPatchRansac(file_test_image)
        algo.Dimension=70
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
            bigger_cluster=None
            smaller_cluster=None
            if len(clusters[0].ransac_lines[0].inliers) > len(clusters[1].ransac_lines[0].inliers):
                bigger_cluster=clusters[0]
                smaller_cluster=clusters[1]
            else:
                bigger_cluster=clusters[1]
                smaller_cluster=clusters[0]

            slope_of_bigger_cluster=math.atan(-bigger_cluster.ransac_lines[0].line.A/bigger_cluster.ransac_lines[0].line.B) * 180/math.pi
            slope_of_smaller_cluster=math.atan(-smaller_cluster.ransac_lines[0].line.A/smaller_cluster.ransac_lines[0].line.B) * 180/math.pi

            self.assertGreaterEqual(slope_of_bigger_cluster,38,"The slope should be within expected range")
            self.assertLessEqual(slope_of_bigger_cluster,42,"The slope should be within expected range")

            self.assertGreaterEqual(slope_of_smaller_cluster,-14,"The slope should be within expected range")
            self.assertLessEqual(slope_of_smaller_cluster,-10,"The slope should be within expected range")


    def  test_find_connected_lines_in_across_all_patches_3x3patches_and_1Cluster(self):
        """
        3x3 patches
        Only diagonal patches have 2 ransac lines each
        2   0   0
        0   2   0
        0   0   2
        Overall 1 single cluster because of overallaping membership
        """
        line0=RansacLineInfo()
        line1=RansacLineInfo()
        line2=RansacLineInfo()
        line3=RansacLineInfo()
        line4=RansacLineInfo()
        line5=RansacLineInfo()

        array_of_patch_clusters=np.full((3,3), None,dtype="object")

        cluster_0_0=ConnectedLines()
        cluster_0_0.add_ransac_line(line0)
        cluster_0_0.add_ransac_line(line1)

        cluster_1_1=ConnectedLines()
        cluster_1_1.add_ransac_line(line1)
        cluster_1_1.add_ransac_line(line2)

        cluster_2_2=ConnectedLines()
        cluster_2_2.add_ransac_line(line2)
        cluster_2_2.add_ransac_line(line3)

        array_of_patch_clusters[0][0]=[cluster_0_0]
        array_of_patch_clusters[1][1]=[cluster_1_1]
        array_of_patch_clusters[2][2]=[cluster_2_2]

        patch_aggregator=PatchByPatchLineAggregator(None)
        list_of_connected_lines=patch_aggregator.find_connected_lines_in_across_all_patches(array_of_patch_clusters)
        self.assertEqual(1, len(list_of_connected_lines), '1 cluster should be returned')
        self.assertEqual(4, len(list_of_connected_lines[0].ransac_lines), 'The cluster should contain all the ransac lines')
        self.assertTrue(line0 in list_of_connected_lines[0].ransac_lines)
        self.assertTrue(line1 in list_of_connected_lines[0].ransac_lines)
        self.assertTrue(line2 in list_of_connected_lines[0].ransac_lines)
        self.assertTrue(line3 in list_of_connected_lines[0].ransac_lines)

    def  test_find_connected_lines_in_across_all_patches_4x4patches_and_2Clusters(self):
        """
        3x3 patches
        Only diagonal patches have 2 ransac lines each
        2   0   0   0
        0   1   0   0
        0   0   1   0
        0   0   0   2
        Overall 2 clusters because of interruption in the middle of the diagonal
        """
        line0=RansacLineInfo()
        line1=RansacLineInfo()
        line2=RansacLineInfo()
        line3=RansacLineInfo()
        line4=RansacLineInfo()
        line5=RansacLineInfo()

        array_of_patch_clusters=np.full((3,3), None,dtype="object")

        cluster_0_0=ConnectedLines()
        cluster_0_0.add_ransac_line(line0)
        cluster_0_0.add_ransac_line(line1)

        cluster_1_1=ConnectedLines()
        cluster_1_1.add_ransac_line(line1)

        cluster_2_2=ConnectedLines()
        cluster_2_2.add_ransac_line(line2)

        cluster_3_3=ConnectedLines()
        cluster_3_3.add_ransac_line(line2)
        cluster_3_3.add_ransac_line(line3)

        array_of_patch_clusters[0][0]=[cluster_0_0]
        array_of_patch_clusters[1][1]=[cluster_1_1]
        array_of_patch_clusters[2][2]=[cluster_2_2]
        array_of_patch_clusters[2][2]=[cluster_3_3]

        patch_aggregator=PatchByPatchLineAggregator(None)
        list_of_connected_lines=patch_aggregator.find_connected_lines_in_across_all_patches(array_of_patch_clusters)
        self.assertEqual(2, len(list_of_connected_lines), '2 cluster should be returned')
        self.assertEqual(2, len(list_of_connected_lines[0].ransac_lines), 'The cluster should contain all the ransac lines')
        self.assertEqual(2, len(list_of_connected_lines[1].ransac_lines), 'The cluster should contain all the ransac lines')

        self.assertTrue(line0 in list_of_connected_lines[0].ransac_lines)
        self.assertTrue(line1 in list_of_connected_lines[0].ransac_lines)

        self.assertTrue(line2 in list_of_connected_lines[1].ransac_lines)
        self.assertTrue(line3 in list_of_connected_lines[1].ransac_lines)

    @unittest.skip("To be done")
    def test_ImageWith2Lines(self):
        raise Exception("to be done")

if __name__ == '__main__':
    unittest.main()
