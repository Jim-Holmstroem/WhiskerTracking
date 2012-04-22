

import cairo
import math
from wmedia.wimage import wimage
from wgui.wlayermanager import wlayermanager


w,h=[512,512]

class response_object():
    def __init__(self):
        pass
    def render(self,context):
        raise Exception("not implemented, abstract class")

    def get_wimage(self):
        img = cairo.ImageSurface(cairo.FORMAT_ARGB32,w,h)
        context = cairo.Context(img)
        self.render(context)
        context.paint()
        return wimage(img)

class response_circle(response_object):
    def __init__(self,pos):
        self.pos=pos

    def render(self,context):
        context.arc(self.pos[0],self.pos[1],64,0,2*math.pi)
        context.set_source_rgba(1.0,1.0,1.0,1.0)
        context.fill()

class response_test:
    def __init__(self):
        self.middle_img=response_circle((w/2,h/2)).get_wimage()
        self.x_img = map(lambda posx:response_circle((w/2,h/2+posx)).get_wimage(), range(-128,128+1,32))
        self.response_x = map(lambda img:(self.middle_img*img).sum(),self.x_img)

        lm=wlayermanager()
        lm.add_layer(self.middle_img)
        lm.exportPNGVIN("test.pngvin")


        for response in self.response_x:
            print response

response_test()


