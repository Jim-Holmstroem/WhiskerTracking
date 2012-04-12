__all__ = ['pad_left', 'left_align_videoformat']

def pad_left(i, num_digits=5, pad_char="0"):
    """
    Left-pads the given number with zeros

    @param i: The number to get right format for
    @param num_digits: The number of digits wanted in the result
    @param pad_char: The character to pad with
    @return: a string representing i, padded with pad_char to the length num_digits.
                Example: If i=42, num_digits=5 and pad_char="0", the result is "00042".
    @note: Could use String.format instead but some functionality is missing in python 2.*
    """
    assert(len(str(i))<=num_digits)
    assert(len(pad_char) == 1)
    return (pad_char*(num_digits-len(str(i))))+str(i)

def left_align_videoformat(i):
    """
    Left-pads the given number with zeros to 5-digit length.
    @see: pad_left
    """
    return pad_left(i, 5, "0")
