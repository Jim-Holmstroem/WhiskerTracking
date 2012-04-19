from pf import pf
from time import time
from wdb import StateTransitionDatabase
from wmedia import wvideo, left_align_videoformat
from wmedia.square_particles_animator import square_particles_animator
from scipy.ndimage import filters
import wtracker
import cProfile
import cairo
import numpy
import os

def goodness(particle, image):
    x, y = (particle[0], particle[2])
    
    if x < 0 or y < 0 or y >= image.shape[0] or x >= image.shape[1]:
        return 0
    
    return image[y,x]**3

class BounceTracker(wtracker.Tracker):
    def __init__(self, db):
        self.db = db
    
    def sample(self, prev_particle):
        
        new_particle_from_prev = prev_particle.copy()
        new_particle_from_prev[0] += prev_particle[1]*0.5
        new_particle_from_prev[2] += prev_particle[3]*0.5
        new_particle_from_prev = new_particle_from_prev + numpy.random.normal(loc=0, scale=5, size=prev_particle.shape)
        
        prev_particle_copy = prev_particle.copy()
        prev_particle_copy[0] = 0
        prev_particle_copy[2] = 0
        new_particle_from_db = self.db.sample_weighted_average(prev_particle_copy)
        new_particle_from_db[0] += prev_particle[0]
        new_particle_from_db[2] += prev_particle[2]
    #    new_particle_from_db += numpy.random.normal(0, scale=[3, 3], size=new_particle_from_db.shape)
        
        db_weight = 2
        prev_weight = 1
        
        new_particle = new_particle_from_prev*prev_weight + (new_particle_from_db)*db_weight
        new_particle /= db_weight + prev_weight
        return new_particle
    
    def run(self, video, start_state, num_particles, square_side=50):
        print("Starting up...")
        
        print("Blurring video...")
        video_blur = video.transform(lambda img: filters.gaussian_filter(img, 20))
        print("Video blurred.")
        
        num_frames = len(video)
        
        particles = numpy.array([start_state]*num_particles)
        
        print "Startup complete."
        
        print "Tracking..."
        
        track = numpy.zeros((num_frames, start_state.size))
        track[0,:] = start_state
        
        for i, frame in enumerate(video_blur[1:], 1):
            particles, intermediate_particles = pf(particles, frame.get_array(), goodness, sampling_function=self.sample)
            track[i,:] = particles.mean(axis=0)
            print "Tracked frame %i of %i"%(i+1, num_frames)
        
        print "Tracking complete."
            
        return track

def cProfile_test(movie_id):
    dataset = "square_accelerating"
    movie = dataset + "_" + str(movie_id)
    save_img_dir = os.path.join("run", "square_tracker_bounce-%i.pngvin"%(movie_id))
    if(not os.path.exists(save_img_dir)):
        os.makedirs(save_img_dir)
    video = wvideo(os.path.join("video", movie+".pngvin")) # Dimensions: x, y, rgba
    db = StateTransitionDatabase(dataset)
    
    correct_states = numpy.load(os.path.join("video", movie+".pngvin", "state_sequence.npy"))
    
    BounceTracker(db).run(video, correct_states[0,:], 100, 50)

if __name__ == "__main__":
#    cProfile.run("run(7)")
#    cProfile.run("run(8)")
#    cProfile.run("run(9)")
    cProfile.run("cProfile_test(0)")
    