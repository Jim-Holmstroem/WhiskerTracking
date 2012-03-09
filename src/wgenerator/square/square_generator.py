import math
import cairo
import numpy
import os
from wmedia import left_align_videoformat
from wdb import delete_database, StateTransitionDatabase

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
    
    print "Rendering pngvin movie", movie_name
    
    delete_database(movie_name)
    db = StateTransitionDatabase(movie_name, 2)
    
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
    
    print "Rendering pngvin movie", movie_name
    
    delete_database(movie_name)
    db = StateTransitionDatabase(movie_name, 2)
    
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

if (__name__=='__main__'):
    render_simple()
    render_online()
