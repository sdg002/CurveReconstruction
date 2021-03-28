#
#Obejctives
#   Generate a noisy image (salt pepper) , but do not use Scikitimage
#   Use a 100x100 image
#   Generate several images with increasing probability of noise from 0.1 to 0.9
#   For every image find average nearest neighbour distance and mean nearest neighbour distance between points using KdTree


from typing import List
import numpy as np
import os
import random
from numpy.core.fromnumeric import mean
from skimage import io
from sklearn.neighbors import KDTree
import math
import statistics
import matplotlib.pyplot as plt

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
    def __init__(self, width:int, height:int,salt_pepper:float):
        super(NearestNeighbour, self).__init__()
        self.__salt_pepper = salt_pepper
        self.__width=width
        self.__height=height
        self.__randomarray=None #Numpy array of random points. N by 2
        self.__nearest_distances=[]
        self.__median:float=math.nan
        self.__mean:float=math.nan


    def generate_random_points(self):
        count_of_pepper_points=int((1-self.__salt_pepper) * self.__width * self.__height)
        self.__randomarray=np.random.random((count_of_pepper_points,2))*self.__width

    def compute_nearest_neighbours(self):
        tree = KDTree(self.__randomarray)
        nearest_dist, nearest_ind = tree.query(self.__randomarray, k=2)  # k=2 nearest neighbors where k1 = identity
        #you were here , the element nearest_dist[i][1] gives you the nearest distance of the first point
        self.__nearest_distances=list(nearest_dist[0:,1:].flatten())
        pass

    def compute_statistics(self, iterations:int):
        """ Repeat the experiment of generating random points and computing the mean NN distance several times"""
        mean_values=[]
        median_values=[]
        for i in range(0,iterations):
            self.generate_random_points()
            self.compute_nearest_neighbours()
            median=statistics.median(self.__nearest_distances)
            median_values.append(median)

            mean=statistics.mean(self.__nearest_distances)
            mean_values.append(mean)
        self.__mean=statistics.mean(mean_values)
        self.__median=statistics.mean(median_values)

    @property
    def median(self):
        """The median of the nearest neighbour distance of all the points."""
        return self.__median

    @property
    def mean(self):
        """The mean of the nearest neighbour distance of all the points."""
        return  self.__mean

##########################################################


sp_ratios=np.arange(0.01,1,0.001)
median_results=[]
mean_results=[]
#[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.91, 0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99]


def generate_noisy_images(salt_pepper:list):
    """ Generates sample images with the salt pepper rations in the given list """
    for sp_ratio in salt_pepper:
        image_generator=NoisyImageGenerator(width=100, height=100,salt_pepper=sp_ratio)
        noisy_image=image_generator.generate()
        image_generator.save_to_subfolder(subfolder="out")
        print("filename=%s " % (image_generator.filename))
        #Perform RANSAC on noisy_image

    pass

def compute_statistics_nearest_neighbour_distance(salt_pepper:list):
    for sp_ratio in salt_pepper:
        nn_statistics=NearestNeighbour(width=100,height=100,salt_pepper=sp_ratio)
        # nn_statistics.generate_random_points()
        # nn_statistics.compute_nearest_neighbours();
        nn_statistics.compute_statistics(iterations=10)
        median=nn_statistics.median
        average=nn_statistics.mean
        print("salt-pepper ratio=%f median=%f mean=%f" % (sp_ratio, median, average))
        median_results.append(median)
        mean_results.append(mean)
    pass

def plot(salt_pepper:List, medians:List, means:List):
    plt.scatter(sp_ratios,median_results, marker='.', s=5)
    plt.grid(b=True, which='major', color='#666666', linestyle='-')

    plt.show()
    pass

#generate_noisy_images(sp_ratios)
compute_statistics_nearest_neighbour_distance(salt_pepper=sp_ratios)
plot(sp_ratios, median_results, mean_results)



