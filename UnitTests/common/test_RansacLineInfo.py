import unittest
from Common import RansacLineInfo
from Common import Point
from Common import LineModel
import math

class Test_RansacLineInfo(unittest.TestCase):
    """Unit tests for RansacInfo class"""

    def test_Basic_Construction(self):
        sut:RansacLineInfo=RansacLineInfo()
        self.assertEqual(0, len(sut.inliers), 'zero inliers should be present')
        self.assertIsNone(sut.line,"The line model should be None")
        pass

    def test_Points_Along_slanted_line_Then_Points_Must_Be_Sequenced(self):
        sut:RansacLineInfo=RansacLineInfo()
        p1=Point(10,100)
        p2=Point(20,200)
        p3=Point(30,300)
        sut.inliers=[ p2,p1,p3]
        sut.line=LineModel(1,1,1)
        sequenced_inliers=sut.sequenced_inliers
        self.assertEquals(p1, sequenced_inliers[0], 'The inliers must be sequenced')
        self.assertEquals(p3, sequenced_inliers[2], 'The inliers must be sequenced')
        self.assertEquals(p1, sut.terminal_inliers[0],"Ther terminal inlier must match")
        self.assertEquals(p3, sut.terminal_inliers[1],"Ther terminal inlier must match")

    def test_Points_Along_horizontal_line_Then_Points_Must_Be_Sequenced(self):
        sut:RansacLineInfo=RansacLineInfo()
        p1=Point(10,5)
        p2=Point(20,5)
        p3=Point(30,5)
        sut.line=LineModel(1,1,1)
        sut.inliers=[ p2,p1,p3]
        sequenced_inliers=sut.sequenced_inliers
        self.assertEquals(p1, sequenced_inliers[0], 'The inliers must be sequenced')
        self.assertEquals(p3, sequenced_inliers[2], 'The inliers must be sequenced')
        self.assertEquals(p1, sut.terminal_inliers[0],"Ther terminal inlier must match")
        self.assertEquals(p3, sut.terminal_inliers[1],"Ther terminal inlier must match")

    def test_Points_Along_vertical_line_Then_Points_Must_Be_Sequenced(self):
        sut:RansacLineInfo=RansacLineInfo()
        p1=Point(5,10)
        p2=Point(5,20)
        p3=Point(5,30)
        sut.line=LineModel(1,1,1)
        sut.inliers=[ p2,p1,p3]
        sequenced_inliers=sut.sequenced_inliers
        self.assertEquals(p1, sequenced_inliers[0], 'The inliers must be sequenced')
        self.assertEquals(p3, sequenced_inliers[2], 'The inliers must be sequenced')
        self.assertEquals(p1, sut.terminal_inliers[0],"Ther terminal inlier must match")
        self.assertEquals(p3, sut.terminal_inliers[1],"Ther terminal inlier must match")

    def test_Points_Along_45degree_line_Then_RansacLength_MustBe_CorrectlyComputed(self):
        sut:RansacLineInfo=RansacLineInfo()
        p1=Point(11,10)
        p2=Point(19,20)
        p3=Point(31,30)
        sut.line=LineModel(-1,1,0)
        sut.inliers=[ p2,p1,p3]
        computed_distance=sut.length
        actual_distance=math.sqrt((30-10)**2 + (31-11)**2)
        self.assertAlmostEqual(computed_distance,actual_distance,delta=0.01)

    def test_compute_ransac_density(self):
        sut:RansacLineInfo=RansacLineInfo()
        p1=Point(11,10)
        p2=Point(19,20)
        p3=Point(31,30)
        sut.line=LineModel(-1,1,0)
        sut.inliers=[ p2,p1,p3]
        actual_distance=math.sqrt((30-10)**2 + (31-11)**2)
        computed_density=sut.density
        actual_density=3/actual_distance
        self.assertAlmostEqual(computed_density,actual_density,delta=0.01)

if __name__ == '__main__':
    unittest.main()

