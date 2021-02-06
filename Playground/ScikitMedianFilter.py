import os
from skimage import io
from skimage.filters.rank import median
from skimage.morphology import disk


def median_filter(inputfilename):
    """
    Produces a blank image
    """
    folder_script=os.path.dirname(__file__)
    absolute_filename=os.path.join(folder_script,"./in/",inputfilename)

    original = io.imread(absolute_filename, as_gray=True)
    print(original.dtype)
    print(original.shape)
    print(original.max())
    print(original.min())
    
    median_filtered=median(original, disk(2))  #`, 5, 10, 20,100

    filename_result="median-filter-output.png"
    file_result=os.path.join(folder_script,"./out/",filename_result)
    io.imsave(file_result,median_filtered)

#median_filter(inputfilename="Sine-50-percent.png")
median_filter(inputfilename="Sine-50-percent - MoreBlack.png")

#