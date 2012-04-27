__all__ = ["SquareAnimator"]

from wmedia.wanimation import wanimation

class SquareAnimator(wanimation):
    
    SQUARE_SIDE = 50
    
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
        context.save()
        
#        context.scale(512,512)

        if self.intermediate_particles != None:
            context.set_source_rgba(*(self.intermediate_particle_color + (self.alpha,)))
            for row in self.intermediate_particles[i]:
                context.rectangle(row[0], row[2], 1, 1)
                context.fill()
        
        if self.particles != None:
            context.set_source_rgba(*(self.particle_color + (self.alpha,)))
            for row in self.particles[i]:
                context.rectangle(row[0], row[2], 1, 1)
                context.fill()
        
        main_particle = None
        if self.main_particles != None:
            main_particle = self.main_particles[i] - self.SQUARE_SIDE/2.0
        else:
            main_particle = self.particles[i].mean(axis=0) - self.SQUARE_SIDE/2.0
        
        context.rectangle(main_particle[0], main_particle[2], self.SQUARE_SIDE, self.SQUARE_SIDE)
        context.set_source_rgb(*self.main_particle_color)
        context.set_line_width(1)
        context.stroke()
        
        context.restore()
