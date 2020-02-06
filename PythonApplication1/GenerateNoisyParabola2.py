#
#This script will 
#   *)generate a random parabola in a 
#   *)scatter the picture with salt-pepper noise
#
import numpy as np
import os
import skimage
import Util
import random
from common.Point import Point
#from common.GenGaussianNoise import GenGaussianNoise #importing from subfolder did not work! Why?
import GenGaussianNoise as gaussianxy
import math

#as gaussianxy
#
#Create blank image
#

img_back_color=255
img_width=100
img_height=50
num_points=30
img = np.zeros([img_height,img_width,1],dtype=np.uint8)
img.fill(img_back_color)
#
#Generate Salt-Pepper noise
#
salt_pepper_ratio=0.01
#0.2
#0.01
image_noisy=skimage.util.random_noise(img,mode="s&p",seed=None, clip=True,salt_vs_pepper=salt_pepper_ratio)
#
#Generate points using the equation of the Parabola
#
origin_x=img_width*0.5
origin_y=img_height*0.25
lst_points=list()
multiplier=random.random()*(0.1) + 0.01 #a random number which controls the shape of the parabola
print("Random multiplier=%f" % (multiplier))

#for x in range(0,img_width):
#    y=multiplier*pow((x - origin_x),2) + origin_y
#    pt=Point(x,y)
#    lst_points.append(pt)
def Parabola(x:float)->float:
    y=multiplier*pow((x - origin_x),2) + origin_y
    return y
    pass
#########
#Objetive  - 
#   smoothen out the parabola
#   begin with lowest x, compute y, x+deltaX, compute y, compute distance, if more than threshold than x+0.5deltax
#   if less than threshold then x+0.25deltax

min_distance=4 # we expect 2 points to be not any more further than this
x_current=0
y_current=Parabola(x_current)
point_last=Point(x_current,y_current)
delta_x=1
lst_points.append(point_last)
while (x_current <= img_width):
    y_current = Parabola(x_current)
    distance=math.sqrt( (point_last.X - x_current)**2 + (point_last.Y - y_current)**2)
    if (distance > min_distance):
        #select this point
        pt=Point(x_current,y_current)
        lst_points.append(pt)
        x_current=x_current+1
        point_last=pt
    else:
        #too close , move on to the next point
        x_current=x_current+1
#
#Generate noisy around the Parabola
#
stddev=5
#2
#3 was too sparse
#2 looks more sparse
#1
num_noisy_points=20
#1 worked best
#0
#5
#20
lst_points_with_noise=list()
for pt_original in lst_points:
    print(pt_original)
    arr_cluster=gaussianxy.GenerateClusterOfRandomPointsAroundXY(pt_original.X,pt_original.Y,stddev,num_noisy_points)
    cluster_shape=arr_cluster.shape
    #lst_points_with_noise.append(pt_original) #Not adding original point
    for idx in range(0,cluster_shape[0]):
        x_cluster=arr_cluster[idx][0]; 
        y_cluster=arr_cluster[idx][1];
        if (x_cluster < 0 ) or (x_cluster >= img_width):
            continue
        if (y_cluster < 0 ) or (y_cluster >= img_height):
            continue

        pt_new=Point(x_cluster,y_cluster)
        lst_points_with_noise.append(pt_new)


image_result=Util.superimpose_points_on_image(image_noisy,lst_points_with_noise,0,0,0)
#
#Save the image to disk
#
folder_script=os.path.dirname(__file__)
folder_results=os.path.join(folder_script,"./out/")
count_of_files=len(os.listdir(folder_results))

filename=("NoisyParabola.%d.png" % count_of_files)
file_result=os.path.join(folder_script,"./out/",filename)
skimage.io.imsave(file_result,image_result)
print("Image saved to fileL%s" % (file_result))
