__all__ = ["square_animation"]

from wmedia.wanimation import wanimation

class square_animation(wanimation):
    def __init__(self, data, square_side, color=(255, 0, 0), alpha=1.0):
        self.color = color
        self.square_side = square_side
        wanimation.__init__(self, data, self.render_square, alpha)
    
    def __len__(self):
        return len(self.data)
    
    def render_square(self, context, data_point):
        context.save()
        
#        context.scale(512,512)
        
        context.rectangle(data_point[0]-self.square_side/2.0, data_point[1]-self.square_side/2.0, self.square_side, self.square_side)
        context.set_source_rgb(*self.color)
        context.set_line_width(1)
        context.stroke()
        
        context.restore()
