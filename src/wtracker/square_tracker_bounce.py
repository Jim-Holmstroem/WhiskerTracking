from scipy.ndimage import filters
from wmedia import wimage
from wtracker.tracker import Tracker
from wview import SquareAnimator
from wview.square import SquareLayer
import numpy
import wtracker

class SquareTracker(wtracker.Tracker):
    
    def __init__(self, db, video):
        wtracker.Tracker.__init__(self, db, video)
        print("Starting up...")
        
        print("Blurring video...")
        self.blurred_video = self.video.transform(lambda img: filters.gaussian_filter(img, 20))
        print("Video blurred.")

        self.video = self.blurred_video        
        self.original_video = self.video
        
        print "Startup complete."
        
    def make_animator(self, main_particles, particles, intermediate_particles):
        return SquareAnimator(main_particles, particles, intermediate_particles)
        
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
    
    def export_results(self, *args):
        self.video = self.original_video
        Tracker.export_results(self, *args)
        self.video = self.blurred_video
