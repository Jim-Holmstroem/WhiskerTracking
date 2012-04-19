from wdb import create_database, delete_database, StateTransitionDatabase
from wmedia import left_align_videoformat
import cairo
import math
import numpy
import os

"""
Only used to generate square test-data, nothing more.
"""

IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512

def clear(ctx):
    """
    To clear the Cairo.Context and
    """
    ctx.identity_matrix() 
    ctx.scale(IMAGE_WIDTH, IMAGE_HEIGHT) # Normalizing the canvas

def render_simple():
    """
    Renders a spinning square moving in a straight line.
    """
    movie_name = "square_simple"
    save_dir = os.path.join("video", movie_name+".pngvin")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    print "Rendering pngvin movie", movie_name
    
    delete_database(movie_name)
    create_database(movie_name, [2])
    db = StateTransitionDatabase(movie_name)
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT)
    ctx = cairo.Context(surface)
    
    num_frames=32
    
    x0 = 0.2
    y0 = 0.2
    theta0 = 0.0
    
    dx=0.02
    dy=0.02
    dtheta=2.0*math.pi/num_frames
    width=0.1
    
    prev_state = numpy.array([IMAGE_WIDTH*x0, IMAGE_WIDTH*y0, theta0])

    for i in xrange(num_frames):
        clear(ctx)

        ctx.set_source_rgb(0,0,0)
        ctx.rectangle(0, 0, 1, 1)
        ctx.fill()

        ctx.set_source_rgb(1, 1, 1)
        ctx.translate(x0+dx*i, y0+dy*i)
        ctx.rotate(theta0+dtheta*i)
        ctx.rectangle(-width/2, -width/2, width, width)
        ctx.fill()

        surface.write_to_png(os.path.join(save_dir, "frame-"+left_align_videoformat(i)+".png"))

        if i>0:
            # Input the transition into the database
            new_state = numpy.array([IMAGE_WIDTH*(x0+dx*i), IMAGE_WIDTH*(y0+dy*i), theta0+dtheta*i])
            db.add_transitions(prev_state[:2], new_state[:2])
            prev_state = new_state
        
        print "Rendered frame", i
    
    print "Done."

def render_online():
    """
    Renders a spinning square moving on a straight line.
    """
    movie_name = "square_online"
    save_dir = os.path.join("video", movie_name+".pngvin")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    print "Rendering pngvin movie", movie_name
    
    delete_database(movie_name)
    create_database(movie_name, [2])
    db = StateTransitionDatabase(movie_name)
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT)
    ctx = cairo.Context(surface)
    
    num_frames=32
    
    x0 = 0.2
    y0 = 0.2
    theta0 = 0.0
    
    dx=0.02
    dy=0.02
    dtheta=2.0*math.pi/num_frames
    width=0.1
    
    prev_state = numpy.array([IMAGE_WIDTH*x0, IMAGE_WIDTH*y0, theta0])

    for i in xrange(num_frames):
        clear(ctx)

        ctx.set_source_rgb(0,0,0)
        ctx.rectangle(0, 0, 1, 1)
        ctx.fill()

        ctx.set_source_rgb(1, 1, 1)
        ctx.translate(x0+dx*i, y0+dy*i)
        ctx.rotate(theta0+dtheta*i)
        ctx.rectangle(-width/2, -width/2, width, width)
        ctx.fill()

        # Render Obstacle
        clear(ctx)
        ctx.set_source_rgb(1,1,1)
        ctx.move_to(0,0)
        ctx.line_to(1,1)
        ctx.set_line_width(0.02)
        ctx.stroke()

        surface.write_to_png(os.path.join(save_dir, "frame-"+left_align_videoformat(i)+".png"))

        if i>0:
            # Input the transition into the database
            new_state = numpy.array([IMAGE_WIDTH*(x0+dx*i), IMAGE_WIDTH*(y0+dy*i), theta0+dtheta*i])
            db.add_transitions(prev_state[:2], new_state[:2])
            prev_state = new_state
        
        print "Rendered frame", i
    
    print "Done."

def render_bounce(movie_id=0, start_state=None, gravity=numpy.array([0, 1]), bounce_factor=0.75, input_to_database=True):
    """
    Renders a falling and bouncing square.
    """
    
    dataset = "square_bounce"
    num_frames = 128
    square_side = 50.
    half_square_side = square_side/2.0
    
    dt = 0.5
    
    X_LIMITS = [half_square_side, IMAGE_WIDTH-half_square_side]
    Y_LIMITS = [half_square_side, IMAGE_HEIGHT-half_square_side]
    
    # State: [x, y, x', y']
    if start_state is None:
        delete_database(dataset)
        create_database(dataset, [2, 2])
        render_bounce(0, numpy.array([IMAGE_WIDTH/2., 0., Y_LIMITS[0], 0.]))
        render_bounce(1, numpy.array([IMAGE_WIDTH/2., 2., Y_LIMITS[0], 0.]))
        render_bounce(2, numpy.array([IMAGE_WIDTH*2./3, -1, IMAGE_HEIGHT/2., -0.4]))
        render_bounce(3, numpy.array([IMAGE_WIDTH/4., 0., Y_LIMITS[1], 0.]))
        render_bounce(4, numpy.array([IMAGE_WIDTH*3./4, 0., Y_LIMITS[1], 2]))
        render_bounce(5, numpy.array([IMAGE_WIDTH/2., 4, Y_LIMITS[1], 0.6]))
        render_bounce(6, numpy.array([IMAGE_WIDTH/2., 4., IMAGE_HEIGHT/2., 0.]))
        render_bounce(7, numpy.array([X_LIMITS[0], 5., Y_LIMITS[0], 0.]), input_to_database=False)
        render_bounce(8, numpy.array([IMAGE_WIDTH/2., -1, IMAGE_HEIGHT*3./4, 0.6]), input_to_database=False)
        render_bounce(9, numpy.array([IMAGE_WIDTH/5., 2, IMAGE_HEIGHT/3., 0.4]), input_to_database=False)
        return
    
    movie_name = dataset + "_" + str(movie_id)
    save_dir = os.path.join("video", movie_name + ".pngvin")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    print "Rendering pngvin movie", movie_name
    
    db = StateTransitionDatabase(dataset)
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT)
    ctx = cairo.Context(surface)
    
    state = start_state
#    state[:2] += half_square_side
    
    print "Initial values:", state
    
    def timestep(state, fixpoint_iterations=10):
        next_state = state
        d0 = numpy.array((state[1], gravity[0], state[3], gravity[1]))
        for i in xrange(fixpoint_iterations):
            d = numpy.array((next_state[1], gravity[0], next_state[3], gravity[1]))
            next_state = state + 0.5 * (d0 + d) * dt
        return next_state
    
    for i in xrange(num_frames):
        
        if i>0:
            next_state = timestep(state)

            # Collisions with edges
            for axis, limits in ((0, X_LIMITS), (2, Y_LIMITS)):
                if next_state[axis] < limits[0]:
                    next_state[axis+1] *= -bounce_factor
                    next_state[axis] = 2*limits[0] - next_state[axis]
                elif next_state[axis] > limits[1]:
                    next_state[axis+1] *= -bounce_factor
                    next_state[axis] = 2*limits[1] - next_state[axis]
            
            if input_to_database:
                # Input the transition into the database
                normalizer = numpy.array((state[0], 0, state[2], 0))
                db.add_transitions(state - normalizer, next_state - normalizer)
        
            state = next_state
        
        x = (state[0]-half_square_side)/IMAGE_WIDTH
        y = (state[2]-half_square_side)/IMAGE_HEIGHT
        
        clear(ctx)
        ctx.rectangle(0, 0, 1, 1)
        ctx.set_source_rgb(0,0,0)
        ctx.fill()
        
        ctx.set_source_rgb(1, 1, 1)
        ctx.rectangle(x, y, square_side/IMAGE_WIDTH, square_side/IMAGE_WIDTH)
        ctx.fill()
        
        surface.write_to_png(os.path.join(save_dir, "frame-"+left_align_videoformat(i)+".png"))

    print "Completed rendering", movie_name

def generate_accelerating(number_of_transitions, accel_func=lambda a:numpy.array((0,0,0,0.1)), debug=False):
    """
    Generates number_of_transitions random movements of objects subject to acceleration given by accel_func
    """
    
    dataset = "square_accelerating"
    dt = 1
    X_STD = IMAGE_WIDTH/15.0
    Y_STD = IMAGE_HEIGHT/15.0
    
    # State: [x, y, x', y']
    delete_database(dataset)
    create_database(dataset, [2, 2])
    
    print "Generating %i random accelerating movements"%(number_of_transitions)
    db = StateTransitionDatabase(dataset)
    
    
    def velocities(states):
        return numpy.vstack((states[:,1],
                           numpy.zeros(states.shape[0]),
                           states[:,3],
                           numpy.zeros(states.shape[0])
                           )).T + accel_func(states)
    
    def timestep(states, fixpoint_iterations=10):
        next_states = states
        d0 = velocities(states)
        for i in xrange(fixpoint_iterations):
            d = velocities(next_states)
            next_states = states + 0.5 * (d0 + d) * dt
        return next_states
    
    from_states = numpy.vstack((numpy.zeros(number_of_transitions),
                                numpy.random.normal(0, X_STD, number_of_transitions),
                                numpy.zeros(number_of_transitions),
                                numpy.random.normal(0, Y_STD, number_of_transitions)
                                )).T
    to_states = timestep(from_states)
    
    db.add_transitions(from_states, to_states)
    
    print "Done."
    
    print "Generating movement sequences for testing..."
    square_side = 50.0
    num_movies = 10
    num_frames = int(number_of_transitions * 3.0/7 /num_movies)   # The 70-30 principle
    
    for movie_id in xrange(num_movies):
        movie_name = dataset + "_" + str(movie_id)
        save_dir = os.path.join("video", movie_name + ".pngvin")
        import shutil
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)
        os.makedirs(save_dir)
        
        print "Rendering pngvin movie", movie_name
        
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT)
        ctx = cairo.Context(surface)
        
        state = numpy.hstack((numpy.random.normal(IMAGE_WIDTH/2.0, X_STD),
                              numpy.random.normal(0, IMAGE_WIDTH/200.),
                              numpy.random.normal(IMAGE_HEIGHT/2.0, Y_STD,),
                              numpy.random.normal(0, IMAGE_HEIGHT/200.)))
        state = numpy.reshape(state, (1,)+state.shape)
        
        states = numpy.zeros((num_frames, state.size))
        
        for i in xrange(num_frames):
            x = (state[0,0]-square_side/2)/IMAGE_WIDTH
            y = (state[0,2]-square_side/2)/IMAGE_HEIGHT
            
            clear(ctx)
            ctx.rectangle(0, 0, 1, 1)
            ctx.set_source_rgb(0,0,0)
            ctx.fill()
            
            ctx.set_source_rgb(1, 1, 1)
            ctx.rectangle(x, y, square_side/IMAGE_WIDTH, square_side/IMAGE_WIDTH)
            ctx.fill()
            
            surface.write_to_png(os.path.join(save_dir, "frame-"+left_align_videoformat(i)+".png"))
            states[i,:] = state
            
            state = timestep(state)
        
        numpy.save(os.path.join(save_dir, "state_sequence.npy"), states)
    
    print "Done."
    
    if debug:
        import matplotlib.pyplot as plot
        plot.hist(from_states[:,1::2], 20)
        plot.show()
    
if (__name__=='__main__'):
#    render_simple()
#    render_online()
    render_bounce()
    generate_accelerating(1000)
