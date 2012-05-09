from itertools import izip
from scipy.ndimage import filters
from wmedia import wimage
from wtracker.tracker import Tracker
from wview import SquareAnimator
from wview.square import SquareLayer
import numpy
import wtracker

class SquareTracker(wtracker.Tracker):
    
    def __init__(self, *args):
        wtracker.Tracker.__init__(self, *args)
        print("Starting up...")
        
        print("Blurring video...")
        self.blurred_video = self.video.transform(lambda img: filters.gaussian_filter(img, 20))
        print("Video blurred.")

        self.original_video = self.video
        self.video = self.blurred_video
        
        print "Startup complete."
        
    def make_animators(self):
        return [SquareAnimator(mp[:,::2], post[:,:,::2], pre[:,:,::2]) for mp, post, pre in izip(self.tracks, self.resampled_particles, self.preresampled_particles)]
        
    def goodness(self, arg):#particle, image):
        particle, image = arg
        x, y = (particle[0], particle[2])
        
        if x < 0 or y < 0 or y >= image.shape[0] or x >= image.shape[1]:
            return numpy.array([0])
        
        return image[y,x]**3
    
    def sample(self, prev_particle):
        
        # new_particle_from_prev = prev_particle.copy()
        # new_particle_from_prev[0] += prev_particle[1]
        # new_particle_from_prev[2] += prev_particle[3]
        # new_particle_from_prev = new_particle_from_prev + numpy.random.normal(loc=0, scale=5, size=prev_particle.shape)
        
        prev_particle_copy = prev_particle.copy()
        prev_particle_copy[0] = 0
        prev_particle_copy[2] = 0
        new_particle_from_db = numpy.random.normal(self.db.sample_weighted_average(prev_particle_copy), 16)
        new_particle_from_db[0] += prev_particle[0]
        new_particle_from_db[2] += prev_particle[2]
    #    new_particle_from_db += numpy.random.normal(0, scale=[3, 3], size=new_particle_from_db.shape)
        
#        db_weight = 1
#        prev_weight = 1
        
#        new_particle = new_particle_from_prev*prev_weight + (new_particle_from_db)*db_weight
#        new_particle /= db_weight + prev_weight
#        return new_particle
        return new_particle_from_db
    
    def export_results(self, *args):
        self.video = self.original_video
        Tracker.export_results(self, *args)
        self.video = self.blurred_video

class SquareTrackerBetterGoodness(SquareTracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
    def export_results(self, *args):
        Tracker.export_results(self, *args)
    
    def goodness(self, arg):#particle, image):
        particle, image = arg
        mask = wimage(SquareLayer(particle[::2]))
        processed_image = wimage(image)
        
        mask_sum = mask.sum()
        if mask_sum == 0:
            return 0
        return (mask*processed_image).sum()/(255*mask_sum)

class SquareWithoutVelocityTracker(SquareTrackerBetterGoodness):

    def make_animators(self):
        return map(SquareAnimator, self.tracks, self.resampled_particles, self.preresampled_particles)

    def goodness(self, arg):#particle, image):
        particle, image = arg
        mask = wimage(SquareLayer(particle))
        processed_image = wimage(image)
        
        mask_sum = mask.sum()
        if mask_sum == 0:
            return 0
        return (mask*processed_image).sum()/(255*mask_sum)

    def sample(self, prev_particle):
        return numpy.random.normal(self.db.sample_weighted_average(prev_particle), 15)
