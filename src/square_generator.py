import math
import cairo


# NOTE
# Could use String.format instead but some functionality is missing in python 2.*
#
def left_align_videoformat(i):
    assert(len(str(i))<=5)
    return ('0'*(5-len(str(i))))+str(i)

def clear(ctx):
    ctx.identity_matrix() 
    ctx.scale(WIDTH, HEIGHT) # Normalizing the canvas



WIDTH = 256
HEIGHT = 256

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)


for i in range(32):
    clear(ctx)

    ctx.set_source_rgb(0,0,0)
    ctx.rectangle(0, 0, 1, 1) 
    ctx.fill()

    ctx.set_source_rgb(1, 1, 1)
    ctx.translate(0.2+0.02*i, 0.2+0.02*i)
    ctx.rotate(2.0*math.pi/32.0*i)
    ctx.rectangle(-0.05,-0.05,0.1, 0.1)
    ctx.fill()
   

    #obsticle
    clear(ctx)
    ctx.set_source_rgb(1,1,1)
    ctx.move_to(0,0)
    ctx.line_to(1,1)
    ctx.set_line_width(0.02)
    ctx.stroke()

    


    surface.write_to_png("../data/square_stair/frame-"+left_align_videoformat(i)+".png") # Output to PNG


