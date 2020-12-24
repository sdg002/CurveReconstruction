import numpy as np
from Common import PolarLineModel

class HoughAccumator(object):
    """Represents a 2d array. Theta along one axis and Rho along another axis"""
    def __init__(self, diag_len:float):
        thetas = np.arange(-90.0, +89.0)
        num_thetas=len(thetas)
        self.__accumulator=np.zeros((2 * int(diag_len), num_thetas), dtype=np.uint64)
        pass
    

    def add_polar_line(self, polar_line:PolarLineModel):
        """
        Increments the vote count of the accumulator cell which matches the specified polar line
        """
        pass
