'''

Numpy convolution
-----------------
    a1=np.arange(4).reshape([2,2])
    k=np.ones([2,2])
    ndimage.convolve(a1,k, mode='constant', cval=0.0)
    #When cval=0, then the extra padding is assumed to have a value of 0
    #Works well, but there is no way to apply a stride
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.convolve.html

OpenCV filter method
--------------------
    Can be used but no way to apply a stride

What was I thinking?
--------------------
    Do manual convolution
    use ndimage.convolution
    This might be good https://medium.com/analytics-vidhya/2d-convolution-using-python-numpy-43442ff5f381
    
Attention!
-----------
    I began with the intention of using convolution from out of box library
    But, I had to branch out to Convolve.py
    Most of the work in this file are irrelevant
    

'''


from skimage.transform import rescale, resize, downscale_local_mean
from skimage import io
import os
from os import listdir
from os.path import join
import datetime
import glob
import numpy as np
from matplotlib import pyplot as plt 
import cv2


def save_file(filename:str,image:np.ndarray):
    folder_script=os.path.dirname(__file__)
    now=datetime.datetime.now()    
    filename_result=("Reduced-%s.png") % (os.path.basename(filename))
    file_result=os.path.join(folder_script,"./out/",filename_result)
    io.imsave(file_result,image)


def generate_histogram(filename:str):
    print("-----------------------------------")
    print("Generating Histogram for file %s" % (filename))
    np_image=io.imread(filename,as_gray=True)
    scale_down=2
    image_resized = resize(np_image, (np_image.shape[0] // scale_down, np_image.shape[1] // scale_down),anti_aliasing=False)
    save_file(filename,image=image_resized)
    flattened_pixels=image_resized.flatten()
    #bins=list(range(-10,265,10))
    bins=list(np.arange(-0.1,1.1,0.1))
    hist,bins = np.histogram(flattened_pixels ,bins = bins) 
    plt.hist(flattened_pixels, bins = bins) 
    plt.title(filename) 
    plt.show()

    #you were here - not conclusive - what is the color of the black point, why is not on the histogram
    pass

def generate_histogram_for_all_files_in_folder(folder:str,pattern:str):
    matching_files=glob.glob(folder+pattern)    
    count=0
    for file in matching_files:
        extension=os.path.splitext(matching_files[0])[1]
        if (extension.lower() != '.png'):
            continue
        absolutepath=join(folder,file)
        generate_histogram(absolutepath)
        count+=1
    print("Resized %d files" % (count))
    pass



#
#Some problems when kernel=10X10 and image=200X200
#
def stride_conv(input_array,kernel,stride,padding):
    beg = 0
    end = kernel.shape[0]
    final = []
    for i in range(0,input_array.shape[0]-1,stride):
        k = []
        for j in range(0,input_array.shape[0]-1,stride):
            k.append(np.sum(input_array[beg+i : end+i, beg+j:end+j] * kernel))
        final.append(k)
    return np.array(final)
    
def convolve_image(filename:str):
    print("-----------------------------------")
    print("Convolving file %s" % (filename))
    np_image = cv2.imread(filename,cv2.IMREAD_GRAYSCALE )
    kernel_size=10
    kernel_value=1/(kernel_size*kernel_size)
    kernel=np.full((kernel_size,kernel_size),kernel_value)
    stride=int(kernel_size/2)
    #result=stride_conv(np_image, kernel=kernel, stride=stride, padding=0)
    result = cv2.filter2D(np_image, -1, kernel)
    save_file(image=result,filename=filename)
    pass

def convolve_all_files(folder:str,pattern:str):
    matching_files=glob.glob(folder+pattern)   
    count=0
    for file in matching_files:
        extension=os.path.splitext(matching_files[0])[1]
        if (extension.lower() != '.png'):
            continue
        absolutepath=join(folder,file)
        convolve_image(absolutepath)
        count+=1
    print("Resized %d files" % (count))
    pass

current_folder_with_samples=os.path.join(os.path.dirname(__file__),"./In/")
#generate_histogram_for_all_files_in_folder(folder=current_folder_with_samples, pattern="*para*200*.png")
convolve_all_files(folder=current_folder_with_samples, pattern="*para*200*.png")
