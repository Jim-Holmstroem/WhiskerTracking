from wdb import create_database, delete_database, StateTransitionDatabase
from wmedia import left_align_videoformat
import cairo
import math
import numpy
import os

IMAGE_WIDTH=512
IMAGE_HEIGHT=512

def clear(ctx):
    """
    To clear the Cairo.Context and
    """
    ctx.identity_matrix() 
    ctx.scale(IMAGE_WIDTH, IMAGE_HEIGHT) # Normalizing the canvas

def generate_pendulum(number_of_transitions, l, g=9.81, dt=0.001, radius=10):
    """
    Generates number_of_transitions random movements of a pendulum with start
    angle theta_0 from the y axis
    """
    
    dataset = "pendulum"
    
    # State: [x, y, x', y']
    delete_database(dataset)
    create_database(dataset, [1])
    
    print "Generating %i random accelerating movements"%(number_of_transitions)
    db = StateTransitionDatabase(dataset)
    
    omega = math.sqrt(float(g)/l)
    T = 2*math.pi*1.0/omega
    
    theta_0 = numpy.random.uniform(math.radians(-20), math.radians(20), (number_of_transitions, 1))
    t = numpy.random.uniform(0, T, (number_of_transitions, 1))
    
    from_phi = theta_0 * numpy.cos(omega*t)
    to_phi = theta_0 * numpy.cos(omega*(t+dt))
    
    db.add_transitions(from_phi, to_phi)
    
    print "Done."
    
    print "Generating movement sequences for testing..."
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
        
        theta_0 = numpy.random.uniform(math.radians(-20),math.radians(20))
        t = numpy.atleast_2d(numpy.linspace(0, 3*T, num_frames)).T
        
        phi = theta_0 * numpy.cos(omega*t)
        
        for i in xrange(num_frames):
            x = (IMAGE_WIDTH/2 + l*numpy.sin(phi[i]))/IMAGE_WIDTH
            y = l*numpy.cos(phi[i])/IMAGE_HEIGHT
            
            clear(ctx)
            ctx.rectangle(0, 0, 1, 1)
            ctx.set_source_rgb(0,0,0)
            ctx.fill()
            
            ctx.set_source_rgb(1, 1, 1)
#            ctx.rectangle(x, y, 10, 10)
            ctx.arc(x, y, float(radius)/IMAGE_WIDTH, 0., 2 * math.pi)
            ctx.fill()
            
            surface.write_to_png(os.path.join(save_dir, "frame-"+left_align_videoformat(i)+".png"))
        
        numpy.save(os.path.join(save_dir, "state_sequence.npy"), phi)
    
    print "Done."
    
if (__name__=='__main__'):
#    render_simple()
#    render_online()
#    render_bounce()
    generate_pendulum(1000, 400)
