from itertools import izip
import cairo
import math
import numpy
from wgenerator.generator import Generator
from wgenerator.settings import IMAGE_WIDTH, IMAGE_HEIGHT
from wmedia import wvideo
from wview import GWhiskerRenderer

class GWhiskerGenerator(Generator):
    """Generates whisker-like lines that swoosh around."""
    PARAMETER_GROUPS = [3]

    A_LIMITS = (-0.00004, 0.00004)
    B_LIMITS = (-0.010, 0.010)
    C_LIMITS = (-1.0, 1.0)

    WHISKER_DL = 5
    WHISKER_LENGTH = 150
    WHISKER_WIDTH = 5

    DISTANCE_BETWEEN_WHISKERS = 25
    
    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)
        self.renderers = []

        mid = numpy.array((IMAGE_WIDTH/2, IMAGE_HEIGHT/2))
        translate_height = self.DISTANCE_BETWEEN_WHISKERS*float(self.number_of_objects-1)
        translate = mid + numpy.vstack((-self.WHISKER_LENGTH/2 * numpy.ones(self.number_of_objects), numpy.linspace(-translate_height/2, translate_height/2, self.number_of_objects))).T
        
        for i in xrange(self.number_of_objects):
            self.renderers.append(GWhiskerRenderer(self.WHISKER_DL, self.WHISKER_LENGTH, self.WHISKER_WIDTH, translate=translate[i]))

    def timestep(self, from_states, t):
        cp = from_states.copy()
        cp[:,1] *= math.sin(t)
        return cp

    def generate_training_transitions(self):
    
        # Limits were found by manual testing, one parameter at a time
        a = numpy.random.uniform(*self.A_LIMITS, size=(self.number_of_transitions, 1))
        b = numpy.random.uniform(*self.B_LIMITS, size=(self.number_of_transitions, 1))
        c = numpy.random.uniform(*self.C_LIMITS, size=(self.number_of_transitions, 1))

        from_states = numpy.hstack((a, b, c))
        to_states = self.timestep(from_states, numpy.random.uniform(0, math.pi*2))
        
        return from_states, to_states
    
    def generate_testing_sequence(self, num_frames):
        a = numpy.random.uniform(*self.A_LIMITS)
        b = numpy.random.uniform(*self.B_LIMITS)
        c = numpy.random.uniform(*self.C_LIMITS)
        
        state = numpy.hstack((a, b, c))
        state = numpy.reshape(state, (1,)+state.shape)
        states = numpy.zeros((num_frames, state.size))

        t = numpy.random.uniform(0, math.pi*2)
        dt = math.pi/32

        for i in xrange(num_frames):
            states[i,:] = self.timestep(state, t)
            t += self.dt*dt
        
        return numpy.array(states)
    
    def generate_testing_movie(self, all_states):
        surfaces = [cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT) for i in xrange(len(all_states[0]))]
        contexts = [cairo.Context(surface) for surface in surfaces]
        
        for context in contexts:
            #context.scale(IMAGE_WIDTH, IMAGE_HEIGHT) # Normalize the canvas

            context.rectangle(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT)
            context.set_source_rgb(0,0,0)
            context.fill()

        for i, states in enumerate(all_states):
            for particle, context in izip(states, contexts):
                self.renderers[i].render(context, particle)
        
        return wvideo(surfaces)

