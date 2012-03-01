from frame import frame
from video import video

def left_align_videoformat(i):
    """
    To get the format for the frame-number

    @Param i The number to get right format for
    @Note Could use String.format instead but some functionality is missing in python 2.*
    """
    assert(len(str(i))<=5)
    return ('0'*(5-len(str(i))))+str(i)
