import os
from skimage import io
from skimage.filters.rank import median
from skimage.morphology import disk
import glob


def median_filter(inputfilename,disk_size:int):
    """
    Produces a blank image
    """
    print("Processing input file %s " % (inputfilename))
    folder_script=os.path.dirname(__file__)
    absolute_filename=os.path.join(folder_script,"./in/",inputfilename)

    original = io.imread(absolute_filename, as_gray=True)
    print(original.dtype)
    print(original.shape)
    print(original.max())
    print(original.min())
    
    median_filtered=median(original, disk(disk_size))  #`, 2,5, 10, 20,100

    # filename_result="median-filter-output.png"
    # file_result=os.path.join(folder_script,"./out/",filename_result)

    filename_noextension=os.path.splitext(inputfilename)[0]
    filename_result=("median-%s-disk-%d.png") % (filename_noextension,disk_size)
    file_result=os.path.join(folder_script,"./out/",filename_result)
    print("Output written to file %s" % (file_result))
    io.imsave(file_result,median_filtered)

def run_selected_filepattern(pattern:str):
    folder_script=os.path.dirname(__file__)
    folder_with_files=os.path.join(folder_script,"./in/")
    matching_files=glob.glob(folder_with_files+pattern)
    for file in matching_files:
        filename=os.path.basename(file)
        median_filter(inputfilename=filename,disk_size=2)
        median_filter(inputfilename=filename,disk_size=4)
        median_filter(inputfilename=filename,disk_size=8)
        median_filter(inputfilename=filename,disk_size=16)

#run_selected_filepattern("*para*.png")
#median_filter(inputfilename="Sine-50-percent.png")
#median_filter(inputfilename="Sine-50-percent - MoreBlack.png")
#run_selected_filepattern("*SampleFor*.png")
run_selected_filepattern("*Lena.noise.png")
# median_filter(inputfilename="SampleForMedianFilter.png",disk_size=2 )
# median_filter(inputfilename="SampleForMedianFilter.png",disk_size=3 )
# median_filter(inputfilename="SampleForMedianFilter.png",disk_size=4 )
# median_filter(inputfilename="SampleForMedianFilter.png",disk_size=8 )
# median_filter(inputfilename="SampleForMedianFilter.png",disk_size=16 )
# median_filter(inputfilename="SampleForMedianFilter.png",disk_size=20 )




#