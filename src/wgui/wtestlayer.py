from wlayer import *


class wtestlayer():
    def __init__(self):
        pass

    def draw(self,context):
        
        context.set_source_rgb(0,0.8,0.5)
        context.move_to(0,0)
        context.rel_line_to(512,512)
        context.stroke()

        context.set_source_rgb(1-0,1-0.8,1-0.5)
        context.move_to(0,512)
        context.rel_line_to(512,-512)
        context.stroke()
        context.move_to(512,0)
        context.rel_line_to(-512,512)
        context.stroke()
