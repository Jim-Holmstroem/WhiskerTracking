import os
import re
from PIL import Image
from numpy import array

class video:
    """
    Wrapper to use our video-format .pngvin
    """
    vid=[]
    num_digits=5
    is_frame=re.compile('^frame-[0-9]{'+str(num_digits)+'}.png$')
    is_valid_pngvin=re.compile('.pngvin$')

    def __init__(self,url_to_folder):
        """
        Constructor for video

        @Param url_to_folder The url to the .pngvin file to load video from.
        """
        if self.is_valid_pngvin.match(url_to_folder):
            for img_path in os.listdir(url_to_folder): #NOTE possible bug the order of listing the frames might change.
                if self.is_frame.match(img_path):
                    self.vid.append(Image.open(url_to_folder+'/'+img_path)) #NOTE not cross-platform since we use '/    '
        else:
            raise Exception('Not a .pngvin file')

    def __getitem__(self,i):
        """
        Get video-frame

        @Param i The index of the image you want.
        """
        return self.vid[i]


