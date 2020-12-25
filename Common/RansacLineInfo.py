from .LineModel import LineModel
from .Point import Point
from typing import Union, Any, List, Optional, cast

class RansacLineInfo(object):
    """Represents all information of a single Line that has been determined via Ransac algo"""
    def __init__(self):
        self._line:LineModel=None
        self._inliers=[]
        pass

    @property
    def line(self)->LineModel:
        """The equation of the line determined by Ransac."""
        return self._line

    @line.setter
    def line(self, value:LineModel):
        self._line = value   

    @property
    def inliers(self)->List[Point]:
        """Points which were determined by Ransac to be inliers."""
        return self._inliers

    @inliers.setter
    def inliers(self, value:List[Point]):
        self._inliers = value
    
    def __repr__(self):
        display=("Count of inliers=%d , Line=%s")%(len(self.inliers),self.line)
        return display

