import numpy as np
import os
import skimage
import random
import math
from Common import Point
from Common import Util
from skimage import io

class GenericCurveGenerator(object):
    """Generic class that abtracts the drawing of a noisy curve on a canvas of given width and height"""
    def __init__ (self,width,height):
        self._width=width
        self._height=height
        self._saltpepper=0.9
        self._img_back_color=255
        self._output_file=None
        self._max_distance_consecutive_points=10
        self.__curvetype=None
        pass

    @property
    def curvetype(self):
        return self.__curvetype

    @curvetype.setter
    def curvetype(self,value):
        if (value == "sine"):
            self.__curvetype=value
        elif (value == "cubic"):
            self.__curvetype=value
        elif (value == "cosine"):
            self.__curvetype=value
        elif (value == "parabola"):
            self.__curvetype=value
        elif (value == "spiral"):
            self.__curvetype=value
        else:
            raise Exception("This curve type is not implemented:%s" % (value))
        
    
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self,value):
        self._width=value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self,value):
        self._height=value

    @property
    def saltpepper(self):
        return self._saltpepper

    @saltpepper.setter
    def saltpepper(self,value):
        self._saltpepper=value

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self,value):
        self._output_file=value
    
    @property
    def max_consecutive_distance(self):
        return self._max_distance_consecutive_points

    @max_consecutive_distance.setter
    def max_consecutive_distance(self,value):
        self._max_distance_consecutive_points=value

    def __generate_blankimage_with_saltpepper_noise(self):
        #width,height,saltpepper_noise
        img = np.zeros([self.height,self.width,1],dtype=np.uint8)
        img.fill(self._img_back_color)
        image_noisy=skimage.util.random_noise(img,mode="s&p",seed=None, clip=True,salt_vs_pepper=self.saltpepper)
        return image_noisy

    #
    #Generate X,Y values using custom function and superimpose over image 
    #max_distance=max distance betwen 2 consecutive points
    #
    def __generate_xy_from_custom_function(self,image_array):
        max_distance=self._max_distance_consecutive_points
        x_start=0
        width=image_array.shape[1]
        height=image_array.shape[0]
        x_end=width
        y_origin=height/2

        delta_x=width*0.25 #an approx gap to being with
        x_last=x_start
        y_last=self.__InvokeAnyFunction(x_last ,width=width,height=height)+y_origin #add a new private functoin and property to decide which type of curve
        pts_new=list();
        while(x_last<x_end):
            gap=delta_x
            while(True):
                x_new=x_last+gap
                y_new=self.__InvokeAnyFunction(x_new,width=width,height=height)+y_origin
                dsquare=(x_new-x_last)**2 + (y_new-y_last)**2
                d=dsquare**0.5
                if (d <= max_distance):
                    pt_new=Point(x_new,y_new)
                    pts_new.append(pt_new)
                    x_last=x_new
                    y_last=y_new
                    break
                else:
                    gap=gap*0.5 #reduce the gap and try again
                    continue
        image_result=Util.superimpose_points_on_image(image_array,pts_new, 0,0,0)
        return image_result
        pass


    def __generate_xy_from_polar_function(self,image_array):
        max_distance=self._max_distance_consecutive_points
        min_distance=max_distance/2
        width=image_array.shape[1]
        height=image_array.shape[0]

        theta=0
        delta_theta=0.1
        origin_x=width/2
        origin_y=height/2

        distance_x_at_2pie=width/10 #Where does the spiral intersect the X axis at 2pie radians
        const_a=(distance_x_at_2pie/(2*math.pi))
        pts_new=list();
        
        x_last=origin_x
        y_last=origin_y

        while (True):
            r=const_a*theta
            x=r*math.cos(theta)
            y=r*math.sin(theta)
            x_new=x+origin_x
            y_new=y+origin_y
            if (x_new > width):
                break
            if (y_new > height):
                break

            distance_from_lastpoint= ((x_new-x_last)**2 + (y_new-y_last)**2)**0.5
            if (distance_from_lastpoint < max_distance) and (distance_from_lastpoint >= min_distance):
                pt_new=Point(x_new,y_new)
                pts_new.append(pt_new)
                x_last=x_new
                y_last=y_new
                theta=theta+ delta_theta
            elif (distance_from_lastpoint < min_distance):
                delta_theta=delta_theta*1.1
                theta=theta+ delta_theta
            else:
                delta_theta= delta_theta*0.9
                theta=theta - delta_theta
            
        image_result=Util.superimpose_points_on_image(image_array,pts_new, 0,0,0)
        return image_result


    def __SineFunction(self,x, width,height):
        amplitude=height*0.5*0.9
        radians_to_pix=math.pi/2 / (height*0.25)
        theta=x*radians_to_pix
        y=math.sin(theta)*amplitude
        return y

    def __CosineFunction(self,x, width,height):
        amplitude=height*0.5*0.9
        radians_to_pix=math.pi/2 / (height*0.25)
        theta=x*radians_to_pix
        y=math.cos(theta)*amplitude
        return y

    def __CubeFunction(self,x, width,height):
        y=(x-width/2)**3
        return y/100000

    def __ParabolaFunction(self,x, width,height):
        y=0.1*(x-width/2)**2 - height/2.0
        return y


    def __InvokeAnyFunction(self,x,width,height):
        if (self.__curvetype == "sine"):
            return self.__SineFunction(x,width,height)
        elif (self.__curvetype == "cosine"):
            return self.__CosineFunction(x,width,height)
        elif (self.__curvetype == "cubic"):
            return self.__CubeFunction(x,width,height)
        elif (self.__curvetype == "parabola"):
            return self.__ParabolaFunction(x,width,height)
        else:
            raise Exception("This curve type is not implemented: %s" % (self.__curvetype))

    def generate_curve(self):
        blank_image=self.__generate_blankimage_with_saltpepper_noise()
        new_image=None
        if (self.__curvetype == "spiral"):
            new_image= self.__generate_xy_from_polar_function(blank_image)
        else:
            new_image=self.__generate_xy_from_custom_function(blank_image)
        self.__save_image_to_disk(new_image,self.output_file)
        pass

    #
    #Generates a filename derived from the properties of the class
    #Rationale - a simple way to visually trace back what was used
    #
    def generate_filename_prefix(self):
        sp_ratio=round(self.saltpepper,2)
        filename="%s.W=%d.H=%d.MAXD=%d.SP=%.2f"%(self.__curvetype,self.width,self.height,self.max_consecutive_distance,sp_ratio)
        return filename

    def __save_image_to_disk(self,image_array,filename):
        image_result=image_array
        folder_script=os.path.dirname(__file__)
        folder_results=os.path.join(folder_script,"./out/")
        count_of_files=len(os.listdir(folder_results))
        new_filename=("%s.%d.png" % (filename,count_of_files))
        file_result=os.path.join(folder_script,"./out/",new_filename)
        io.imsave(file_result,image_result)
        print("Image saved to fileL%s" % (file_result))
    