from .LineModel import LineModel
from .Point import Point
from typing import Union, Any, List, Optional, cast

class RansacLineInfo(object):
    """Represents all information of a single Line that has been determined via Ransac algo"""
    def __init__(self):
        self._Line:LineModel=None
        pass

    @property
    def Line(self)->LineModel:
        """The Line property."""
        return self._Line

    @Line.setter
    def Line(self, value:LineModel):
        self._Line = value   

    @property
    def inliers(self)->List[Point]:
        """Points which were determined by Ransac to be inliers."""
        return self._inliers

    @inliers.setter
    def inliers(self, value:List[Point]):
        self._inliers = value
    #you were here, implement __repr__

