from wmedia.wlayer import wlayer
from wmedia.wanimation import wanimation

class SquareLayer(wlayer):
    def __init__(self, particle, alpha=1):
        wlayer.__init__(self, alpha)
        self.particle = particle
        self.renderer = SquareRenderer(50)
    
    def render(self, context):
        self.renderer.render(context, (self.particle[0], self.particle[2]))

class SquareRenderer:
    def __init__(self, square_side):
        self.square_side = square_side
        self.rect_tuple = (-self.square_side/2, -self.square_side/2, self.square_side, self.square_side)
    
    def render(self, context, pos, angle=0, color=(255,255,255), filled=True, stroke_width=2, alpha=1.0):
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
    
    def __init__(self, main_particles, particles, intermediate_particles=None, main_particle_color=(0,0,255), particle_color=(255, 0, 0), intermediate_particle_color=(0,255,0), alpha=0.1):
        self.particles = particles
        self.main_particles = main_particles
        self.intermediate_particles = intermediate_particles
        self.alpha = alpha
        
        self.particle_color = particle_color
        self.main_particle_color = main_particle_color
        self.intermediate_particle_color = intermediate_particle_color
        
        self.data_renderer = self.render
    
    def __len__(self):
        if self.particles != None:
            return len(self.particles)
        elif self.main_particles != None:
            return len(self.main_particles)
        return 0
    
    def render(self, context, i):
        if self.intermediate_particles != None:
            for row in self.intermediate_particles[i]:
                angle = 0
                if len(row) >= 5:
                    angle = row[4]
                self.renderer.render(context, (row[0], row[2]), angle=angle, color=self.intermediate_particle_color, filled=False, alpha=0.1)
        
        if self.particles != None:
            for row in self.particles[i]:
                angle = 0
                if len(row) >= 5:
                    angle = row[4]
                self.renderer.render(context, (row[0], row[2]), angle=angle, color=self.particle_color, filled=False, alpha=0.1)
        
        main_particle = None
        if self.main_particles != None:
            main_particle = self.main_particles[i]
        else:
            main_particle = self.particles[i].mean(axis=0)

        angle = 0
        if len(row) >= 5:
            angle = row[4]
        self.renderer.render(context, (main_particle[0], main_particle[2]), angle=angle, color=self.main_particle_color, filled=False, alpha=1)
