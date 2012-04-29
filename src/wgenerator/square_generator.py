from itertools import izip
from wgenerator.generator import Generator
from wgenerator.settings import IMAGE_WIDTH, IMAGE_HEIGHT
from wmedia.wvideo import wvideo
import cairo
import numpy
__all__ = ["AcceleratingSquareGenerator"]

def velocities(states, accel_func):
    return numpy.vstack((states[:,1],
                       numpy.zeros(states.shape[0]),
                       states[:,3],
                       numpy.zeros(states.shape[0])
                       )).T + accel_func(states)

def timestep(states, accel_func, fixpoint_iterations=10, dt=1):
    next_states = states
    d0 = velocities(states, accel_func)
    for i in xrange(fixpoint_iterations):
        d = velocities(next_states, accel_func)
        next_states = states + 0.5 * (d0 + d) * dt
    return next_states

class AcceleratingSquareGenerator(Generator):

    SQUARE_SIDE = 50    
    X_STD = IMAGE_WIDTH/15.0
    Y_STD = IMAGE_HEIGHT/15.0
    
    def accel_func(self, a):
        return numpy.array((0, 0, 0, 0.1))
    
    def generate_training_transitions(self):
    
        from_states = numpy.vstack((numpy.zeros(self.number_of_transitions),
                                    numpy.random.normal(0, self.X_STD, self.number_of_transitions),
                                    numpy.zeros(self.number_of_transitions),
                                    numpy.random.normal(0, self.Y_STD, self.number_of_transitions)
                                    )).T
        to_states = timestep(from_states, self.accel_func, dt=self.dt)
        
        return from_states, to_states
    
    def generate_testing_sequence(self, num_frames):
        state = numpy.hstack((numpy.random.normal(IMAGE_WIDTH/2.0, self.X_STD),
                              numpy.random.normal(0, IMAGE_WIDTH/200.),
                              numpy.random.normal(IMAGE_HEIGHT/2.0, self.Y_STD,),
                              numpy.random.normal(0, IMAGE_HEIGHT/200.)))
        state = numpy.reshape(state, (1,)+state.shape)
        states = numpy.zeros((num_frames, state.size))
        
        for i in xrange(num_frames):
            states[i,:] = state
            state = timestep(state, self.accel_func)
        
        return states

    def generate_testing_movie(self, states):
        surfaces = [cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT) for i in xrange(len(states))]
        contexts = [cairo.Context(surface) for surface in surfaces]
        
        for state, context in izip(states, contexts):

            context.scale(IMAGE_WIDTH, IMAGE_HEIGHT) # Normalize the canvas

            x = (state[0]-self.SQUARE_SIDE/2)/IMAGE_WIDTH
            y = (state[2]-self.SQUARE_SIDE/2)/IMAGE_HEIGHT
            
            context.rectangle(0, 0, 1, 1)
            context.set_source_rgb(0,0,0)
            context.fill()
            
            context.set_source_rgb(1, 1, 1)
            context.rectangle(x, y, float(self.SQUARE_SIDE)/IMAGE_WIDTH, float(self.SQUARE_SIDE)/IMAGE_WIDTH)
            context.fill()
            
        return wvideo(surfaces)

def run():
    ag = AcceleratingSquareGenerator("square_accelerating", [2, 2], 1000)
    ag.generate()

if __name__ == "__main__":
    import cProfile
    cProfile.run("run()")
