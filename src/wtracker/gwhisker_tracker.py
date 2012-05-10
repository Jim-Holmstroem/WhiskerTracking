import numpy
import wtracker

from wmedia import wimage
from wgenerator import GWhiskerGenerator
from wview import GWhiskerAnimator, GWhiskerLayer

class GWhiskerTracker(wtracker.SquareTrackerBetterGoodness):

    STDEVS = [max(a)/5.0 for a in (GWhiskerGenerator.A_LIMITS, GWhiskerGenerator.B_LIMITS, GWhiskerGenerator.C_LIMITS)]

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
        return self.db.sample_weighted_average(prev_particle) + numpy.array(map(numpy.random.normal, numpy.zeros_like(self.STDEVS), self.STDEVS))
