__all__ = ["square_particles_animator"]

from wmedia.wanimation import wanimation

class square_particles_animator(wanimation):
    def __init__(self, particles, square_side, main_particles=None, intermediate_particles=None, particle_color=(255, 0, 0), main_particle_color=(0,0,255), intermediate_particle_color=(0,255,0), alpha=1.0):
        self.particles = particles
        self.main_particles = main_particles
        self.intermediate_particles = intermediate_particles
        
        self.particle_color = particle_color
        self.main_particle_color = main_particle_color
        self.intermediate_particle_color = intermediate_particle_color
        
        self.square_side = square_side
        self.data_renderer = self.render
    
    def __len__(self):
        return len(self.data)
    
    def render(self, context, i):
        context.save()
        
#        context.scale(512,512)

        if self.intermediate_particles != None:
            context.set_source_rgb(*self.intermediate_particle_color)
            for row in self.intermediate_particles[i]:
                context.rectangle(row[0], row[2], 1, 1)
                context.fill()
        
        context.set_source_rgb(*self.particle_color)
        for row in self.particles[i]:
            context.rectangle(row[0], row[2], 1, 1)
            context.fill()
        
        main_particle = None
        if self.main_particles != None:
            main_particle = self.main_particles[i]
        else:
            main_particle = self.particles[i][:,0:3:2].mean(axis=0) - self.square_side/2.0
        
        context.rectangle(main_particle[0], main_particle[1], self.square_side, self.square_side)
        context.set_source_rgb(*self.main_particle_color)
        context.set_line_width(1)
        context.stroke()
        
        context.restore()
