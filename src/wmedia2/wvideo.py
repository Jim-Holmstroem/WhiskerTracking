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

    def __init__(self,filename):
        """
        Contrstructor for video

        @Param filename
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

