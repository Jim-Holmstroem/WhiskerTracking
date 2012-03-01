from frame import frame
from video import video

def left_align_videoformat(i, num_digits=5):
    """
    Left-pads the given number with zeros

    @param i: The number to get right format for
    @param num_digits: The number of digits wanted in the result
    @return: a string representing i, padded with zeros to the length num_digits. Example: If i=42 and num_digits=5, the result is "00042".
    @note: Could use String.format instead but some functionality is missing in python 2.*
    """
    assert(len(str(i))<=num_digits)
    return ('0'*(num_digits-len(str(i))))+str(i)
