import cairo
from wlayer import *

class wimagelayer:
    def __init__(self):
        pass

    def draw(self,context):
        context.set_source_surface(cairo.ImageSurface.create_from_png("../../data/square_simple.pngvin/frame-00000.png"),20,20)


