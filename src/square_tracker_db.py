import numpy
import os
from PIL import ImageDraw
from pf import pf
from wmedia import video, left_align_videoformat
from wdb import StateTransitionDatabase

def goodness(particle, image):
    x, y = particle
    
    if x < 0 or y < 0 or x >= image.shape[0] or y >= image.shape[1]:
        return 0
    
    if(image[x,y,0] == 255 and image[x,y,1] == 255 and image[x,y,2] == 255):
        return 0.9
    else:
        return 0.1

def sample(prev_particle):
    
    new_particle_from_prev = prev_particle + numpy.random.normal(loc=0, scale=10, size=prev_particle.shape)
    new_particle_from_db = db.sample_weighted_average(prev_particle)
#    new_particle_from_db += numpy.random.normal(0, scale=[3, 3], size=new_particle_from_db.shape)
    
    db_weight = 10
    prev_weight = 1
    
    new_particle = new_particle_from_prev*prev_weight + new_particle_from_db*db_weight
    new_particle /= db_weight + prev_weight
    return new_particle

dataset = "square_simple"
db = StateTransitionDatabase(dataset)
save_img_dir = "run/square_tracker_db-"+dataset+".pngvin"
if(not os.path.exists(save_img_dir)):
    os.makedirs(save_img_dir)

print("Rendering tracking images to " + save_img_dir)
    
v = video("data/"+dataset+".pngvin") # Dimensions: x, y, rgba

num_particles = 100
#particles = numpy.random.uniform(0, max(v[0].get_copy_of_current_image().size)-1, (num_particles, 2))
#particles = numpy.random.normal(size=(num_particles, 2), scale=10) + numpy.array([51, 51])
#start_state = numpy.array([102, 102, 0])
start_state = numpy.array([102, 102])
particles = numpy.array([start_state]*num_particles)
#particles = numpy.random.normal(start_state, scale=[3, 3, pi/18], size=[num_particles, start_state.size])

for (i, frame) in enumerate(v):

    img = frame.get_copy_of_current_image()
    draw = ImageDraw.Draw(img)
    for row in particles:
        draw.point(row[:2].tolist(), fill="#FF0000")
    
    pos = particles.mean(axis=0)[:2]
    draw.point(pos.tolist(), fill="#0000FF")
    img.save(save_img_dir + "/frame-" + left_align_videoformat(i) + ".png", "PNG")
    print("Successfully rendered frame " + str(i))
    
    particles = pf(particles, frame.get_array(), goodness, sampling_function=sample)
    