#
#Obejctives
#   Generate a noisy image (salt pepper) , but do not use Scikitimage
#   Use a 100x100 image
#   Generate several images with increasing probability of noise from 0.1 to 0.9
#   For every image find average nearest neighbour distance and mean nearest neighbour distance between points using KdTree


import numpy as np
import os
import random
from skimage import io

class NoisyImageGenerator(object):
    """Generators an monochrome image with the specified amounts of Salt-peper noise"""

    def __init__(self, width:float, height:float,salt_pepper:float):
        super(NoisyImageGenerator, self).__init__()
        self.__salt_pepper = salt_pepper
        self.__width=width
        self.__height=height
        self.__filename=None

    def generate(self):
        self.__noisy_image = np.zeros([self.__height,self.__width,1],dtype=np.uint8)
        height=self.__noisy_image.shape[0]
        width=self.__noisy_image.shape[1]
        for y in range(0,height):
            for x in range(0,width):
                r=random.random()
                if (r > self.__salt_pepper):
                    self.__noisy_image[y][x][0]=0
                else:
                    self.__noisy_image[y][x][0]=255
        return self.__noisy_image

    @property
    def noisy_image(self):
        """Returns the noisy image."""
        return self.__noisy_image

    @property
    def median(self):
        """The median of the nearest neighbour distance of all the points."""
        return self.__median

    @property
    def filename(self):
        """Returns the filename where the newly generated noisy image was saved."""
        return self.__filename

    def save_to_subfolder(self, subfolder:str):
        folder_script=os.path.dirname(__file__)
        folder_results=os.path.join(folder_script,"./out/")
        filename= ("%s-%.3f.png") % ("NoisyImage", self.__salt_pepper)
        absolute_filepath=os.path.join(folder_script,"./out/",filename)
        io.imsave(absolute_filepath,self.__noisy_image)
        self.__filename=absolute_filepath
        pass        

class NearestNeighbour(object):
    """Manages the statistics for the nearest neighbour distance between points"""
    def __init__(self, image:np.ndarray):
        super(NearestNeighbour, self).__init__()
        self.__image = image

    @property
    def median(self):
        """The median property."""
        return -1

    @property
    def mean(self):
        """The mean property."""
        return  -1

sp_ratios=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


def generate_noisy_images(salt_pepper:list):
    """ Generates sample images with the salt pepper rations in the given list """
    for sp_ratio in sp_ratios:
        image_generator=NoisyImageGenerator(width=100, height=100,salt_pepper=sp_ratio)
        noisy_image=image_generator.generate()
        nn_statistics=NearestNeighbour(noisy_image)
        median=nn_statistics.median
        average=nn_statistics.mean
        image_generator.save_to_subfolder(subfolder="out")
        print("filename=%s  median distance=%f  average distance=%f" % (image_generator.filename,median,average))
        #Perform RANSAC on noisy_image

    pass

generate_noisy_images(sp_ratios)



#    you were here - do the Kd tree thing, fill in mean and median


