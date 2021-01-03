#
#Using Pillow library to read images
#
from PIL import Image
from numpy import asarray
import os


def pillow_demo(inputfilename:str):
    folder_script=os.path.dirname(__file__)
    absolute_filename=os.path.join(folder_script,"./in/",inputfilename)

    pil_image=Image.open(absolute_filename)
    arr = asarray(pil_image)
    print("Shape of the image:")
    print(arr.shape)
    print(arr.flatten())
    pass

pillow_demo("LineSample1.png")