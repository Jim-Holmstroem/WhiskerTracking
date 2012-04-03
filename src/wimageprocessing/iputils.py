
__all__=['filter_image','filter_video']

import numpy

from wmedia import wimage,wvideo

def filter_image(img,f=None):
    """
    @param img the image to filter
    @param f function f:img->img
    """
    return wimage(f(img))
def filter_video(video,f=None):
    """
    @param video the video in which to filter all the frames in 
    @param f function f:img->img
    """
    return wvideo(map(lambda img:f(img.data),video))

