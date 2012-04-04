
__all__=['image_gradient']

import numpy

from filters import central_diff
from ipmath import point,norm,direction 

class image_gradient:
    """
    Lazy gradient class that takes a reference to an image and calculates necassary parameters as they are called.
    
    Updating the image will invalidate all data, you can call renew (you might as well make a new instance)

    """
    diffs_data=None
    mag_data=None
    dir_data=None
    
    def __init__(self,img,diff_method=central_diff):
        """

        Argument img the image to take the gradient of
        Argument diff_method takes image and returns [diff_x,diff_y]
        """
        self.img=img
        self.diff_method=diff_method
  
    def renew(self,img):
        self.img=img
        self.diffs_data=None
        self.mag_data=None
        self.dir_data=None

    def diffs(self):
        """
        Returns a point containing the diff in x and y 
        """
        if self.diffs_data is None:
            self.diffs_data = point(self.diff_method(self.img))
        return self.diffs_data

    def mag(self):
        if self.mag_data is None:
            self.mag_data = norm(self.diffs().x,self.diffs().y,2)
        return self.mag_data

    def dir(self):
        if self.dir_data is None:
            self.dir_data=direction(self.diffs().x,self.diffs().y)
        return self.dir_data

