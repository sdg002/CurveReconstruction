import numpy as np
from matplotlib import pyplot as plt

from skimage.measure import LineModelND, ransac
import os
from skimage import io
from Common import Util
from Common import Point
import math

def run(inputfilename:str):
    folder_script=os.path.dirname(__file__)
    file_noisy_curve=os.path.join(folder_script,"./in/",inputfilename)
    np_image=io.imread(file_noisy_curve,as_gray=True)
    width=np_image.shape[1]
    height=np_image.shape[0]
    points=Util.create_points_from_numpyimage(np_image)
    new_np_image=np.zeros((np_image.shape))
    for point in points:
        new_np_image[point.Y][point.X]=1


    # robustly fit line only using inlier data with RANSAC algorithm
    diagonal=math.sqrt( width*width +height*height )
    distance_from_line=diagonal/4
    model_robust, inliers = ransac(new_np_image, LineModelND, min_samples=3,
                                   residual_threshold=distance_from_line, max_trials=1000)
    pass


run("LineSample1.png")
pass
