from .LineModel import LineModel
from .Point import Point
from typing import Union, Any, List, Optional, cast
from Common import Util

class RansacLineInfo(object):
    """Represents all information of a single Line that has been determined via Ransac algo"""
    def __init__(self):
        self._line:LineModel=None
        self._inliers=[]
        self._projected_inliers=None #Projecton of inlier points on the Ransac line
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

    @property
    def projected_inliers(self)->List[Point]:
        """Returns the projection of inlier points on the ransac line."""
        if (self._projected_inliers==None):
            #do the computation here
            self._projected_inliers=Util.generate_plottable_points_from_projection_of_points(self.line,self.inliers)
        return self._projected_inliers
