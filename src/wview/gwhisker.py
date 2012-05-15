from wmedia.wanimation import wanimation
from wmedia.wlayer import wlayer
from wview import ParticleAnimator
import math
from wmath import render_points

class GWhiskerLayer(wlayer):
    def __init__(self, particle, dl=5, length=150, width=15, alpha=1,rotation=0.,translate=(0,0)):
        wlayer.__init__(self, alpha)
        self.particle = particle
        self.renderer = GWhiskerRenderer(dl,length,width,rotation,translate)
    
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
    
    def render(self, context, particle, color=(255,255,255), stroke_width=1, alpha=1.0, filled=True):
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
            lambda t: particle[0]*t**3+particle[1]*t**2+particle[2]*t,
            lambda t: 1,
            lambda t: 3*particle[0]*t**2+2*particle[1]*t+particle[2],
            self.dl,
            self.length)
        
        map(fragment_renderer,points)

        context.arc(0,0,3,-math.pi,math.pi)
        if filled:
            context.fill()
        else:
            context.stroke()

class GWhiskerDatabaseRenderer:
    def __init__(self, dl, length,width, rotation=0,translate=(0,0),particle_alpha=0.1):
        self.dl = float(dl)
        self.length=float(length) 
        self.width=float(width)
        self.rotation=rotation
        self.translate=translate
        self.particle_alpha = particle_alpha
    
    def render(self, context, particle, color=(255,255,255), stroke_width=1, alpha=1.0, filled=True):
        context.identity_matrix()
        context.translate(*(self.translate))
        context.rotate(self.rotation)
        context.set_source_rgba(*(color + (alpha,)))

        context.set_line_width(self.width)
        def fragment_renderer(data):
            context.line_to(data[0],data[1])
            context.stroke()
            w=self.width*(1-data[2]/self.length)
#            context.arc(data[0],data[1],w/2,-math.pi,math.pi) #to remove the space between segments
#            context.fill()
            context.move_to(data[0],data[1])
            context.set_line_width(w)

        points=render_points(
            lambda t: t,
            lambda t: particle[0]*t**3+particle[1]*t**2+particle[2]*t,
            lambda t: 1,
            lambda t: 3*particle[0]*t**2+2*particle[1]*t+particle[2],
            self.dl,
            self.length)
        
        map(fragment_renderer,points)

        context.arc(0,0,3,-math.pi,math.pi)
        if filled:
            context.fill()
        else:
            context.stroke()

class GWhiskerAnimator(ParticleAnimator):
    rotation = 0
    translate = (0,0)
    dl = 5
    length = 150
    width = 5

    def __init__(self, *args, **kwargs):
        ParticleAnimator.__init__(self, *args, **kwargs)
        
        if 'rotation' in kwargs.keys():
            self.rotation = kwargs['rotation']
        if 'translate' in kwargs.keys():
            self.translate = kwargs['translate']
        if 'dl' in kwargs.keys():
            self.dl = kwargs['dl']
        if 'length' in kwargs.keys():
            self.length = kwargs['length']
        if 'width' in kwargs.keys():
            self.width = kwargs['width']
        
        self.renderer = GWhiskerRenderer(self.dl, self.length, self.width, rotation=self.rotation, translate=self.translate)
