import cairo
from wlayer import *

class wimagelayer:
    def __init__(self,alpha=1.0):
        self.alpha = alpha
    def draw(self,context):
        context.set_source_surface(cairo.ImageSurface.create_from_png("../../data/square_simple.pngvin/frame-00000.png"),0,0)
        context.paint_with_alpha(self.alpha) #normally fills entire area with foreground color if you haven't recently drawn an image that is
