import unittest
from typing import Union, Any, List, Optional, cast
from Common import LineModel
from Common import Point
from Common import PolarLineModel
import math

class Test_TestPolarCoordinates(unittest.TestCase):
    """Unit tests for polar coordinate coversion."""


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

    def test_Line_With_30degrees_InclinationToXAxis(self):
        test_models=[]
        expected_polar_models=[]

        test_models.append(LineModel(-0.577,-1,1))
        expected_polar_models.append(tuple((0.866,1.0472)))

        test_models.append(LineModel(+0.577,-1,1))
        expected_polar_models.append(tuple((0.866,2.094)))

        test_models.append(LineModel(-0.577,-1,-1))
        expected_polar_models.append(tuple((0.866,4.1889)))    

        for test_index in range(0,len(test_models)):
            test_model=test_models[test_index]
            actual_polar_line=PolarLineModel.generate_polar_equation(test_model)

            expected_polar=expected_polar_models[test_index]
            self.assertAlmostEqual(actual_polar_line.theta, expected_polar[1],2,'The theta of the polar equation should match')
            self.assertAlmostEqual(actual_polar_line.rho, expected_polar[0],2,'The rho of the polar equation should match')


    def test_PolarLine_Hough_Transformation(self):

        test_cases=[]
        test_cases.append((LineModel(-1,-1,+1),PolarLineModel(+0.707,+0.785),"Line with Slope 1 and passing through +1,0 and 0,+1."))
        test_cases.append((LineModel(+1,+1,+1),PolarLineModel(-0.707,+0.785),"Line with Slope 1 and passing through -1,0 and 0,-1"))
        test_cases.append((LineModel(+1,-1,+1),PolarLineModel(+0.707,-0.785),"Line with Slope 1 and passing through -1,0 and 0,+1"))
        test_cases.append((LineModel(-1,+1,+1),PolarLineModel(-0.707,-0.785),"Line with Slope 1 and passing through +1,0 and 0,-1"))

        #45 degrees=0.785 radians

        for test_index in range(0,len(test_cases)):
            test_model:LineModel=test_cases[test_index][0]
            expected_polar:PolarLineModel=test_cases[test_index][1]
            actual_polar_line=PolarLineModel.generate_polar_equation_hough(test_model)

            self.assertAlmostEqual(actual_polar_line.theta, expected_polar.theta,2,'The theta of the polar equation should match')
            self.assertAlmostEqual(actual_polar_line.rho, expected_polar.rho,2,'The rho of the polar equation should match')
            

if __name__ == '__main__':
    unittest.main()
