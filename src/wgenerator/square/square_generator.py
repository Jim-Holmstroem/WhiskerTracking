import math
import cairo
from wmedia import left_align_videoformat

"""
Only used to generate square test-data, nothing more.
"""

IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256

def clear(ctx):
    """
    To clear the Cairo.Context and
    """
    ctx.identity_matrix() 
    ctx.scale(IMAGE_WIDTH, IMAGE_HEIGHT) # Normalizing the canvas

def render_movie():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT)
    ctx = cairo.Context(surface)

    raw_input("Press enter to continue rendering pngvin movie...")

    num_frames=32
    dx=0.02
    dy=0.02
    width=0.1

    for i in xrange(num_frames):
        clear(ctx)

        ctx.set_source_rgb(0,0,0)
        ctx.rectangle(0, 0, 1, 1)
        ctx.fill()

        ctx.set_source_rgb(1, 1, 1)
        ctx.translate(0.2+dx*i, 0.2+dy*i)
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

        surface.write_to_png("../data/square_new.pngvin/frame-"+left_align_videoformat(i)+".png")

if (__name__=='__main__'):
    render_movie()
