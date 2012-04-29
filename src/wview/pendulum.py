from wmedia.wanimation import wanimation
from wmedia.wlayer import wlayer
import math

class PendulumLayer(wlayer):
    def __init__(self, particle, alpha=1):
        wlayer.__init__(self, alpha)
        self.particle = particle
        self.renderer = PendulumRenderer(400.0/512, 24.0/512)
    
    def render(self, context):
        self.renderer.render(context, self.particle)

class PendulumRenderer:
    
    def __init__(self, l, radius, particle_alpha=0.1):
        self.l = l
        self.radius = radius
        self.particle_alpha = particle_alpha
    
    def render(self, context, particle, color=(255,255,255), filled=True, stroke_width=1, alpha=1.0):
        context.identity_matrix()
        context.scale(512, 512)
        phi = particle[0]
        x = 0.5 + self.l*math.sin(phi)
        y = self.l*math.cos(phi)
        
        context.set_source_rgba(*(color + (alpha,)))
        context.arc(x, y, float(self.radius), 0., 2 * math.pi)
        if filled:
            context.fill()
        else:
            context.set_line_width(0.005)
            context.stroke()

class PendulumAnimator(wanimation):
    def __init__(self, main_particles, particles, intermediate_particles, l, radius, main_particle_color=(0,255,0), particle_color=(255,0,0), intermediate_particle_color=(0,0,255), alpha=0.1):
        self.particles = particles
        self.main_particles = main_particles
        self.intermediate_particles = intermediate_particles
        self.alpha = alpha
        
        self.particle_color = particle_color
        self.main_particle_color = main_particle_color
        self.intermediate_particle_color = intermediate_particle_color
        
        self.data_renderer = self.render
        self.renderer = PendulumRenderer(l, radius)
    
    def __len__(self):
        if self.particles != None:
            return len(self.particles)
        elif self.main_particles != None:
            return len(self.main_particles)
        return 0
    
    def render(self, context, i):
        if self.intermediate_particles != None:
            for row in self.intermediate_particles[i]:
                self.renderer.render_particle(context, row, self.intermediate_particle_color, filled=False, alpha=0.1)
        
        if self.particles != None:
            for row in self.particles[i]:
                self.renderer.render_particle(context, row, self.particle_color, filled=False, alpha=0.1)
        
        main_particle = None
        if self.main_particles != None:
            main_particle = self.main_particles[i]
        else:
            main_particle = self.particles[i].mean(axis=0)
        
        self.renderer.render_hypothesis(context, main_particle, self.main_particle_color, filled=False, alpha=0.5)
