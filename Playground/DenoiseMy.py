#
#https://www.youtube.com/watch?v=StX_1iEO3ck
#

from skimage import data, img_as_float
from skimage.util import random_noise
import os
from skimage import io
from skimage.filters.rank import median
from skimage.filters import rank

from skimage.morphology import disk
from skimage import img_as_float
import datetime
from skimage import data


def mean_filter(inputfilename):
    """
    This works
    With disk(3) the pixels got enlarged. Not good.
    With disk(10) we got very large circular blobs. Not good
    With disk(5) the results are similar to disk(3)
    """
    folder_script=os.path.dirname(__file__)
    absolute_filename=os.path.join(folder_script,"./in/",inputfilename)

    #original = img_as_float(data.chelsea()[100:250, 50:300])
    original0 = io.imread(absolute_filename, as_gray=True)
    # #original=img_as_float(original0)
    original=original0
    
    #median_filtered=median(original, disk(2),mode='constant', cval=0.0)
    mean_filtered = rank.mean(original, selem=disk(5))

    now=datetime.datetime.now()    
    filename_result=("mean-%s-%s.png") % (os.path.basename(inputfilename)[0:5],now.strftime("%Y-%m-%d-%H-%M-%S"))
    file_result=os.path.join(folder_script,"./out/",filename_result)
    io.imsave(file_result,mean_filtered)

def median_filter(inputfilename):
    """
    Produces a blank image
    """
    folder_script=os.path.dirname(__file__)
    absolute_filename=os.path.join(folder_script,"./in/",inputfilename)

    #original = img_as_float(data.chelsea()[100:250, 50:300])
    original0 = io.imread(absolute_filename, as_gray=True)
    # #original=img_as_float(original0)
    original=original0
    
    #median_filtered=median(original, disk(2),mode='constant', cval=0.0)  #this is with new median filter, as per youtube video
    median_filtered=median(original, disk(3))

    now=datetime.datetime.now()    
    filename_result=("median-%s-%s.png") % (os.path.basename(inputfilename)[0:5],now.strftime("%Y-%m-%d-%H-%M-%S"))
    file_result=os.path.join(folder_script,"./out/",filename_result)
    io.imsave(file_result,median_filtered)

median_filter(inputfilename="Sine-50-percent.png")
#mean_filter(inputfilename="Sine-50-percent.png")
