import numpy
import os
from PIL import ImageDraw
from pf import pf
from wmedia import video, left_align_videoformat
from itertools import product
from time import sleep

def goodness(particle, image):
    x, y = particle
    
    if x < 0 or y < 0 or x >= image.shape[0] or y >= image.shape[1]:
        return 0
    
    if(image[x,y,0] == 255 and image[x,y,1] == 255 and image[x,y,2] == 255):
        return 0.9
    else:
        return 0.1

def sample(prev_particle):
    return prev_particle + numpy.random.normal(loc=5, scale=2, size=prev_particle.size)

dataset = "square_simple"
save_img_dir = "run/square_tracker-"+dataset+".pngvin"
if(not os.path.exists(save_img_dir)):
    os.makedirs(save_img_dir)

print("Rendering tracking images to " + save_img_dir)
    
v = video("data/"+dataset+".pngvin") # Dimensions: x, y, rgba

num_particles = 1000
#particles = numpy.random.uniform(0, max(v[0].get_copy_of_current_image().size)-1, (num_particles, 2))
particles = numpy.random.normal(size=(num_particles, 2), scale=10) + numpy.array([51, 51])

for (i, frame) in enumerate(v):

    img = frame.get_copy_of_current_image()
    draw = ImageDraw.Draw(img)
    for row in particles:
        draw.point(row.tolist(), fill="#FF0000")
    
    particles = pf(particles, frame.get_array(), goodness, sampling_function=sample)
    
    pos = particles.mean(axis=0)
    draw.point(pos.tolist(), fill="#FF0000")
    img.save(save_img_dir + "/frame-" + left_align_videoformat(i) + ".png", "PNG")
    print("Successfully rendered frame " + str(i))
    sleep(0.2)
