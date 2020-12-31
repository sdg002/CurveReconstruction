from .RansacLineInfo import RansacLineInfo
from .RansacPatchInfo import RansacPatchInfo
from typing import List, Set, Dict, Tuple, Optional

class ConnectedLines(object):
    """Represents a collection of ransac lines which are very similar, i.e. nearly coincident."""
    def __init__(self):
        # self.x=-1   #zero based index of the top left patch along X (left to right)
        # self.y=-1   #zero based index of the top left patch along Y (top to bottom)
        self.__member_ransac_patches:List[RansacPatchInfo]=[] #The ransac patches which yielded the connected lines in this object
        self.__ransac_lines:List[RansacLineInfo]=[] #The ransac lines which are connected
        pass

    def __repr__(self):
        return ("Count of connected lines=%d" % (len(self.ransac_lines)))

    def add_ransac_line(self,line:RansacLineInfo):
        self.__ransac_lines.append(line)

    @property
    def ransac_lines(self):
        """Returns the ransac lines that are members of this cluster."""
        return self.__ransac_lines
