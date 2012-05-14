from wmedia.wanimation import wanimation
from wmedia.wlayer import wlayer
import math
from wmath import render_points

class GWhiskerLayer(wlayer):
    def __init__(self, particle, alpha=1,rotation=0.,translate=(0,0)):
        wlayer.__init__(self, alpha)
        self.particle = particle
        self.renderer = GWhiskerRenderer(8,256,16,rotation,translate)
    
    def render(self, context):
        self.renderer.render(context, self.particle)

class GWhiskerRenderer:
    def __init__(self, dl, length,width, rotation=0,translate=(0,0),particle_alpha=0.1):
        self.dl = float(dl)
        self.length=float(length) 
        self.width=float(width)
        self.rotation=rotation
        self.translate=translate
        self.particle_alpha = particle_alpha
    
    def render(self, context, particle, color=(255,255,255), stroke_width=1, alpha=1.0):
        context.identity_matrix()
        context.translate(*(self.translate))
        context.rotate(self.rotation)
        context.set_source_rgba(*(color + (alpha,)))

        context.set_line_width(self.width)
        def fragment_renderer(data):
            context.line_to(data[0],data[1])
            context.stroke()
            w=self.width*(1-data[2]/self.length)
            context.arc(data[0],data[1],w/2,-math.pi,math.pi) #to remove the space between segments
            context.fill()
            context.move_to(data[0],data[1])
            context.set_line_width(w)

        points=render_points(
            lambda t: t,
            lambda t: particle[0]*t**3+particle[1]*t**2+particle[2]*t+particle[3],
            lambda t: 1,
            lambda t: 3*particle[0]*t**2+2*particle[1]*t+particle[2],
            self.dl,
            self.length)
        
        map(fragment_renderer,points)

        context.arc(0,particle[3],3,-math.pi,math.pi)
        context.fill()

"""
class GWhiskerAnimator(wanimation):
    def __init__(self, main_particles, particles, intermediate_particles, l, radius, main_particle_color=(0,255,0), particle_color=(255,0,0), intermediate_particle_color=(0,0,255), alpha=0.1):
        self.particles = particles
        self.main_particles = main_particles
        self.intermediate_particles = intermediate_particles
        self.alpha = alpha
        
        self.particle_color = particle_color
        self.main_particle_color = main_particle_color
        self.intermediate_particle_color = intermediate_particle_color
        
        self.data_renderer = self.render
        self.renderer = GWhiskerRenderer(l, radius)
    
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
"""

