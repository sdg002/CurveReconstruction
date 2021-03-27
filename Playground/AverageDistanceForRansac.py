#
#What was I thinking?
#Given any image which has some salt-pepper noise, can we find the best fitting line using RANSAC by automatically detecting the 'threshold' parameter
#

from os.path import basename
from typing import Match
import numpy as np
from numpy.lib.npyio import save
import skimage
import os
from skimage import io
import math
import statistics


def generate_noisy_image(width:int, salt_pepper:float):
    white_color=255
    img = np.zeros([width,width,1],dtype=np.uint8)
    img.fill(white_color)
    img=skimage.util.random_noise(img,mode="s&p",seed=None, clip=True,salt_vs_pepper=salt_pepper)
    return img


def compute_mutual_distances(image:np.ndarray):
    all_black_indices=np.where(image < 1)
    x_values=all_black_indices[1]
    y_values=all_black_indices[0]
    total_black_points=len(x_values)
    distances=[]
    for i in range(0,total_black_points):
        for j in range(i+1,total_black_points):
            x1=x_values[i]
            x2=x_values[j]
            y1=y_values[i]
            y2=y_values[j]
            distance= math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
            distances.append(distance)
    return distances

def find_ransac_model(image:np.ndarray, threshold:float):
    return None

def save_image(image:np.ndarray,filename):
    folder_script=os.path.dirname(__file__)
    folder_results=os.path.join(folder_script,"./out/")
    absolute_filepath=os.path.join(folder_script,"./out/",filename)
    io.imsave(absolute_filepath,image)
    print("Image saved to fileL%s" % (absolute_filepath))
    pass

def generate_filename(basename:str,salt_pepper:float):
    return ("%s-%.3f.png") % (basename, salt_pepper)

salt_pepper=0.9
print("Generating noisy image with salt_pepper=%f" % (salt_pepper))
noisy_image=generate_noisy_image(100,salt_pepper=salt_pepper)
#
#Save noisy image
#
new_filename=generate_filename(basename="original", salt_pepper=salt_pepper)
save_image(image=noisy_image,filename=new_filename)
#
#Compute average distance
#
print("Computing average distance between the points")
distances=compute_mutual_distances(image=noisy_image)
print("Calculated %d distances" % (len(distances)))
average_distance=statistics.mean(distances)
median_distance=statistics.median(distances)
print("Average distance=%f, Median distance=%f" % (average_distance,median_distance))

#You have reached here. The mean and median is about 50.0
# Plot a histogram of the distances and find the distribution
# Also find the closest point for every point
# Look at Kdtree https://scipy-cookbook.readthedocs.io/items/KDTree_example.html
# The salt-pepper does not work as I thought - you may have to roll your own algorithm

#You were here
#Decinde on the fraction of pepper points
#Generat an image with approximately these many pepper points (see SaltPepperNoise.py)
#
#
exit()
#
#Generate RANSAC mdoel
#
all_thresholds=[ 0.5*average_distance , 0.6*average_distance]
threshold=1.5*average_distance
model=find_ransac_model(image=noisy_image,threshold=threshold)

