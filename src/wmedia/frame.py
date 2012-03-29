from PIL import Image
import numpy

class frame:
    """
    Dual for image as numpy.array and PIL.Image with lazy loading/constructing

    @Example
        f=frame(Image.load('test.png'))
        frame.get_image().show() #no converting
        read_array(frame.get_array()) #convert img->arr internally since img updated (from None)
        frame.get_image().show() #no converting since arr hash haven't changed
        write_array(frame.get_array()) #no conversion
        frame.get_image().show() #convert arr->img since arr has updated

    @NOTE AVOID (Example)
        arr=f.get_arr()
        img=f.get_image()
        write2(arr)
        img.show() #will show the old image

    @Note the dual could be generalized and perhaps used elsewhere
    """

    array=None

    def __init__(self,image):
        self.array=numpy.asarray(image).copy()

    def get_copy_of_current_image(self):
        """
        Generates an new image from the array each time its called

        @Return An PIL.Image from the current array
        """
        return Image.frombuffer('RGBA',self.array.shape[0:2], self.array, 'raw', 'RGBA', 0, 1)

    def get_array(self):
        """
        Gets the array representing the image.

        @Return numpy.array representing the image
        """
        return self.array


if(__name__=='__main__'):
    img=frame(Image.open("../../data/square_simple.pngvin/frame-00000.png"))
    img.get_copy_of_current_image().show()
   # Image.frombuffer('RGBA',(16,16),numpy.zeros((16,16,4)),'raw','RGBA',0,1).show()
