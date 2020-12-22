'''
Demonstrates how to use Scikit RANSAC library
on a simple image
'''
import numpy as np
from matplotlib import pyplot as plt

from skimage.measure import LineModelND, ransac
import os
from skimage import io
from Common import Util
from Common import Point
import math
import datetime

def run(inputfilename:str):
    folder_script=os.path.dirname(__file__)
    file_noisy_curve=os.path.join(folder_script,"./in/",inputfilename)
    np_image=io.imread(file_noisy_curve,as_gray=True)
    width=np_image.shape[1]
    height=np_image.shape[0]
    points=Util.create_points_from_numpyimage(np_image)

    # robustly fit line only using inlier data with RANSAC algorithm
    arr_x=list(map(lambda p: p.X, points))
    arr_y=list(map(lambda p: p.Y, points))
    np_data_points=np.column_stack((arr_x,arr_y))
    diagonal=math.sqrt( width*width +height*height )
    distance_from_line=diagonal/16
    min_samples=3
    model_robust, inliers = ransac(np_data_points, LineModelND, min_samples=min_samples,
                                   residual_threshold=distance_from_line, max_trials=1000)

    line_x = np.arange(0, width)
    line_y = model_robust.predict_y(line_x)

    file_result=os.path.join(folder_script,"./out/",inputfilename)
    new_points=[]
    for i in range(0,len(line_x)):
        pt=Point(line_x[i], line_y[i])
        new_points.append(pt)


    filename_noextension=os.path.splitext(inputfilename)[0]
    now=datetime.datetime.now()
    count_of_inliers=len(list(map(lambda x: x==True, inliers)))
    filename_result=("%s-%s-threshold-%d-minsamples-%d-inliers-%d.result.png") % (filename_noextension,now.strftime("%Y-%m-%d-%H-%M-%S"),distance_from_line,min_samples,count_of_inliers)
    file_result=os.path.join(folder_script,"./out/",filename_result)

    np_superimposed=Util.superimpose_points_on_image(np_image,new_points,100,255,100)
    io.imsave(file_result,np_superimposed)
    pass




run("LineSample1.png")
run("LineSample2.png")
run("LineSample3.png")
pass
