from Common import Point
from typing import Union, Any, List, Optional, cast
from Common import RansacLineInfo
from Common import LineModel
from Common import Point


class RansacAlgorithm(object):
    """implementation of Ransac algorithm"""
    def __init__(self,width:float, height:float,points:List[Point]):
        self.Points=points
        self.Width=width
        self.Height=height
        pass


    def run(self)->List[RansacLineInfo]:
        linePerp:RansacLineInfo=RansacLineInfo()
        linePerp.line = LineModel(1,0,-self.Width/2)
        linePerp.inliers=[Point(self.Width/2,0),Point(self.Width/2, self.Height)]

        lineHor=RansacLineInfo()
        lineHor.line = LineModel(0,1,-self.Height/3)
        lineHor.inliers = [Point(0,self.Height/3), Point(self.Width,self.Height/3)]
        return [linePerp,lineHor]

