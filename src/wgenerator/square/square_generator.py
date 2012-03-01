import math
import cairo
import numpy
from wmedia import left_align_videoformat
from wdb import StateTransitionDatabase

"""
Only used to generate square test-data, nothing more.
"""

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256

movie_name = "square_obstacle"
save_dir = "data/"+movie_name+".pngvin"

def clear(ctx):
    """
    To clear the Cairo.Context and
    """
    ctx.identity_matrix() 
    ctx.scale(IMAGE_WIDTH, IMAGE_HEIGHT) # Normalizing the canvas

def render_movie():
    db = StateTransitionDatabase("data/transition-db/"+movie_name+".db")
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT)
    ctx = cairo.Context(surface)

    raw_input("Press enter to continue rendering pngvin movie...")

    num_frames=32
    
    x0 = 0.2
    y0 = 0.2
    
    dx=0.02
    dy=0.02
    width=0.1
    
    prev_state = db.add_state(numpy.array([x0, y0]))

    for i in xrange(num_frames):
        clear(ctx)

        ctx.set_source_rgb(0,0,0)
        ctx.rectangle(0, 0, 1, 1)
        ctx.fill()

        ctx.set_source_rgb(1, 1, 1)
        ctx.translate(x0+dx*i, y0+dy*i)
        ctx.rotate(2.0*math.pi/num_frames*i)
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

        # Input the transition into the database
        new_state = db.add_state(numpy.array([x0+dx*i, y0+dy*i]))
        db.add_transition(prev_state, new_state)
        prev_state = new_state

if (__name__=='__main__'):
    render_movie()
