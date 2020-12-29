from .LineModel import LineModel
from .Point import Point
from typing import Union, Any, List, Optional, cast
from Common import Util
import math
import numpy as np

class RansacLineInfo(object):
    """Represents all information of a single Line that has been determined via Ransac algo"""
    def __init__(self):
        self._line:LineModel=None
        self._inliers=[]
        self._projected_inliers=None #Projecton of inlier points on the Ransac line (used for display only , ignore otherwise)
        self._arranged_inliers=None
        self._length=-1
        self._inlier_distribution_index=-1
        self._bin_width=0
        self._projected_inliers2=None #Projecton of inlier points on the Ransac line

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

    @property
    def terminal_inliers(self):
        """The first and last inlier points when arranged sequentially along the ransacline."""
        sequenced_inliers=self.sequenced_inliers
        return [sequenced_inliers[0], sequenced_inliers[len(sequenced_inliers)-1]]

    @property
    def sequenced_inliers(self):
        """Inlier points re-ordered along ransac line"""
        if (self._arranged_inliers != None):
            return self._arranged_inliers

        if (len(self.inliers)<2):
            raise Exception("Inliers should be set before terminal points can be calcualted")
        if (self._line == None):
            raise Exception("The Ransac line model should be set before terminal points can be calculated")
        
        all_x=list(map(lambda  p: p.X, self.inliers))
        min_x=min(all_x)
        max_x=max(all_x)

        all_y=list(map(lambda  p: p.Y, self.inliers))
        min_y=min(all_y)
        max_y=max(all_y)

        if (max_y-min_y > max_x-min_x):
            #use Y
            self._arranged_inliers=sorted(self.inliers, key=lambda p:p.Y)
        else:
            #use X
            self._arranged_inliers=sorted(self.inliers, key=lambda p:p.X)
        return self._arranged_inliers

    @property
    def length(self):
        """The length of the Ransac line calculated as the distance between the projection of the terminal inliers on the Ransac line"""
        if (self._length != -1):
            return self._length
        first_terminal_point=self.sequenced_inliers[0]
        last_terminal_point=self.sequenced_inliers[len(self.sequenced_inliers)-1]
        projected_terminal_points=LineModel.compute_projection_of_points(self.line,[first_terminal_point,last_terminal_point])

        euclidean_distance=math.sqrt((projected_terminal_points[0].X-projected_terminal_points[1].X)**2 + (projected_terminal_points[0].Y-projected_terminal_points[1].Y)**2)
        self._length=euclidean_distance
        return self._length

    @property
    def density(self):
        """The ratio of the count of inliers to the length of the Ransac line segment."""
        return len(self.inliers)/self.length

    @property
    def inlier_distribution_index(self):
        """The ratio of bins which have 1 or more projected inliers to total number of bins on the line segment between the projected terminal points"""
        if (self.bin_width ==0):
            raise Exception("The bin_width property should be set before the inliers can be distributed into bins")            

        if (self._inlier_distribution_index != -1):
            return self._inlier_distribution_index
        distances_from_first_terminal_point:List[float]=[]
                
        first_terminal_point=self.sequenced_inliers[0]
        for projected_point in self.projected_inliers2:
            distance_from_first_terminal_point=Point.euclidean_distance(first_terminal_point,projected_point)
            t_value=distance_from_first_terminal_point
            distances_from_first_terminal_point.append(t_value)
        
        #adding the bin_width to the end value of the bin to ensure inclusion
        bins=np.arange(0,self.length+self.bin_width,self.bin_width) 
        histogram=np.histogram(a=distances_from_first_terminal_point, bins=bins,density=False)
        total_bins=len(histogram[0])
        total_occupied_bins=np.count_nonzero(histogram[0])
        self._inlier_distribution_index=total_occupied_bins/total_bins
        return self._inlier_distribution_index

    @property
    def projected_inliers2(self):
        """ Returns the projection of every inlier on the ransac line"""
        if (self._projected_inliers2 != None):
            return self._projected_inliers2
        self._projected_inliers2=LineModel.compute_projection_of_points(self.line,self.sequenced_inliers)
        return self._projected_inliers2

    @property
    def bin_width(self):
        """The size of the bin on the ransac line which will be used for binning the projection of the inliers"""
        return self._bin_width

    @bin_width.setter
    def bin_width(self, value):
        self._bin_width = value
