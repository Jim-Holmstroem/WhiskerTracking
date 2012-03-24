from PIL import Image
import numpy

class frame:
    """
    Dual for image as numpy.array and (PIL.Image, Cairo.ImageSurface)

    @Example
        f=frame(Image.load('test.png'))
        frame.get_copy_of_image().show()
        read_array(frame.get_array()) 
        frame.get_image().show()
        write_array(frame.get_array()) 
        frame.get_copy_of_image().show() 

    @Note the dual could be generalized and perhaps used elsewhere
    """

    array=None

    def __init__(self,image):
        self.array=numpy.asarray(image,dtype=float).copy()

    def get_copy_of_current_image(self):
        """
        Generates an new image from the array each time its called

        @Return An PIL.Image from the current array
        """
        return Image.frombuffer('RGBA',tuple([self.array.shape[i] for i in (0,1)]),numpy.uint8(self.array),'raw','RGBA',0,1)



    def get_array(self):
        """
        Gets the array representing the image.

        @Return numpy.array representing the image
        """
        return self.array


if(__name__=='__main__'):
    img=frame(Image.open("../../data/square_simple.pngvin/frame-00012.png"))
    print img.get_array().dtype
    img.get_copy_of_current_image().show()
    img.get_array()[128:200,128:200,:]=128     
    img.get_copy_of_current_image().show()

