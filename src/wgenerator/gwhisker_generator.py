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

    CUSTOM_CLI_DEFINITION = "[--dl DL] [--length WHISKER_LENGTH] [--width WHISKER_WIDTH]"

    PARAMETER_GROUPS = [3]

    A_LIMITS = 0.000016 * numpy.array((0, 1))
    B_LIMITS = 0.004 * numpy.array((0, 1))
    C_LIMITS = 1 * numpy.array((0, 1))

    DT = 2*math.pi/30

    """
    DT = math.pi/32

    A_LIMITS = (-0.00004, 0.00004)
    B_LIMITS = (-0.010, 0.010)
    C_LIMITS = (-0.5, 0.5)
    """

    dl = 5
    length = 150
    width = 5

    DISTANCE_BETWEEN_WHISKERS = 25
    
    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)
        self.renderers = []

        mid = numpy.array((IMAGE_WIDTH/2, IMAGE_HEIGHT/2))
        translate_height = self.DISTANCE_BETWEEN_WHISKERS*float(self.number_of_objects-1)
        self.translate = mid + numpy.vstack((-self.length/2 * numpy.ones(self.number_of_objects), numpy.linspace(-translate_height/2, translate_height/2, self.number_of_objects))).T

        if "DL" in kwargs.keys():
            self.dl = kwargs["DL"]
        if "WHISKER_LENGTH" in kwargs.keys():
            self.length = kwargs["WHISKER_LENGTH"]
        if "WHISKER_WIDTH" in kwargs.keys():
            self.width = kwargs["WHISKER_WIDTH"]
        
        for i in xrange(self.number_of_objects):
            self.renderers.append(GWhiskerRenderer(self.dl, self.length, self.width, translate=self.translate[i]))

    def goto_time(self, base_states, t):
        return base_states * numpy.vstack((numpy.sin(t), numpy.sin(t), numpy.sin(t))).T

    """
    def goto_time(self, base_states, t):
        cp = base_states.copy()
        cp[:,1] *= numpy.sin(t)
        return cp
    """

    def generate_training_transitions(self):
    
        # Limits were found by manual testing, one parameter at a time
        a = numpy.random.uniform(*self.A_LIMITS, size=(self.number_of_transitions, 1))
        b = numpy.random.uniform(*self.B_LIMITS, size=(self.number_of_transitions, 1))
        c = numpy.random.uniform(*self.C_LIMITS, size=(self.number_of_transitions, 1))

        base_states = numpy.hstack((a, b, c))
        times = numpy.random.uniform(0, math.pi*2, base_states.shape[0])
        from_states = self.goto_time(base_states, times)
        to_states = self.goto_time(base_states, times+self.DT*self.dt)
        
        return from_states, to_states
    
    def generate_testing_sequence(self, num_frames):
        a = numpy.random.uniform(*self.A_LIMITS)
        b = numpy.random.uniform(*self.B_LIMITS)
        c = numpy.random.uniform(*self.C_LIMITS)
        
        state = numpy.hstack((a, b, c))
        state = numpy.reshape(state, (1,)+state.shape)
        states = numpy.zeros((num_frames, state.size))

        t = numpy.random.uniform(0, math.pi*2)

        for i in xrange(num_frames):
            states[i,:] = self.goto_time(state, t)
            t += self.dt*self.DT
        
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

    def generate_metadata(self, obj_i):
        return {"dl": self.dl,
                "length": self.length,
                "width": self.width,
                "translate": self.translate[obj_i]}
