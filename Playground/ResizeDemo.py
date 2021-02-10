from skimage.transform import rescale, resize, downscale_local_mean
from skimage import io
import os
from os import listdir
from os.path import join
import datetime





def resize_demo(filename:str):
    #filename=get_input_file()
    print("Resizing file  %s" % (filename))
    image=io.imread(filename,as_gray=True)
    image_resized = resize(image, (image.shape[0] // 2, image.shape[1] // 2),anti_aliasing=False)
    #,anti_aliasing=True)    

    folder_script=os.path.dirname(__file__)
    now=datetime.datetime.now()    
    filename_result=("%s-%s.png") % (os.path.basename(filename),now.strftime("%Y-%m-%d-%H-%M-%S"))
    file_result=os.path.join(folder_script,"./out/",filename_result)
    io.imsave(file_result,image_resized)

def get_input_file():
    return ""

def resize_all_files_in_folder(folder:str):
    files=listdir(folder)
    count=0
    for file in files:
        extension=os.path.splitext(files[0])[1]
        if (extension.lower() != '.png'):
            continue
        absolutepath=join(folder,file)
        resize_demo(absolutepath)
        count+=1
    print("Resized %d files" % (count))
    pass

#resize_demo("C:/Users/saurabhd/MyTrials/MachineLearnings-2/CurveReconstruction/Main/in/Sine-W=500.H=200.MAXD=20.SP=0.95.2.png.2.png")
resize_all_files_in_folder("C:/Users/saurabhd/MyTrials/MachineLearnings-2/CurveReconstruction/Main/in")
