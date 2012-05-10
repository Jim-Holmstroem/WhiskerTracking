DEBUG = False
if DEBUG:
    import cairo
import numpy
import wtracker

from wmedia import wimage
from wgenerator import GWhiskerGenerator
from wview import GWhiskerAnimator, GWhiskerLayer

from scipy.ndimage import filters

class GWhiskerTracker(wtracker.SquareTrackerBetterGoodness):

    debug_i = 0
    STDEVS = [max(a)/5.0 for a in (GWhiskerGenerator.A_LIMITS, GWhiskerGenerator.B_LIMITS, GWhiskerGenerator.C_LIMITS)]

    def make_animators(self):

        mid = numpy.array((256, 256))
        translate_height = GWhiskerGenerator.DISTANCE_BETWEEN_WHISKERS*float(self.num_objects-1)
        translate = mid + numpy.vstack((-GWhiskerGenerator.WHISKER_LENGTH/2 * numpy.ones(self.num_objects), numpy.linspace(-translate_height/2, translate_height/2, self.num_objects))).T

        return map(lambda t,r,p,trans: GWhiskerAnimator(t, r, p, translate=trans), self.tracks, self.resampled_particles, self.preresampled_particles, translate)

    def preprocess_image(self, image):
        return image.transform(lambda img: filters.gaussian_filter(img,3.0))

    def goodness(self, arg):#particle, image):
        particle, image = arg
        mask = wimage(GWhiskerLayer(particle, 5, 150, 5, translate=(256-75, 256))) # TODO: Un-hardcode this
        mask_sum = mask.sum()
        if mask_sum == 0:
            return 0

        result =  ((mask*image).sum()/(255*mask_sum))**2
        
        if DEBUG:
            wim = wimage((mask*image).data/255)
            
            imsurf=cairo.ImageSurface(cairo.FORMAT_ARGB32, 512*3,512)
            ctx = cairo.Context(imsurf)
            for im in (image, mask, wim):
                ctx.save()
                im.render(ctx)
                ctx.restore()
                ctx.translate(512,0)
            imsurf.write_to_png("/misc/projects/whisker/run/debug/%s%i.png"%("frame", self.debug_i))
            self.debug_i += 1

            print "sum, result:", mask_sum, result
        
        return result
    
    def sample(self, prev_particle):
        return self.db.sample_weighted_average(prev_particle) + numpy.array(map(numpy.random.normal, numpy.zeros_like(self.STDEVS), self.STDEVS))
