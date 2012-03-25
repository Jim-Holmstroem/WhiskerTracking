from PIL import Image
import numpy
import cairo

class wimage(wlayer):
    """

    Could be used as a layer but mainly used in wvideo as a videframe.
    Has a numpy array as basis 
    """
    data=None
    def __init__(self,input_data)
        """
        The input data can be a filename,numpy array or cairo.ImageSurface
        If numpy.array it connects the data else is just copied at __init__
        """
        
        #Handles different argument types
        if(isinstance(input_data,numpy.ndarray)):
            self.init_with_array(input_data)
        elif(isinstance(input_data,basestring):
            self.init_with_filename(input_data)
        elif(isinstance(input_data,cairo.ImageSurface):
            self.init_with_imagesurface(input_data)
        else:
            raise Exception("Invalid input type; not (ndarray/basestring/imagesurface")
    
    def init_with_array(self,input_data):
        self.data=input_data
    def init_with_filename(self,input_data):
        self.init_with_imagesurface(cairo.ImageSurface.create_from_png(input_data))
    def init_with_imagesurface(self,input_data):
        self.data=numpy.array(input_data.get_data().reshape(input_data.get_width(),input_data.get_height()))

    def debug_show(self):
        """
        DEBUGGING
        Show the image with default imageviewer, just for debugging
        """
        Image.frombuffer('RGBA',tuple([self.array.shape[i] for i in (0,1)]),numpy.uint8(self.array),'raw',0,1).show()

    def shape(self):
        return self.array.shape

    def render(self,context,i=None):
        """
        Argument i not used by wvideo but needed to be a wlayer

        """
        #http://stackoverflow.com/questions/7610159/convert-pil-image-to-cairo-imagesurface

        height,width,channels=self.shape()
        img=cairo.ImageSurface.create_for_data(self.data, cairo.FORMAT_ARGB32,width,height)
        context.set_source_surface(img)

