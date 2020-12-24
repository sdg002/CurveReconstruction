import unittest
from typing import Union, Any, List, Optional, cast
from Common import LineModel
from Common import Point
from Common import PolarLineModel
import math

class Test_TestPolarCoordinates(unittest.TestCase):
    """Unit tests for polar coordinate coversion."""


    # def test_LinePassing_Through_Origin_And_Slope_1(self):
    #     std_line=LineModel(-1,+1,0)
    #     polar_line=PolarLineModel.generate_polar_equation(std_line)
    #     self.assertAlmostEqual(polar_line.rho, 0, 2,'The rho of the polar equation should match')
    #     self.assertAlmostEqual(polar_line.theta, math.pi/4.0, 2,'The theta of the polar equation should match')
    #     pass

    # def test_LinePassing_Through_Origin_And_Slope_minus1(self):
    #     std_line=LineModel(+1,+1,0)
    #     polar_line=PolarLineModel.generate_polar_equation(std_line)
    #     self.assertAlmostEqual(polar_line.rho, 0, 2,'The rho of the polar equation should match')
    #     self.assertAlmostEqual(polar_line.theta, -math.pi/4.0, 2,'The theta of the polar equation should match')
    #     pass

    # def test_Line_With_YIntercept_1_And_Slope_1_ShouldHave_Negative_Rho(self):
    #     std_line=LineModel(-1,+1,-1)
    #     polar_line=PolarLineModel.generate_polar_equation(std_line)
    #     self.assertAlmostEqual(polar_line.rho, -1/math.sqrt(2),2,'The rho of the polar equation should match')
    #     self.assertAlmostEqual(polar_line.theta, math.pi/4.0, 2,'The theta of the polar equation should match')
    #     pass

    # def test_Line_With_YIntercept_1_XIntercept_minus2_ShouldHave_Negative_Rho(self):
    #     std_line=LineModel(-0.5,+1,-1)
    #     polar_line=PolarLineModel.generate_polar_equation(std_line)
    #     self.assertAlmostEqual(polar_line.rho, -1/math.sqrt(1.25),2,'The rho of the polar equation should match')
    #     self.assertAlmostEqual(polar_line.theta, 1.107, 2,'The theta of the polar equation should match')
    #     pass

    # def test_Line_With_YIntercept_minus1_XIntercept_minus2_ShouldHave_Negative_Rho(self):
    #     std_line=LineModel(-0.5,+1,+1)
    #     polar_line=PolarLineModel.generate_polar_equation(std_line)
    #     self.assertAlmostEqual(polar_line.rho, -1/math.sqrt(1.25),2,'The rho of the polar equation should match')
    #     self.assertAlmostEqual(polar_line.theta, 1.107, 2,'The theta of the polar equation should match')
    #     pass

    # def test_Line_With_YIntercept_minus1_And_Slope_1(self):
    #     std_line=LineModel(-1,+1,1)
    #     polar_line=PolarLineModel.generate_polar_equation(std_line)
    #     self.assertAlmostEqual(polar_line.rho, 1/math.sqrt(2),2,'The rho of the polar equation should match')
    #     self.assertAlmostEqual(polar_line.theta, math.pi/4.0, 2,'The theta of the polar equation should match')
    #     pass

################################
    def test_Line_With_postiveYIntercept_And_positiveXIntercept_ShouldHave_Theta_BetWeen_0And90(self):
        std_line=LineModel(+1,+1,-1)
        polar_line=PolarLineModel.generate_polar_equation(std_line)
        self.assertAlmostEqual(polar_line.rho, 1/math.sqrt(2),2,'The rho of the polar equation should match')
        self.assertAlmostEqual(polar_line.theta, math.pi/4,2,'The rho of the polar equation should match')
        pass

    def test_Line_With_postiveYIntercept_And_negativeXIntercept_ShouldHave_Theta_BetWeen_90And180(self):
        std_line=LineModel(+1,-1,+1)
        polar_line=PolarLineModel.generate_polar_equation(std_line)
        self.assertAlmostEqual(polar_line.rho, 1/math.sqrt(2),2,'The rho of the polar equation should match')
        self.assertAlmostEqual(polar_line.theta, math.pi/4 + math.pi/2,2,'The rho of the polar equation should match')
        pass

    def test_Line_With_negativeYIntercept_And_negativeXIntercept_ShouldHave_Theta_BetWeen_90And270(self):
        std_line=LineModel(+1,+1,+1)
        polar_line=PolarLineModel.generate_polar_equation(std_line)
        self.assertAlmostEqual(polar_line.rho, 1/math.sqrt(2),2,'The rho of the polar equation should match')
        self.assertAlmostEqual(polar_line.theta, math.pi/4 + math.pi,2,'The rho of the polar equation should match')
        pass

    def test_Line_With_negativeYIntercept_And_positiveXIntercept_ShouldHave_Theta_BetWeen_270And360(self):
        std_line=LineModel(+1,-1,-1)
        polar_line=PolarLineModel.generate_polar_equation(std_line)
        self.assertAlmostEqual(polar_line.rho, 1/math.sqrt(2),2,'The rho of the polar equation should match')
        self.assertAlmostEqual(polar_line.theta, math.pi/4 + math.pi + math.pi/2,2,'The rho of the polar equation should match')
        pass

if __name__ == '__main__':
    unittest.main()
