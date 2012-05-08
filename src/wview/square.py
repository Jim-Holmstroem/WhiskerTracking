from wmedia.wlayer import wlayer
from wmedia.wanimation import wanimation

class SquareLayer(wlayer):
    def __init__(self, particle, alpha=1):
        wlayer.__init__(self, alpha)
        self.particle = particle
        self.renderer = SquareRenderer(50)
    
    def render(self, context):
        self.renderer.render(context, self.particle)

class SquareRenderer:
    def __init__(self, square_side):
        self.square_side = square_side
        self.rect_tuple = (-self.square_side/2, -self.square_side/2, self.square_side, self.square_side)
    
    def render(self, context, pos, angle=0, color=(255,255,255), filled=True, stroke_width=2, alpha=1.0):
        context.identity_matrix()
        context.translate(*pos)
        context.rotate(angle)
        context.rectangle(*self.rect_tuple)
        context.set_source_rgba(*(color+(alpha,)))
        if filled:
            context.fill()
        else:
            context.set_line_width(stroke_width)
            context.stroke()

class SquareAnimator(wanimation):
    
    renderer = SquareRenderer(50)
    
    def __init__(self, main_square_poses, square_poses, intermediate_square_poses=None, main_square_color=(0,0,255), square_color=(255, 0, 0), intermediate_square_color=(0,255,0), alpha=0.1):
        self.square_poses = square_poses
        self.main_square_poses = main_square_poses
        self.intermediate_square_poses = intermediate_square_poses
        self.alpha = alpha
        
        self.square_color = square_color
        self.main_square_color = main_square_color
        self.intermediate_square_color = intermediate_square_color
        
        self.data_renderer = self.render
    
    def __len__(self):
        if self.square_poses != None:
            return len(self.square_poses)
        elif self.main_square_poses != None:
            return len(self.main_square_poses)
        return 0
    
    def render(self, context, i):
        if self.intermediate_square_poses != None:
            for row in self.intermediate_square_poses[i]:
                angle = 0
                if len(row) >= 5:
                    angle = row[4]
                self.renderer.render(context, row, angle=angle, color=self.intermediate_square_color, filled=False, alpha=0.1)
        
        if self.square_poses != None:
            for row in self.square_poses[i]:
                angle = 0
                if len(row) >= 5:
                    angle = row[4]
                self.renderer.render(context, row, angle=angle, color=self.square_color, filled=False, alpha=0.1)
        
        main_pos = None
        if self.main_square_poses != None:
            main_pos = self.main_square_poses[i]
        else:
            main_pos = self.square_poses[i].mean(axis=0)

        angle = 0
        if len(row) >= 5:
            angle = row[4]
        self.renderer.render(context, main_pos, angle=angle, color=self.main_square_color, filled=False, alpha=1)
