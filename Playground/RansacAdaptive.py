from operator import mod
from Common.Point import Point
import numpy as np
import os
from skimage import io
from Common import Util
from sklearn.neighbors import KDTree
import statistics
from skimage.measure import LineModelND, ransac
import datetime
from scipy import stats

def run(inputfilename:str):
    print("-------------------------------------------")
    print("Processing input file %s" % (inputfilename))
    folder_script=os.path.dirname(__file__)
    file_noisy_curve=os.path.join(folder_script,"./in/",inputfilename)
    np_image=io.imread(file_noisy_curve,as_gray=True)
    width=np_image.shape[1]
    height=np_image.shape[0]

    points=Util.create_points_from_numpyimage(np_image)

    # robustly fit line only using inlier data with RANSAC algorithm
    arr_x=list(map(lambda p: p.X, points))
    arr_y=list(map(lambda p: p.Y, points))
    points_array=np.column_stack((arr_x,arr_y))
    tree = KDTree(points_array)
    nearest_dist, nearest_ind = tree.query(points_array, k=2)
    nne_distances=list(nearest_dist[0:,1:].flatten())
    mean=statistics.mean(nne_distances)
    #mode=statistics.mode(nne_distances)
    mode=stats.mode(nne_distances)[0]
    stdev=statistics.stdev(nne_distances)
    print("Count of points=%d" % (len(points_array)))
    print("Mean=%f, Mode=%f, Stddev=%f" % (mean,mode, stdev))
    #
    #Now do the RANSAC
    #
    #I tried mode-stdev, but this produced near zero threshold for LineSample2.png
    distance_from_line=mode *.5
    min_samples=3
    model_robust, inliers = ransac(points_array, LineModelND, min_samples=min_samples,
                                   residual_threshold=distance_from_line, max_trials=1000)
    #
    #Generate points on the RANSAC line
    #
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
    filename_result=("adaptive-%s-threshold-%d-minsamples-%d-inliers-%d.result.png") % (filename_noextension,distance_from_line,min_samples,count_of_inliers)
    file_result=os.path.join(folder_script,"./out/",filename_result)

    np_superimposed=Util.superimpose_points_on_image(np_image,new_points,100,255,100)
    io.imsave(file_result,np_superimposed)
    pass

    pass

#
#
#
run("LineSample1.png")
run("LineSample2.png")
run("LineSample3.png")