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
image_noisy=skimage.util.random_noise(img,mode="s&p",seed=None, clip=True,salt_vs_pepper=0.2)
#
#Generate points using the equation of the Parabola
#
origin_x=img_width*0.5
origin_y=img_height*0.25
lst_points=list()
multiplier=random.random()*(0.1) + 0.01 #a random number which controls the shape of the parabola
print("Random multiplier=%f" % (multiplier))
for x in range(0,img_width):
    y=multiplier*pow((x - origin_x),2) + origin_y
    pt=Point(x,y)
    lst_points.append(pt)

image_result=Util.superimpose_points_on_image(image_noisy,lst_points,0,0,0)
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
