import numpy
from PIL import ImageDraw
from pf import pf
from wmedia import video
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

def sample(particles):
#    return numpy.random.normal(scale=10, size=particles.size) + particles.mean(axis=0)
    return particles + numpy.random.normal(loc=5, scale=2, size=particles.size)

v = video("data/square_simple.pngvin") # Dimensions: x, y, rgba

num_particles = 1000

#particles = numpy.random.uniform(0, max(v[0].get_copy_of_current_image().size)-1, (num_particles, 2))
particles = numpy.random.normal(size=(num_particles, 2), scale=10) + numpy.array([51, 51])

for frame in v:
#    frame.get_copy_of_current_image().show()
#    raw_input()
#    continue

    img = frame.get_copy_of_current_image()
    draw = ImageDraw.Draw(img)
    for row in particles:
        draw.point(row.tolist(), fill="#FF0000")
    
    particles = pf(particles, frame.get_array(), goodness, sampling_function=sample)
    
    pos = particles.mean(axis=0)
    draw.point(pos.tolist(), fill="#FF0000")
    img.show()
    sleep(0.2)
