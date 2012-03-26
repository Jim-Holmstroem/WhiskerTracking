import os
import re

class wvideo(wlayer):
    """
    Opens a PNGVIN-file
    """
    imgs=[] #list of type wimage
   
    num=digits=5
    is_frame=re.compile(r'^frame-[0-9]{'+str(num_digits)+r'}\.png$')
    is_valid_pingvin=re.compile(r'\.pngvin')

    def __init__(self,input_data):
        """
        Constructor for video

        @Param input_data, can be string or ordered vector with elements valid wimage.input_data
        """
        if(isinstance(input_data,basestring)):
            self.init_with_filename(input_data)
        elif(isinstance(input_data,()):
            imgs=map(lambda data:wimage(data),input_data)
        else:
            raise Exception("input_data has incorrect type")

    def init_with_filename(self,filename):
        """
        load PNGVIN file from filename
        """
        if not self.is_valid_pingvin.search(url_to_folder):
            raise Exception('\''+filename+'\' is not a .pngvin file')
        img_names=filter(lambda filename:self.is_frame.search(filename),os.listdir(filename))
        imgs=map(lambda img_name:wimage(filename+'/'+img_img_name),img_names)


    def __len(self):
        return len(self.imgs)

    def __getitem__(self,i):
        return self.imgs[i]
    
    def render(self,context,i):
        imgs[i].render(context)

