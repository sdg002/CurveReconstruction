'''
Experimenting with Convolution

Wrote my own function
The function works except for padding at the boundaries
What have I tried so far?
    Used a simple linear kernel
    kernel size 
        20
        10
        5
What do I learn?
    Try histogram
    and then determine the threshold using histogram
        
What do I learn?
    I think we need to try with Gaussian filter

What did I learn?
    Nothing worked in de-noising the image. I have posted on Reddit

Image processing via GIMP
    Approach 1 - Take the input image. Gaussian filter, followed by threshold(234)
    Approach 2 - 
        kernel=5. Take the convolved image. Apply threshold 0f 245. (Left arm was good)
        kernel=25. Take the convolved image. Apply threshold 0f 253. (Very good. Got both arms)

        Convolved-parabola.W=500.H=200.MAXD=5.SP=0.90.19.png-kernel-10
        ----------------------------------------------------------------------
            Convolve and then GIMP 
                Treshold=247. All noise gone, part of the arms visible.
                Threshold=248. The arms are beautifully visible. Some noise

        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.90.20.png.20.png-kernel-20
        ----------------------------------------------------------------------
            Convolve and then GIMP Treshold=253, significant noise reduction. Some spots remain.

        Convolved-parabola.W=500.H=200.MAXD=5.SP=0.90.19.png-kernel-25
        --------------------------------------------------------------
            Convolve and then GIMP Treshold=253, massive noise reduction

        Convolved-parabola.W=500.H=200.MAXD=5.SP=1.00.18.png-kernel-25
        ---------------------------------------------------------------
            Convolve and then GIMP Treshold=255, very good noise reduction. But, the output was of good quality

        Convolved-parabola.W=200.H=200.MAXD=10.SP=0.80.png-kernel-5
        ------------------------------------------------------------
            Threshold=246.  The parabola is much more prominent but still noisy

        Convolved-parabola.W=200.H=200.MAXD=10.SP=0.80.png-kernel-20
        -------------------------------------------------------------
            Threshold=251. Lot of noise gone. The parabola emerges. But, still some noise


        Convolved-parabola.W=500.H=200.MAXD=5.SP=0.90.19.png-kernel-50
        -------------------------------------------------------------
            Threshold=254. Lot of noise gone. Very good

        Convolved-parabola.W=500.H=200.MAXD=5.SP=0.90.19.png-kernel-40
        -------------------------------------------------------------
            Threshold=253. Lot of noise gone. Little noisier than kernel=50. But, still very good

        Convolved-parabola.W=500.H=200.MAXD=5.SP=0.90.19.png-kernel-40
        -------------------------------------------------------------
            Threshold=253 Very good. 

        
        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.90.20.png.20.png-kernel-50
        -------------------------------------------------------------
            Threshold=254.  Only left arm of the parabola was visible

        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.90.20.png.20.png-kernel-40
        -------------------------------------------------------------
            Threshold=254. Parabola identified. But a few and large noisy spots left behind

        
        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.90.20.png.20.png-kernel-30
        -------------------------------------------------------------
            Threshold=253. Left arm was visible.

        Convolved-parabola.W=500.H=200.MAXD=5.SP=0.90.19.png-kernel-25
        -------------------------------------------------------------
            Threshold=253. Left arm was visible

        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.90.20.png.20.png-kernel-25
        -------------------------------------------------------------
            Threshold=253. Left arm was visible

        Convolved-parabola.W=500.H=200.MAXD=5.SP=0.90.19.png-kernel-20
        -------------------------------------------------------------
            Threshold=252. Very good. A few tiny spots remain

        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.90.20.png.20.png-kernel-10
        -------------------------------------------------------------
            Threshold=251. Lot of noise reduction. Arms are clearly visible. Some spots remain

        Convolved-parabola.W=200.H=200.MAXD=10.SP=0.80.png-kernel-10
        ------------------------------------------------------------
            Threshold=248. The parabola emerges. But, still some noise

        Convolved-parabola.W=200.H=200.MAXD=10.SP=0.80.png-kernel-25.png
        ------------------------------------------------------------
            Threshold=251. The parabola emerges. But, still some noise
        
        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.80.21.png-kernel-50
        ------------------------------------------------------------
            Threshold=25. A lof the parabola is visible. Some portion of the right arm is missing

        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.80.21.png-kernel-40
        ------------------------------------------------------------
            Threshold=253. Left arm is visible. Most of the right arm is missing.

        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.80.21.png-kernel-35
        ------------------------------------------------------------
            Threshold=253. Left arm and right arm is visible. Some additional chunks  (Little better than 30)

        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.80.21.png-kernel-30
        ------------------------------------------------------------
            Threshold=253. Left arm is visible. Right arm is visible. Some noisy additional chunks (Slightly poorer than 35)

        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.80.21.png-kernel-25
        ------------------------------------------------------------
            Threshold=252.  Left and right arms are identified. But several noisy chunks


        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.80.21.png-kernel-20
        ------------------------------------------------------------
            Threshold=251. Left arm is good. Half of right arm is missing. Few noisy chunks

        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.80.21.png-kernel-15
        ------------------------------------------------------------
            Threshold=251.  Very noisy with dots


        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.80.21.png-kernel-10
        ------------------------------------------------------------
            Threshold=251.  Very noisy with dots

        Convolved-parabola.W=500.H=200.MAXD=10.SP=0.80.21.png-kernel-5
        ------------------------------------------------------------
            Threshold=246.  Very noisy with dots

        

What next?
    Read about Nearest neighbour approach for de-noising
    Try Gaussian with radius=3 and 5

Go back to what you were doing before


'''


from skimage.transform import rescale, resize, downscale_local_mean
from skimage import io
import os
from os import listdir
from os.path import join
import datetime
import glob
import numpy as np
import cv2

def save_file(filename:str,image:np.ndarray):
    folder_script=os.path.dirname(__file__)
    now=datetime.datetime.now()    
    filename_result=("Convolved-%s.png") % (os.path.basename(filename))
    file_result=os.path.join(folder_script,"./out/",filename_result)
    io.imsave(file_result,image)


def convolve_image(filename:str,kernel_size:int):
    print("-----------------------------------")
    print("Convolving file %s" % (filename))
    np_image = cv2.imread(filename,cv2.IMREAD_GRAYSCALE )
    #kernel_size=  #25 # 5 #10,20
    kernel_value=1/(kernel_size*kernel_size)
    kernel=np.full((kernel_size,kernel_size),kernel_value)
    stride=int(kernel_size/2)
    #result = convolve2D_medium(image=np_image, kernel=kernel, strides=stride) #Produced a black image with white dots
    #result = convolve2D_image_sfo(input_array=np_image, kernel=kernel, stride=stride) #some problems
    result = convolve2D_my(image=np_image, kernel=kernel, strides=stride) 
    new_filename=("%s-kernel-%d") % (filename,kernel_size)
    save_file(image=result,filename=new_filename)
    pass

def simple_convolve(arr1:np.ndarray, arr2:np.ndarray):
    if (arr1.shape != arr2.shape):
        raise Exception("The shape of array1 %s should match array2 %s" % str(arr1.shape), str(arr2.shape))
    sum=0
    height=arr1.shape[0]
    width=arr1.shape[1]
    for y in range(0,height):
        for x in range(0,width):
            arr1_pixel=arr1[y][x]
            arr2_pixel=arr2[y][x]
            sum=sum+arr1_pixel*arr2_pixel
    return sum

'''
Performs a convolution operation on the given image, using the specified kernel and stride
Padding is not being used
How to improve?
    When the right boundary is reached, we are ignoring if left width is less than kernel dimension
    This is where we need to consider padding. See OPENCV and SCIPY. They specify some constants
Tip
    Pre-compute the extra padding required and add this addtional along the width and height 
    to the clone of the input image
'''
def convolve2D_my(image, kernel, padding=0, strides=1):
    kernel_height=kernel.shape[0]
    kernel_width=kernel.shape[1]
    if (kernel_height != kernel_width):
        raise Exception("The width of the height of the kernel array must be identical")
    image_height=image.shape[0]
    image_width=image.shape[1]
    kernel_size=kernel_width
    if (image_height < kernel_size):
        raise Exception("The height of the image must be greater than the kernel size")

    if (image_width < kernel_size):
        raise Exception("The width of the image must be greater than the kernel size")

    max_y=1
    for y in range(0,image_height,strides):
        y_start=y
        y_end=y_start+kernel_size-1
        if (y_end > image_height):
            break
        max_y=max_y+1

    max_x=1
    for x in range(0,image_width,strides):
        x_start=x
        x_end=x_start+kernel_size-1
        if (x_end > image_width):
            break
        max_x=max_x+1

    result_array=np.zeros([max_y,max_x])
    y_index=0
    for y in range(0,image_height,strides):
        x_index=0
        for x in range(0,image_width,strides):
            y_start=y
            y_end=y_start+kernel_size
            x_start=x
            x_end=x_start+kernel_size
            image_slice=image[y_start:y_end,x_start:x_end]
            print(image_slice.shape)
            if (image_slice.shape[0] < kernel_size):
                #Temporary - need to pad the image to avoid index out of range
                break
            if (image_slice.shape[1] < kernel_size):
                #Temporary - need to pad the image to avoid index out of range
                continue
            conv_result=simple_convolve(image_slice,kernel)
            result_array[y_index][x_index]=conv_result
            x_index=x_index+1
        y_index=y_index+1
    return result_array

def convolve2D_image_sfo(input_array,kernel,stride,padding=0):
    beg = 0
    end = kernel.shape[0]
    final = []
    for i in range(0,input_array.shape[0]-1,stride):
        k = []
        for j in range(0,input_array.shape[0]-1,stride):
            k.append(np.sum(input_array[beg+i : end+i, beg+j:end+j] * kernel))
        final.append(k)
    return np.array(final)

def convolve2D_medium(image, kernel, padding=0, strides=1):
    # Cross Correlation
    kernel = np.flipud(np.fliplr(kernel))

    # Gather Shapes of Kernel + Image + Padding
    xKernShape = kernel.shape[0]
    yKernShape = kernel.shape[1]
    xImgShape = image.shape[0]
    yImgShape = image.shape[1]

    # Shape of Output Convolution
    xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
    yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
    output = np.zeros((xOutput, yOutput))

    # Apply Equal Padding to All Sides
    if padding != 0:
        imagePadded = np.zeros((image.shape[0] + padding*2, image.shape[1] + padding*2))
        imagePadded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
        print(imagePadded)
    else:
        imagePadded = image

    # Iterate through image
    for y in range(image.shape[1]):
        # Exit Convolution
        if y > image.shape[1] - yKernShape:
            break
        # Only Convolve if y has gone down by the specified Strides
        if y % strides == 0:
            for x in range(image.shape[0]):
                # Go to next row once kernel is out of bounds
                if x > image.shape[0] - xKernShape:
                    break
                try:
                    # Only Convolve if x has moved by the specified Strides
                    if x % strides == 0:
                        output[x, y] = (kernel * imagePadded[x: x + xKernShape, y: y + yKernShape]).sum()
                except:
                    break

    return output

def convolve_all_files(folder:str,pattern:str):
    matching_files=glob.glob(folder+pattern)   
    count=0
    for file in matching_files:
        extension=os.path.splitext(matching_files[0])[1]
        if (extension.lower() != '.png'):
            continue
        absolutepath=join(folder,file)
        # convolve_image(absolutepath,kernel_size=15)
        # convolve_image(absolutepath,kernel_size=30)
        convolve_image(absolutepath,kernel_size=35)
        # convolve_image(absolutepath,kernel_size=40)
        # convolve_image(absolutepath,kernel_size=50)
        count+=1
    print("Resized %d files" % (count))
    pass

current_folder_with_samples=os.path.join(os.path.dirname(__file__),"./In/")
#generate_histogram_for_all_files_in_folder(folder=current_folder_with_samples, pattern="*para*200*.png")
convolve_all_files(folder=current_folder_with_samples, pattern="*para*200*.png")

