import numpy
import wtracker

from wmedia import wimage
from wview import GWhiskerAnimator, GWhiskerLayer

class GWhiskerTracker(wtracker.SquareTrackerBetterGoodness):

    def make_animators(self):

        mid = numpy.array((256, 256))
        translate = numpy.vstack((numpy.zeros(self.num_objects), numpy.linspace(-100, 100, self.num_objects))).T

        return map(lambda t,r,p,trans: GWhiskerAnimator(t, r, p, translate=trans), self.tracks, self.resampled_particles, self.preresampled_particles, mid+translate)

    def goodness(self, arg):#particle, image):
        particle, image = arg
        mask = wimage(GWhiskerLayer(particle))
        processed_image = wimage(image)
        
        mask_sum = mask.sum()
        if mask_sum == 0:
            return 0
        return (mask*processed_image).sum()/(255*mask_sum)
    
    def sample(self, prev_particle):
        return numpy.random.normal(self.db.sample_weighted_average(prev_particle), 0.1)
