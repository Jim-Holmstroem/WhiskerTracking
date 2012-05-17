from itertools import izip
from wgenerator.generator import Generator
from wgenerator.settings import IMAGE_WIDTH, IMAGE_HEIGHT
from wmedia.wvideo import wvideo
from wview import SquareRenderer
import cairo
import math
import numpy

__all__ = ["AcceleratingSquareGenerator", "AcceleratingSquareWithoutVelocityGenerator", "SimpleSquareGenerator" , "OnlineSquareGenerator"]

def velocities(states, accel_func):
    stack = []
    map(stack.extend, ((states[:,i], numpy.zeros(states.shape[0])) for i in xrange(1, states.shape[1], 2)))
    return numpy.vstack(stack).T + accel_func(states)
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

class SquareGenerator(Generator):

    renderer = SquareRenderer(50)

    def generate_testing_movie(self, all_squares_positions):
        surfaces = [cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT) for i in xrange(len(all_squares_positions[0]))]
        contexts = [cairo.Context(surface) for surface in surfaces]
        
        for context in contexts:
            #context.scale(IMAGE_WIDTH, IMAGE_HEIGHT) # Normalize the canvas

            context.rectangle(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT)
            context.set_source_rgb(0,0,0)
            context.fill()

        for positions in all_squares_positions:
            for pos, context in izip(positions, contexts):
                self.renderer.render(context, pos)
        
        return wvideo(surfaces)

class AcceleratingSquareGenerator(SquareGenerator):

    PARAMETER_GROUPS = [2, 2]

    X_STD = IMAGE_WIDTH/15.0
    Y_STD = IMAGE_HEIGHT/15.0
    VX_STD = IMAGE_WIDTH/200.0
    VY_STD = IMAGE_HEIGHT/200.0
    
    def accel_func(self, a):
        return numpy.array((0, 0, 0, 0.1))
    
    def generate_training_transitions(self):
    
        from_states = numpy.vstack((numpy.zeros(self.number_of_transitions),
                                    numpy.random.normal(0, self.VX_STD, self.number_of_transitions),
                                    numpy.zeros(self.number_of_transitions),
                                    numpy.random.normal(0, self.VY_STD, self.number_of_transitions)
                                    )).T
        to_states = timestep(from_states, self.accel_func, dt=self.dt)
        
        return from_states, to_states
    
    def generate_testing_sequence(self, num_frames):
        state = numpy.hstack((numpy.random.normal(IMAGE_WIDTH/2.0, self.X_STD),
                              numpy.random.normal(0, self.VX_STD),
                              numpy.random.normal(IMAGE_HEIGHT/2.0, self.Y_STD,),
                              numpy.random.normal(0, self.VY_STD)))
        state = numpy.reshape(state, (1,)+state.shape)
        states = numpy.zeros((num_frames, state.size))
        
        for i in xrange(num_frames):
            states[i,:] = state
            state = timestep(state, self.accel_func)
        
        return numpy.array(states)
    
    def generate_testing_movie(self, all_squares_states):
        return SquareGenerator.generate_testing_movie(self, all_squares_states[:,:,::2])

class AcceleratingSquareWithoutVelocityGenerator(SquareGenerator):

    PARAMETER_GROUPS = [1, 1]

    X_STD = IMAGE_WIDTH/15.0
    Y_STD = IMAGE_HEIGHT/15.0
    VX_STD = IMAGE_WIDTH/200.0
    VY_STD = IMAGE_HEIGHT/200.0
    
    def accel_func(self, a):
        return numpy.array((0, 0, 0, 0.1))
    
    def generate_training_transitions(self):
    
        from_states = numpy.vstack((numpy.random.uniform(0, IMAGE_WIDTH, self.number_of_transitions),
                                    numpy.random.normal(0, self.VX_STD, self.number_of_transitions),
                                    numpy.random.uniform(0, IMAGE_HEIGHT, self.number_of_transitions),
                                    numpy.random.normal(0, self.VY_STD, self.number_of_transitions)
                                    )).T
        to_states = timestep(from_states, self.accel_func, dt=self.dt)
        
        return from_states[:,::2], to_states[:,::2]
    
    def generate_testing_sequence(self, num_frames):
        state = numpy.hstack((numpy.random.normal(IMAGE_WIDTH/2.0, self.X_STD),
                              numpy.random.normal(0, self.VX_STD),
                              numpy.random.normal(IMAGE_HEIGHT/2.0, self.Y_STD,),
                              numpy.random.normal(0, self.VY_STD)))
        state = numpy.reshape(state, (1,)+state.shape)
        states = numpy.zeros((num_frames, state.size))
        
        for i in xrange(num_frames):
            states[i,:] = state
            state = timestep(state, self.accel_func)
        
        return states[:,::2]

    def generate_metadata(self, obj_i):
        return {}

class SimpleSquareGenerator(AcceleratingSquareGenerator):
    """
    Renders a spinning square moving in a straight line.
    """

    THETA_STD = 2*math.pi/10
    PARAMETER_GROUPS = [2, 2, 2]

    def accel_func(self, a):
        return numpy.zeros(sum(self.PARAMETER_GROUPS))
    
    def generate_training_transitions(self):
    
        from_states = numpy.vstack((numpy.zeros(self.number_of_transitions),
                                    numpy.random.normal(0, self.X_STD, self.number_of_transitions),
                                    numpy.zeros(self.number_of_transitions),
                                    numpy.random.normal(0, self.Y_STD, self.number_of_transitions),
                                    numpy.zeros(self.number_of_transitions),
                                    numpy.random.normal(0, self.THETA_STD, self.number_of_transitions)
                                    )).T
        to_states = timestep(from_states, self.accel_func, dt=self.dt)
        
        return from_states, to_states
    
    def generate_testing_sequence(self, num_frames):
        state = numpy.hstack((numpy.random.normal(IMAGE_WIDTH/2.0, self.X_STD),
                              numpy.random.normal(0, IMAGE_WIDTH/200.),
                              numpy.random.normal(IMAGE_HEIGHT/2.0, self.Y_STD),
                              numpy.random.normal(0, IMAGE_HEIGHT/200.),
                              numpy.random.normal(0, self.THETA_STD),
                              numpy.random.normal(0, self.THETA_STD/10)
                              ))
        state = numpy.reshape(state, (1,)+state.shape)
        states = numpy.zeros((num_frames, state.size))
        
        for i in xrange(num_frames):
            states[i,:] = state
            state = timestep(state, self.accel_func)
        
        return states

    def generate_testing_movie(self, all_squares_states):
        surfaces = [cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT) for i in xrange(len(all_squares_states[0]))]
        contexts = [cairo.Context(surface) for surface in surfaces]
        
        for context in contexts:
            #context.scale(IMAGE_WIDTH, IMAGE_HEIGHT) # Normalize the canvas

            context.rectangle(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT)
            context.set_source_rgb(0,0,0)
            context.fill()

        for states in all_squares_states:
            for state, context in izip(states, contexts):
                self.renderer.render(context, (state[0], state[2]), state[4])

        return wvideo(surfaces)

class OnlineSquareGenerator(SimpleSquareGenerator):

    LINE_WIDTH = 5

    def generate_testing_movie(self, all_squares_states):
        surfaces = [cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT) for i in xrange(len(all_squares_states[0]))]
        contexts = [cairo.Context(surface) for surface in surfaces]
        
        for context in contexts:
            #context.scale(IMAGE_WIDTH, IMAGE_HEIGHT) # Normalize the canvas

            context.rectangle(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT)
            context.set_source_rgb(0,0,0)
            context.fill()

        for states in all_squares_states:
            for state, context in izip(states, contexts):
                self.renderer.render(context, (state[0], state[2]), state[4])

                # Render line
                context.identity_matrix()
                context.set_source_rgb(1,1,1)
                context.move_to(0,0)
                context.line_to(IMAGE_WIDTH,IMAGE_HEIGHT)
                context.set_line_width(self.LINE_WIDTH)
                context.stroke()
        
        return wvideo(surfaces)

def run():
    ag = AcceleratingSquareGenerator("square_accelerating", 2, 1000)
    ag.generate()

if __name__ == "__main__":
    import cProfile
    cProfile.run("run()")
