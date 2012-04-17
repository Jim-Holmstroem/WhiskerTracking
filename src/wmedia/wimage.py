
__all__ = ['wimage']

from PIL import Image
import numpy
import cairo

from wmedia.wlayer import wlayer

class wimage(wlayer):
    """

    Could be used as a layer but mainly used in wvideo as a videframe.
    Has a numpy array as basis 
    """
    data=None
    def __init__(self,input_data,alpha=1.0):
        """
        The input data can be a filename,numpy array or cairo.ImageSurface
        If numpy.array it connects the data else is just copied at __init__
        """
        wlayer.__init__(self,alpha)
        #Handles different argument types
        if isinstance(input_data,numpy.ndarray):
            self.init_with_array(input_data)
        elif isinstance(input_data,tuple):
            self.init_with_size(input_data)
        elif isinstance(input_data,basestring):
            self.init_with_filename(input_data)
        elif isinstance(input_data,cairo.ImageSurface):
            self.init_with_imagesurface(input_data)
        else:
            raise Exception("Invalid input type; not (ndarray/basestring/imagesurface")
    
    def init_with_size(self,input_data):
        self.init_with_array(numpy.ndarray(input_data))

    def init_with_array(self,input_data):
#        print "wimage(numpy.ndarray[",id(input_data),"])"
        input_data=numpy.atleast_3d(input_data)
        assert(input_data.shape[2]==1) #must be grayscale image (MxNx1)
        self.data=input_data

    def init_with_filename(self,input_data):
#        print "wimage(",input_data,")"
        img=cairo.ImageSurface.create_from_png(input_data) #RGBA
        self.init_with_imagesurface(img)

    def init_with_imagesurface(self,input_data):
        self.data=numpy.frombuffer(input_data.get_data(),dtype=numpy.uint8) #RGBA
        self.data=numpy.cast['float64'](self.data) 
        self.data=self.data.reshape(input_data.get_width(),input_data.get_height(),len("RGBA")) 
        self.data=numpy.add.reduce(self.data[:,:,0:3],axis=2)/3 #RGBA->GRAY TODO one should instead use sqrt(sum(colorchannel^2)), but slower
        self.data=numpy.atleast_3d(self.data) #Make it (MxNx1) (in newer version of numpy on can do reduce(keepdims=True))
        #TODO set colors to GRAYlevel images (R,G,B)

    def transform(self,f):
        """
        transforms the image with the function f:img->img
        """
        return wimage(f(self.data),alpha=self.alpha) #creates a new image

    def debug_show(self):
        """
        DEBUGGING
        Show the image with default imageviewer, just for debugging
        """
        Image.frombuffer('RGBA',tuple([self.array.shape[i] for i in (0,1)]),numpy.uint8(self.array),'raw',0,1).show()


    def __add__(self,other):
        if(other=None):
            return wimage(self.data) #self.data+0
        return wimage(self.data+other.data)
    def __mul__(self,other):
        if(other=None):
            return wimage((512,512))
        return wimage(numpy.multiply(self.data,other.data))

    def shape(self):
        return self.data.shape
    
    def get_array(self):
        return self.data

    def render(self,context,i=None):
        """
        Argument i not used by wvideo but needed to be a wlayer
        """
        #http://stackoverflow.com/questions/7610159/convert-pil-image-to-cairo-imagesurface
        
        width,height=map(lambda i: self.data.shape[i],[0,1])
    
        alpha=255.0*numpy.ones_like(self.data)
       
        rgba_data=numpy.concatenate((self.data,)*3+(alpha,),2)
        img=cairo.ImageSurface.create_for_data(numpy.cast['uint8'](rgba_data.copy()), cairo.FORMAT_ARGB32,width,height) #NOTE .copy() because of bug in numpy
        context.set_source_surface(img)

