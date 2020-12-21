from Common import Point
from typing import Union, Any, List, Optional, cast
from Common import RansacLineInfo


class RansacAlgorithm(object):
    """implementation of Ransac algorithm"""
    def __init__(self,points:List[Point]):
        self.Points=points
        pass


    def run(self)->List[RansacLineInfo]:
        line1=RansacLineInfo()
        line2=RansacLineInfo()
        return [line1,line2]

