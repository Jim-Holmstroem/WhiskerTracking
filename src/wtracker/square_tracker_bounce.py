from pf import pf
from scipy.ndimage import filters
from wdb import StateTransitionDatabase
from wmedia import wvideo
from wmedia.square_particles_animator import square_particles_animator
import cProfile
import numpy
import os
import wtracker

from common import make_video_path, make_run_path

class BounceTracker(wtracker.Tracker):
    
    def __init__(self, db, video):
        wtracker.Tracker.__init__(self, db, video)
        print("Starting up...")
        
        print("Blurring video...")
        self.video = self.video.transform(lambda img: filters.gaussian_filter(img, 20))
        print("Video blurred.")
        
        print "Startup complete."
        
    def make_animator(self, main_particles, particles, intermediate_particles):
        return square_particles_animator(main_particles, particles, intermediate_particles)
        
    def goodness(self, particle, image):
        x, y = (particle[0], particle[2])
        
        if x < 0 or y < 0 or y >= image.shape[0] or x >= image.shape[1]:
            return 0
        
        return image[y,x]**3
    
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
    
def cProfile_test(movie_id):
    dataset = "square_accelerating"
    movie = dataset + "_" + str(movie_id)
    save_img_dir = make_run_path("square_tracker_bounce-%i.pngvin"%(movie_id))
    if(not os.path.exists(save_img_dir)):
        os.makedirs(save_img_dir)
    video = wvideo(make_video_path(movie+".pngvin")) # Dimensions: x, y, rgba
    db = StateTransitionDatabase(dataset)
    
    correct_states = numpy.load(make_video_path(movie+".pngvin", "state_sequence.npy"))
    
    BounceTracker(db, video).run(correct_states[0,:], 100)

if __name__ == "__main__":
#    cProfile.run("run(7)")
#    cProfile.run("run(8)")
#    cProfile.run("run(9)")
    cProfile.run("cProfile_test(0)")
    