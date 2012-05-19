import math
import numpy
from wgenerator import GWhiskerGenerator

class RWhiskerGenerator(GWhiskerGenerator):
    """Generates database for use when tracking real whiskers."""

    A_LIMITS = 0.000016 * numpy.array((0, 1))
    B_LIMITS = 0.004 * numpy.array((0, 1))
    C_LIMITS = 2 * numpy.array((0, 1))

    def __init__(self, *args, **kwargs):
        kwargs['WHISKER_LENGTH'] = 200
        kwargs['WHISKER_WIDTH'] = 1
        GWhiskerGenerator.__init__(self, *args, **kwargs)

    def goto_time(self, base_states, t):
        return base_states * numpy.vstack((numpy.sin(t), numpy.sin(t), numpy.sin(t))).T
