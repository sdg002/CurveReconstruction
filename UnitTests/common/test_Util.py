import unittest
from Common import Util
from Common import Point
import os
import skimage
from skimage import io
import numpy as np

class Test_Util(unittest.TestCase):

    #
    #Use a simple image to test the loading of points
    #
    def test_create_points_from_numpyimage_dtype_is_float(self):
        folder_script=os.path.dirname(__file__)
        filename="Util_unittest_dtype_float.png"
        file_noisy_line=os.path.join(folder_script,"./data/",filename)
        np_image=skimage.io.imread(file_noisy_line,as_gray=True)
        height=np_image.shape[0]
        width=np_image.shape[1]
        self.assertEqual('float', np_image.dtype, 'The dtype should be float')
        self.assertGreaterEqual(0, np_image.min(), 'The min value of the color of any pixel should be greater than 0')
        self.assertLessEqual(1, np_image.max(), 'The max value of the color of any pixel should be less than 1')

        lst_points=Util.create_points_from_numpyimage(np_image)
        self.assertEqual(len(lst_points) , 3)

        for pt_any in lst_points:
            if pt_any.X == 0 and pt_any.Y == height-1:
                pass
            elif (pt_any.X == width-1 and pt_any.Y == height-1):
                pass
            elif (pt_any.X == width-1 and pt_any.Y == 0):
                pass
            else:
               raise Exception("Point '%s' was not expected." % (pt_any))

    def test_create_points_from_numpyimage_dtype_is_uint8(self):
        folder_script=os.path.dirname(__file__)
        filename="Util_unittest_dtype_uint8.png"
        file_noisy_line=os.path.join(folder_script,"./data/",filename)
        np_image=skimage.io.imread(file_noisy_line,as_gray=True)
        height=np_image.shape[0]
        width=np_image.shape[1]
        self.assertEqual('uint8', np_image.dtype, 'The dtype should be uint8')
        self.assertGreaterEqual(0, np_image.min(), 'The min value of the color of any pixel should be greater than 0')
        self.assertLessEqual(255, np_image.max(), 'The max value of the color of any pixel should be less than 1')

        lst_points=Util.create_points_from_numpyimage(np_image)
        self.assertLessEqual(len(lst_points) , 400)
        self.assertGreaterEqual(len(lst_points) , 300)

        for pt_any in lst_points:
            if pt_any.X >= width:
                raise Exception("Point '%s' was not expected." % (pt_any))
            elif (pt_any.Y >= height):
                raise Exception("Point '%s' was not expected." % (pt_any))
            elif (pt_any.X <0 or pt_any.Y < 0):
                raise Exception("Point '%s' was not expected." % (pt_any))
            else:
               pass

    def test_superimpose_single_set_of_points_on_image(self):
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/","SampleWith1ProminentLine.png")
        np_image=io.imread(file_test_image,as_gray=True)

        values=list(np.arange(10,20,1))
        points=list(map(lambda  v: Point(v,v),values))
        superimposed_image=Util.superimpose_points_on_image2(np_image,[points],["yellow"])

        filename_result="result_single_set.png"
        file_result=os.path.join(folder_script,"./data/out/",filename_result)
        io.imsave(file_result,superimposed_image)

    def test_superimpose_single_multiple_sets_of_points_on_image(self):
        folder_script=os.path.dirname(__file__)
        file_test_image=os.path.join(folder_script,"./data/","SampleWith1ProminentLine.png")
        np_image=io.imread(file_test_image,as_gray=True)

        count_of_points_collection=4
        colors=["red","yellow","blue"]
        sets_of_points=[]
        for i in range(1, count_of_points_collection+1):
            values=list(np.arange(10*(i-1)+25,10*i+25,1))
            points=list(map(lambda  v: Point(v,v),values))
            sets_of_points.append(points)

        superimposed_image=Util.superimpose_points_on_image2(np_image,sets_of_points,colors)

        filename_result="result_multiple_sets_of_points.png"
        file_result=os.path.join(folder_script,"./data/out/",filename_result)
        io.imsave(file_result,superimposed_image)


if __name__ == '__main__':
    unittest.main()
