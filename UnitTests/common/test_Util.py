import unittest
from Common import Util
from Common import Point
import os
from skimage import io
import numpy as np

class Test_Util(unittest.TestCase):

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
