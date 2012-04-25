
__all__=['response_test']

import cairo
import math
from wmedia.wlayer import wlayer
from wmedia.wimage import wimage
from wmedia.wvideo import wvideo
from wgui.wlayermanager import wlayermanager
from wimageprocessing.imageprocessing import normalize,abs_edge

import pylab

w,h=[512,512]

class response_object(wlayer):
    def __init__(self):
        wlayer.__init__(self,1.0)
    def render(self,context):
        raise Exception("not implemented, abstract class")

    def get_wimage(self):
        img = cairo.ImageSurface(cairo.FORMAT_ARGB32,w,h)
        context = cairo.Context(img)
        self.render(context)
        return wimage(img)

class response_circle(response_object):
    def __init__(self,pos):
        response_object.__init__(self)
        self.pos=pos

    def render(self,context,i=0):
        context.set_source_rgba(1.0,1.0,1.0,1.0)
        context.arc(self.pos[0],self.pos[1],64,0,2*math.pi)
        context.fill() 

middle_img=response_circle((w/2,h/2)).get_wimage().transform(abs_edge).blur(8)

x_range =range(-128,128+1,8)
print len(x_range)

x_mask = map(lambda posx:response_circle((w/2+posx,h/2)).get_wimage().transform(abs_edge), x_range)
x_correlation = map(lambda img:middle_img*img,x_mask)
x_response = map(lambda (mask,img): img.sum()/(255*mask.sum()),zip(x_mask,x_correlation))

pylab.plot(x_range,x_response)
pylab.show()

lm=wlayermanager()
lm.add_layer(wvideo(x_correlation).transform(normalize))
lm.exportPNGVIN("test.pngvin")

