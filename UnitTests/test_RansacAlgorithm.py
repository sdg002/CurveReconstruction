import unittest
from Algorithm import RansacAlgorithm
import skimage
from skimage import io
import os
from Common import Util
from typing import Union, Any, List, Optional, cast
from Common import RansacLineInfo
class Test_testRansac(unittest.TestCase):
    """Unit tests for Ransac algorithm """



    def test_RansacCtor(self):
        width=100
        height=200
        algo=RansacAlgorithm(width,height,[])
        self.assertEqual(algo.Width, width, 'Width of the image should match')
        self.assertEqual(algo.Height, height, 'Width of the image should match')
        self.assertEqual(type(algo.Width),float, 'The type should be float')
        self.assertEqual(type(algo.Height),float, 'The type should be float')
        self.assertEqual(algo.ThresholdDistance, 10, 'The threshold distance should be correctly initialized')

    def test_WhenImage_HasOneProminentLine_Then_1_LineShouldBe_Returned(self):
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/","SampleWith1ProminentLine.png")
        np_image=io.imread(file_test_image,as_gray=True)
        width=np_image.shape[1]
        height=np_image.shape[0]
        points=Util.create_points_from_numpyimage(np_image)

        algo=RansacAlgorithm(width,height,points)
        results:List[RansacLineInfo]=algo.run()
        self.assertEqual(len(results), 1, 'message')
        first_line:RansacLineInfo=results[0]
        self.assertGreaterEqual(len(first_line.inliers), 10, 'Inliers should be correctly detected')
        self.assertLessEqual(len(first_line.inliers), 11, 'Inliers should be correctly detected')
        pass

    def test_When_Image_Has_LessThan2Points_Then_Zero_LinesShould_Be_Returned(self):
        algo=RansacAlgorithm(20,20,[])
        results:List[RansacLineInfo]=algo.run()
        self.assertEqual(len(results), 0, 'Zero ransac lines should be returned')



    
if __name__ == '__main__':
    unittest.main()