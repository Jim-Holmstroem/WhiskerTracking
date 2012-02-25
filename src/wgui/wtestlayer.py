from wlayer import *


class wtestlayer():
    def __init__(self):
        pass

    def draw(self,context):
        
        context.set_source_rgb(0,0.8,0.5)
        context.move_to(20,20)
        context.rel_line_to(40,40)
        context.stroke()


