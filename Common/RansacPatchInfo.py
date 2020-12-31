from .RansacLineInfo import RansacLineInfo
from typing import Union, Any, List, Optional, cast
from .Point import Point


class RansacPatchInfo(object):
    """This class captures information about all Ransac generated lines in a given patch region of the original image"""

    def __init__(self,topleft_x,topleft_y,bottomright_x,bottomright_y):
        self._topleft=Point(topleft_x,topleft_y)
        self._bottomright=Point(bottomright_x,bottomright_y)
        self._tag=None
        self._ransacinfo:List[RansacLineInfo]=[]
        self._allpoints:List[Point]=[]
        self.x=-1 #The zero based index of the patch element along X axis
        self.y=-1 #The zero based index of the patch element along Y axis


    @property
    def topleft(self):
        return self._topleft

    @property
    def bottomright(self):
        return self._bottomright

    @property
    def tag(self):
        """Getter property to retrieve any user defined information"""
        return self._tag

    @tag.setter
    def tag(self,tag):
        """Setter property to set any user defined information"""
        self._tag=tag

    @property
    def ransacinfo(self)->List[RansacLineInfo]:
        return self._ransacinfo

    @ransacinfo.setter
    def ransacinfo(self,ransaclines:List[RansacLineInfo]):
        """Sets all the ransac lines in this patch"""
        self._ransacinfo=ransaclines

    @property
    def allpoints(self):
        """The Point objects in the image that were used for ransac calculations"""
        return self._allpoints

    @allpoints.setter
    def allpoints(self, value):
        self._allpoints = value

    def __str__(self):
        display= self.__repr__()
        return display

    def __repr__(self):
        display= ("topleft=(%d,%d)  bottomright=(%d,%d)  count of ransac lines=%d") % (self.topleft.X,self.topleft.Y,self.bottomright.X,self.bottomright.Y, len(self.ransacinfo))
        return display



