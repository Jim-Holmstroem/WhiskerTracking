import math
import cairo
import numpy
import os
from wmedia import left_align_videoformat
from wdb import create_database, delete_database, StateTransitionDatabase

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
    save_dir = "data/"+movie_name+".pngvin"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    print "Rendering pngvin movie", movie_name
    
    delete_database(movie_name)
    create_database(movie_name, number_of_parameters=2)
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

        surface.write_to_png(save_dir+"/frame-"+left_align_videoformat(i)+".png")

        if i>0:
            # Input the transition into the database
            new_state = numpy.array([IMAGE_WIDTH*(x0+dx*i), IMAGE_WIDTH*(y0+dy*i), theta0+dtheta*i])
            db.add_transition(prev_state[:2], new_state[:2])
            prev_state = new_state
        
        print "Rendered frame", i
    
    print "Done."

def render_online():
    """
    Renders a spinning square moving on a straight line.
    """
    movie_name = "square_online"
    save_dir = "data/"+movie_name+".pngvin"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    print "Rendering pngvin movie", movie_name
    
    delete_database(movie_name)
    create_database(movie_name, number_of_parameters=2)
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

        surface.write_to_png(save_dir+"/frame-"+left_align_videoformat(i)+".png")

        if i>0:
            # Input the transition into the database
            new_state = numpy.array([IMAGE_WIDTH*(x0+dx*i), IMAGE_WIDTH*(y0+dy*i), theta0+dtheta*i])
            db.add_transition(prev_state[:2], new_state[:2])
            prev_state = new_state
        
        print "Rendered frame", i
    
    print "Done."

def render_bounce(movie_id=0, start_state=None, gravity=numpy.array([0, 9.81]), bounce_factor=0.75, input_to_database=True):
    """
    Renders a falling and bouncing square.
    """
    
    dataset = "square_bounce"
    num_frames = 128
    dt = 0.1
    square_side = 50.
    half_square_side = square_side/2
    
    # State: [x, y, x', y']
    if start_state is None:
        delete_database(dataset)
        create_database(dataset, number_of_parameters=4)
        render_bounce(0, numpy.array([IMAGE_WIDTH/2, 0, 0., 0.]))
        render_bounce(1, numpy.array([IMAGE_WIDTH/2, 0, 10., 0.]))
        render_bounce(2, numpy.array([IMAGE_WIDTH*2/3, IMAGE_HEIGHT/2, -25., -45.]))
        render_bounce(3, numpy.array([IMAGE_WIDTH/2, IMAGE_HEIGHT-square_side, 0., 0.]))
        render_bounce(4, numpy.array([IMAGE_WIDTH/2, IMAGE_HEIGHT-square_side, 0., 150]))
        render_bounce(5, numpy.array([IMAGE_WIDTH/2, IMAGE_HEIGHT-square_side, 20., 50.]))
        render_bounce(6, numpy.array([IMAGE_WIDTH/2, IMAGE_HEIGHT/2, 300., 0.]))
        render_bounce(7, numpy.array([0, 0, 50., 0.]))
        render_bounce(8, numpy.array([IMAGE_WIDTH/2, IMAGE_HEIGHT*3/4, -30., 85.]))
        render_bounce(9, numpy.array([IMAGE_WIDTH/5, IMAGE_HEIGHT/3, 5., 17.]))
        return
    
    movie_name = dataset + "_" + str(movie_id)
    save_dir = "data/" + movie_name + ".pngvin"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    print "Rendering pngvin movie", movie_name
    
    db = StateTransitionDatabase(dataset)
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT)
    ctx = cairo.Context(surface)
    
    state = start_state
    state[:2] += half_square_side
    
    print "Initial values:", state
    
    X_LIMITS = [half_square_side, IMAGE_WIDTH-half_square_side]
    Y_LIMITS = [half_square_side, IMAGE_HEIGHT-half_square_side]
    
    for i in xrange(num_frames):
        next_state = state + numpy.concatenate([state[2:4], gravity])*dt

        # Collisions        
        for axis, limits in enumerate((X_LIMITS, Y_LIMITS)):
            if next_state[axis] < limits[0]:
                next_state[axis+2] *= -bounce_factor
                next_state[axis] = 2*limits[0] - next_state[axis]
            elif next_state[axis] > limits[1]:
                next_state[axis+2] *= -bounce_factor
                next_state[axis] = 2*limits[1] - next_state[axis]
            
        if i>0:
            # Input the transition into the database
            db.add_transition(state, next_state)
        
        state = next_state
        
        x = (state[0]-half_square_side)/IMAGE_WIDTH
        y = (state[1]-half_square_side)/IMAGE_HEIGHT
        

        clear(ctx)
        ctx.rectangle(0, 0, 1, 1)
        ctx.set_source_rgb(0,0,0)
        ctx.fill()
        
        ctx.set_source_rgb(1, 1, 1)
        ctx.rectangle(x, y, square_side/IMAGE_WIDTH, square_side/IMAGE_WIDTH)
        ctx.fill()

        surface.write_to_png(save_dir+"/frame-"+left_align_videoformat(i)+".png")

    print "Completed rendering", movie_name

if (__name__=='__main__'):
    render_simple()
    render_online()
    render_bounce()
