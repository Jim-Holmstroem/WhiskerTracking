from pf import pf
from time import time
from wdb import StateTransitionDatabase
from wmedia import wvideo as video, left_align_videoformat
from wmedia.square_particles_animator import square_particles_animator
import cProfile
import cairo
import numpy
import os

def goodness(particle, image):
    x, y = (particle[0], particle[2])
    
    if x < 0 or y < 0 or y >= image.shape[0] or x >= image.shape[1]:
        return 0
    
    if (image[y,x,:3] == 255).all():
        return 1000
    else:
        return 1

def sample(prev_particle):
    
    next_pos = prev_particle.copy()
    next_pos[0] += prev_particle[1]
    next_pos[1] += 9.81
    next_pos[2] += prev_particle[3]
    next_pos[3] += 9.81
    new_particle_from_prev = next_pos + numpy.random.normal(loc=0, scale=5, size=prev_particle.shape)
    
    prev_particle_copy = prev_particle.copy()
    prev_particle_copy[0] = 0
    prev_particle_copy[2] = 0
    new_particle_from_db = db.sample_weighted_average(prev_particle_copy)
    new_particle_from_db[0] += prev_particle[0]
    new_particle_from_db[2] += prev_particle[2]
#    new_particle_from_db += numpy.random.normal(0, scale=[3, 3], size=new_particle_from_db.shape)
    
    db_weight = 1
    prev_weight = 1
    
    new_particle = new_particle_from_prev*prev_weight + (new_particle_from_db)*db_weight
    new_particle /= db_weight + prev_weight
    return new_particle

IMAGE_WIDTH = 512.
IMAGE_HEIGHT = 512.

dataset = "square_bounce"
db = StateTransitionDatabase(dataset)
num_particles = 100
    
square_side = 50
half_square_side = square_side/2.0
X_LIMITS = [half_square_side, IMAGE_WIDTH-half_square_side]
Y_LIMITS = [half_square_side, IMAGE_HEIGHT-half_square_side]

def run(movie_id):
    movie = dataset + "_" + str(movie_id)
    save_img_dir = os.path.join("run", "square_tracker_bounce-%i.pngvin"%(movie_id))
    if(not os.path.exists(save_img_dir)):
        os.makedirs(save_img_dir)
    
    print("Starting up...")
    
    print("Loading video...")
    v = video(os.path.join("video", movie+".pngvin")) # Dimensions: x, y, rgba
    print("Video loaded.")
    #particles = numpy.random.uniform(0, max(v[0].get_copy_of_current_image().size)-1, (num_particles, 2))
    #particles = numpy.random.normal(size=(num_particles, 2), scale=10) + numpy.array([51, 51])
    #start_state = numpy.array([102, 102, 0])
    
    num_frames = len(v)
    
    start_states = {
            7:numpy.array([X_LIMITS[0], 5., Y_LIMITS[0], 0.]),
            8:numpy.array([IMAGE_WIDTH/2., -1, IMAGE_HEIGHT*3./4, 0.6]),
            9:numpy.array([IMAGE_WIDTH/5., 2, IMAGE_HEIGHT/3., 0.4])}
    
    particles = numpy.array([start_states[movie_id]]*num_particles)
    intermediate_particles = particles.copy()
    spa = square_particles_animator(numpy.zeros((num_frames, num_particles, start_states[movie_id].size)), square_side, intermediate_particles=numpy.zeros((num_frames, num_particles, start_states[movie_id].size)))
    
    imageSurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(IMAGE_WIDTH), int(IMAGE_HEIGHT))
    context = cairo.Context(imageSurface)
    
    def render(i, frame):
        spa.particles[i] = particles.copy()
        spa.intermediate_particles[i] = intermediate_particles.copy()
        
        frame.render(context)
        context.paint()
        spa.render(context, i)
        imageSurface.write_to_png(os.path.join(save_img_dir, "frame-" + left_align_videoformat(i) + ".png"))

    print "Startup complete."
    print "Rendering tracking images to", save_img_dir
    
    start_time = time()
    
    render(0, v[0])
    for i, frame in enumerate(v[1:], 1):
        particles, intermediate_particles = pf(particles, frame.get_array(), goodness, sampling_function=sample)
        render(i, frame)
        
        print "Processed frame %i"%(i)
        
    print "Finished in %f seconds." % (time()-start_time)

cProfile.run("run(7)")
