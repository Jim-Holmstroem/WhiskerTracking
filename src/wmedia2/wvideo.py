import os
import re

from wlayer import *
from wimage import *

class wvideo(wlayer):
    """
    Opens a PNGVIN-file
    """
    imgs=[] #list of type wimage
   
    num_digits=5
    is_frame=re.compile(r'^frame-[0-9]{'+str(num_digits)+r'}\.png$')
    is_valid_pingvin=re.compile(r'\.pngvin')

    def __init__(self,input_data):
        """
        Constructor for video

        @Param input_data, can be string or ordered vector with elements valid wimage.input_data
        """
        print "Loading video..."
        if isinstance(input_data,basestring):
            print "filename=",input_data
            self.init_with_filename(input_data)
        elif isinstance(input_data,(list)):
            print "input_data={data}"
            self.imgs=map(lambda data:wimage(data),input_data)
        else:
            raise Exception("input_data has incorrect type")

    def init_with_filename(self,filename):
        """
        load PNGVIN file from filename
        """
        if not self.is_valid_pingvin.search(filename):
            raise Exception('\''+filename+'\' is not a .pngvin file')
        img_names=filter(lambda filename:self.is_frame.search(filename),os.listdir(filename))
        img_names.sort() #to make sure it's sorted
        self.imgs=map(lambda img_name:wimage(filename+'/'+img_name),img_names)

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self,i):
        return self.imgs[i]
    
    def render(self,context,i):
        self.imgs[i].render(context)

