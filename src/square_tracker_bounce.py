import numpy
import os
from PIL import ImageDraw
from pf import pf
from wmedia import video, left_align_videoformat
from wdb import StateTransitionDatabase
from time import time

def goodness(particle, image):
    x, y = particle[0:2]
    
    if x < 0 or y < 0 or x >= image.shape[0] or y >= image.shape[1]:
        return 0
    
    # FIXME: Image is always black!
    if(image[x,y,0] == 255 and image[x,y,1] == 255 and image[x,y,2] == 255):
        print "White", image[x,y,:]
        return 10000
    else:
        print "Not white", image[x,y,:]
        return 1

def sample(prev_particle):
    
    new_particle_from_prev = prev_particle + numpy.random.normal(loc=0, scale=5, size=prev_particle.shape)
    new_particle_from_db = db.sample_weighted_average(prev_particle)
#    new_particle_from_db += numpy.random.normal(0, scale=[3, 3], size=new_particle_from_db.shape)
    
    db_weight = 5
    prev_weight = 1
    
    new_particle = new_particle_from_prev*prev_weight + new_particle_from_db*db_weight
    new_particle /= db_weight + prev_weight
    return new_particle

dataset = "square_bounce"
square_side = 50
movie_id = 8
movie = dataset + "_" + str(movie_id)
db = StateTransitionDatabase(dataset)
save_img_dir = "run/square_tracker_bounce-" + movie + ".pngvin"
if(not os.path.exists(save_img_dir)):
    os.makedirs(save_img_dir)

print("Rendering tracking images to " + save_img_dir)

v = video("data/"+movie+".pngvin") # Dimensions: x, y, rgba

num_particles = 100
#particles = numpy.random.uniform(0, max(v[0].get_copy_of_current_image().size)-1, (num_particles, 2))
#particles = numpy.random.normal(size=(num_particles, 2), scale=10) + numpy.array([51, 51])
#start_state = numpy.array([102, 102, 0])

start_states = {7:numpy.array([0+square_side/2, 0+square_side/2, 50., 0.]),
                8:numpy.array([512/2+square_side/2, 512*3/4+square_side/2, -30., 85.]),
                9:numpy.array([512/5+square_side/2, 512/3+square_side/2, 5., 17.])}
#for state in start_states.values():
#    state[:2] += square_side/2
        
particles = numpy.array([start_states[movie_id]]*num_particles)
#particles = numpy.random.normal(start_state, scale=[3, 3, pi/18], size=[num_particles, start_state.size])

start_time = time()

for (i, frame) in enumerate(v):

    img = frame.get_copy_of_current_image()
    draw = ImageDraw.Draw(img)
    for row in particles:
        draw.point(row[:2].tolist(), fill="#FF0000")
    
    pos = particles.mean(axis=0)[:2]
    draw.point(pos.tolist(), fill="#00FF00")
    img.save(save_img_dir + "/frame-" + left_align_videoformat(i) + ".png", "PNG")
    print("Successfully rendered frame " + str(i))
    
    particles = pf(particles, frame.get_array(), goodness, sampling_function=sample)
    
print "Finished in %f seconds." % (time()-start_time)
