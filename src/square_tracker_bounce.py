from pf import pf
from time import time
from wdb import StateTransitionDatabase
from wmedia import wvideo as video, left_align_videoformat
import cProfile
import cairo
import numpy
import os

def goodness(particle, image):
    x, y = (particle[0], particle[2])
    
    if x < 0 or y < 0 or y >= image.shape[0] or x >= image.shape[1]:
        return 0
    
    if not False in (image[y,x,:3] == 255):
        return 1000
    else:
        return 1

def sample(prev_particle):
    
    next_pos = prev_particle + numpy.array((prev_particle[1], prev_particle[3], 9.81, 9.81))
    new_particle_from_prev = next_pos + numpy.random.normal(loc=0, scale=10, size=prev_particle.shape)
    new_particle_from_db = db.sample_weighted_average(numpy.array((0, prev_particle[1], 0, prev_particle[3])))
#    new_particle_from_db += numpy.random.normal(0, scale=[3, 3], size=new_particle_from_db.shape)
    
    db_weight = 1
    prev_weight = 1
    
    new_particle = new_particle_from_prev*prev_weight + (prev_particle+new_particle_from_db)*db_weight
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
    
    print("Rendering tracking images to " + save_img_dir)
    
    v = video(os.path.join("video", movie+".pngvin")) # Dimensions: x, y, rgba
    #particles = numpy.random.uniform(0, max(v[0].get_copy_of_current_image().size)-1, (num_particles, 2))
    #particles = numpy.random.normal(size=(num_particles, 2), scale=10) + numpy.array([51, 51])
    #start_state = numpy.array([102, 102, 0])
    
    start_states = {
            7:numpy.array([X_LIMITS[0], 25., Y_LIMITS[0], 0.]),
            8:numpy.array([IMAGE_WIDTH/2., -5, IMAGE_HEIGHT*3./4, 3]),
            9:numpy.array([IMAGE_WIDTH/5., 10, IMAGE_HEIGHT/3., 2])}
    #for state in start_states.values():
    #    state[:2] += square_side/2
    
    particles = numpy.array([start_states[movie_id]]*num_particles)
    #particles = numpy.random.normal(start_state, scale=[3, 3, pi/18], size=[num_particles, start_state.size])
    
    start_time = time()
    
    for (i, frame) in enumerate(v):
    
        imageSurface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(IMAGE_WIDTH), int(IMAGE_HEIGHT))
        context = cairo.Context(imageSurface)
        frame.render(context)
        context.paint()
        
        context.set_source_rgb(255, 0, 0)
        for row in particles:
            context.rectangle(row[0], row[2], 1, 1)
#            print row[0], row[2]
            context.fill()
        
        pos = particles[:,0:3:2].mean(axis=0)
        
#        draw.rectangle(((pos-half_square_side).tolist(), (pos+half_square_side).tolist()), outline=0x00FF00)
        context.set_source_rgb(0, 255, 0)
        context.rectangle(pos[0], pos[1], 1, 1)
        context.fill()
        imageSurface.write_to_png(os.path.join(save_img_dir, "frame-" + left_align_videoformat(i) + ".png"))
#        img.save(os.path.join(save_img_dir, "frame-" + left_align_videoformat(i) + ".png"), "PNG")
        print "Successfully rendered frame %i"%(i)
        
        particles = pf(particles, frame.get_array(), goodness, sampling_function=sample)
        
    print "Finished in %f seconds." % (time()-start_time)

cProfile.run("run(7)")
