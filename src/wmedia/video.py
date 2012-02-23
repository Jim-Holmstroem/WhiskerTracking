import os
import re
from PIL import Image
from numpy import array
from wmedia import frame

class video:
    """
    Wrapper to use our video-format .pngvin
    """
    vid=[]
    num_digits=5
    is_frame=re.compile(r'^frame-[0-9]{' + str(num_digits) + r'}\.png$')
    is_valid_pngvin=re.compile(r'\.pngvin$')

    def __init__(self,url_to_folder):
        """
        Constructor for video

        @Param url_to_folder The url to the .pngvin file to load video from.
        """
        if self.is_valid_pngvin.search(url_to_folder) is not None:
            for img_path in os.listdir(url_to_folder): #NOTE possible bug the order of listing the frames might change.
                if self.is_frame.search(img_path) is not None:
                    self.vid.append(frame(Image.open(url_to_folder+'/'+img_path))) #NOTE not cross-platform since we use '/    '
        else:
            raise Exception('Not a .pngvin file')

    def __getitem__(self,i):
        """
        Get video-frame

        @Param i The index of the image you want.
        """
        return self.vid[i]
