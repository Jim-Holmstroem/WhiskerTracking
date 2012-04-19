from pf import pf
from time import time
from wdb import StateTransitionDatabase
from wmedia import wvideo as video, left_align_videoformat
from wmedia.square_particles_animator import square_particles_animator
from scipy.ndimage import filters
import cProfile
import cairo
import numpy
import os

def goodness(particle, image):
    x, y = (particle[0], particle[2])
    
    if x < 0 or y < 0 or y >= image.shape[0] or x >= image.shape[1]:
        return 0
    
    return image[y,x]**3

def sample(prev_particle):
    
    new_particle_from_prev = prev_particle.copy()
    new_particle_from_prev[0] += prev_particle[1]*0.5
    new_particle_from_prev[2] += prev_particle[3]*0.5
    new_particle_from_prev = new_particle_from_prev + numpy.random.normal(loc=0, scale=5, size=prev_particle.shape)
    
    prev_particle_copy = prev_particle.copy()
    prev_particle_copy[0] = 0
    prev_particle_copy[2] = 0
    new_particle_from_db = db.sample_weighted_average(prev_particle_copy)
    new_particle_from_db[0] += prev_particle[0]
    new_particle_from_db[2] += prev_particle[2]
#    new_particle_from_db += numpy.random.normal(0, scale=[3, 3], size=new_particle_from_db.shape)
    
    db_weight = 2
    prev_weight = 1
    
    new_particle = new_particle_from_prev*prev_weight + (new_particle_from_db)*db_weight
    new_particle /= db_weight + prev_weight
    return new_particle

IMAGE_WIDTH = 512.
IMAGE_HEIGHT = 512.

dataset = "square_bounce"
db = StateTransitionDatabase(dataset)
num_particles = 1000
MAX_FRAMES = 20

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
    num_frames = min(MAX_FRAMES, len(v))
    v = video(v[:num_frames])
    print("Blurring video...")
    v_blur = v.transform(lambda img: filters.gaussian_filter(img, 20))
    print("Video blurred.")
#    v_blur = v
    
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
    print "Rendered frame %i of %i"%(1, num_frames)
    for i, frame in enumerate(v_blur[1:], 2):
        particles, intermediate_particles = pf(particles, frame.get_array(), goodness, sampling_function=sample)
        render(i, v[i])
        
        print "Rendered frame %i of %i"%(i, num_frames)
    
    print "Finished in %f seconds." % (time()-start_time)

cProfile.run("run(7)")
cProfile.run("run(8)")
cProfile.run("run(9)")
