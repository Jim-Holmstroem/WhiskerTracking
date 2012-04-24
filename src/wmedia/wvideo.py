
__all__ = ['wvideo']

import os
import re

from wmedia.wlayer import wlayer 
from wmedia.wimage import wimage
from wmedia.wanimation import wanimation

from wmath.wmath import argmax

from itertools import izip

class wvideo(wlayer):
    """
    Opens a PNGVIN-file
    """
    imgs=[] #list of type wimage
   
    num_digits=5
    is_frame=re.compile(r'^frame-[0-9]{'+str(num_digits)+r'}\.png$')
    is_valid_pingvin=re.compile(r'\.pngvin')

    def __init__(self,input_data,alpha=1.0):
        """
        Constructor for video

        @Param input_data, can be string or ordered vector with elements valid wimage.input_data
        """
        wlayer.__init__(self,alpha)

        if isinstance(input_data,basestring):
            self.init_with_filename(input_data)
        elif isinstance(input_data,wanimation):
            self.init_with_list(input_data.export()) 
        elif isinstance(input_data,(list)):
            self.init_with_list(input_data) 
        else:
            raise Exception("input_data has incorrect type:"+type(input_data))

    def init_with_list(self,dlist):
        """
        Init with a list of image-data (of somesort)
        """
        if len(dlist)!=0:
            if isinstance(dlist[0],wimage):
                self.imgs=dlist
            else:
                self.imgs=map(lambda data:wimage(data,self.alpha),dlist)
        else:
            raise Exception("input_data-list has len=0")


    def init_with_filename(self,filename):
        """
        load PNGVIN file from filename
        """
        if not self.is_valid_pingvin.search(filename):
            raise Exception('\''+filename+'\' is not a .pngvin file')
        img_names=filter(lambda filename:self.is_frame.search(filename),os.listdir(filename))
        img_names.sort() #to make sure it's sorted
        self.imgs=map(lambda img_name:wimage(filename+'/'+img_name),img_names)

    def transform(self,f):
        """
        transform the entire video with the function f:img->img
        """
        return wvideo(map(lambda img:img.transform(f),self.imgs),alpha=self.alpha)         

    def __add__(self,other):
        padding_size=abs(len(self)-len(other))
        [small_len,big_len]=sorted(map(len,[self,other]))
        biggest=argmax(len,(self,other))
        imgs=map(lambda (i,j):i+j,izip(self.imgs,other.imgs))
        imgs.extend(biggest[small_len:])
        return wvideo(imgs)

    def __mul__(self,other):
        padding_size=abs(len(self)-len(other))
        imgs=map(lambda (i,j):i*j,izip(self.imgs,other.imgs))
        imgs.extend(map(lambda dummy:wimage((512,512)),range(padding_size)))
        return wvideo(imgs)

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self,i):
        return self.imgs[i]
    
    def render(self,context,i):
        if len(self)>i:
            self.imgs[i].render(context)
    
    def image_shape(self):
        assert len(self.imgs) > 0, "Video is empty"
        return self.imgs[0].data.shape


