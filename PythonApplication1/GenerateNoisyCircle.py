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
#0.05 not much difference from 0.1
#0.1 looks good
#0.4
#0.2
image_noisy=skimage.util.random_noise(img,mode="s&p",seed=None, clip=True,salt_vs_pepper=salt_pepper_ratio)
#
#Generate points using the equation of the Circle
#
radius=min(img_height, img_width)/2.0
origin_x=img_width*0.5
origin_y=img_height*0.5
lst_points=list()
deg_per_radian=360/(math.pi*2.0)
delta_theta_degrees=5
delta_theta_radians=delta_theta_degrees * 1/deg_per_radian
theta=0.0;
while (theta <= (2*math.pi)):
    x=(math.cos(theta) * radius) + origin_x
    y=(math.sin(theta) * radius) + origin_y
    pt=Point(x,y)
    lst_points.append(pt)
    print("Angle=%f Point=%s" % ((theta * deg_per_radian),pt))
    theta+=delta_theta_radians

#
#Generate noisy around the Parabola
#
stddev=1
num_noisy_points=1
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

filename=("NoisyCircle.%d.png" % count_of_files)
file_result=os.path.join(folder_script,"./out/",filename)
skimage.io.imsave(file_result,image_result)
print("Image saved to fileL%s" % (file_result))
