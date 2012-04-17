
__all__ = ['wanimation']

import collections

from wmedia.wlayer import wlayer

from wmedia.wimage import wimage
from wmedia.wvideo import wvideo

import cairo

class wanimation(wlayer):
    """
    Acts as a base for moving layers, has some helping hands; one can either inherit from it and override the __init__ or just send in data and data_renderer
    """
    def __init__(self,data,data_renderer,alpha=1.0):
        """
        Argument data needs to have __getitem__ defined OR being callable (function)
        Argument data_renderer(context,data_point) and renderers it
        """
        wlayer.__init__(self,alpha)
        self.data=data
        self.data_renderer=data_renderer

    def render(self,context,i):
        if isinstance(self.data,collections.Sequence):
            self.data_renderer(context,self.data[i])
        elif callable(self.data):
            self.data_renderer(context,self.data(i))
        else:
            raise Exception("Data is not sequence nor callable")

    def export_frame(self,i):
        img = cairo.ImageSurface(cairo.ARGB32,512,512)
        context = cairo.Context(img)
        self.render(context,i)
        context.paint()
        return img

    def export(self,range=None):
        if range:
            raise NotImplemented("export range not implemented yet")
        return wvideo(map(self.export_frame,range(len(self))))

    def __len__(self):
        raise Exception("must define __len__ in child to wanimation")

