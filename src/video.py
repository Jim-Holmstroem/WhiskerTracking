import os
import re
from PIL import Image


class video:
    vid=[]

    num_digits=5
    is_frame=re.compile('^frame-[0-9]{'+str(num_digits)+'}.png$')

    def __init__(self,url_to_folder):
        for img_path in os.listdir(url_to_folder): #NOTE possible bug the order of listing the frames might change.
            if self.is_frame.match(img_path):
                self.vid.append(Image.open(url_to_folder+'/'+img_path)) #NOTE not crossplatform

    def __getitem__(self,i):
        return self.vid[i]


