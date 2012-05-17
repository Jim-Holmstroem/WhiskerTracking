DEBUG = False
if DEBUG:
    import cairo
import numpy
import wmath

from itertools import repeat
from wmedia import wimage
from wgenerator import GWhiskerGenerator
from wtracker import Tracker
from wview import GWhiskerAnimator, GWhiskerLayer

from scipy.ndimage import filters

class GWhiskerTracker(Tracker):

    debug_i = 0
    STDEVS = [max(a)/10.0 for a in (GWhiskerGenerator.A_LIMITS, GWhiskerGenerator.B_LIMITS, GWhiskerGenerator.C_LIMITS)]
    
    def __init__(self, db, video, start_states, *other_args, **kwargs):
        Tracker.__init__(self, db, video, start_states, *other_args, **kwargs)
        self.lp_space = int(kwargs['LP'])
        self.weight_power = float(kwargs['WEIGHT_POWER'])

        try:
            self.metadata = kwargs["metadata"]
        except KeyError:
            raise ArgumentError("Fatal: Metadata is missing.")

    def track_object(self, obj_i, *other_args, **kwargs):
        self.renderer_dl = self.metadata[obj_i]["dl"]
        self.renderer_length = self.metadata[obj_i]["length"]
        self.renderer_width = self.metadata[obj_i]["width"]
        self.current_translation = self.metadata[obj_i]["translate"]
        Tracker.track_object(self, obj_i, *other_args, **kwargs)

    def make_animators(self, track=True, resampled_particles=True, preresampled_particles=True, highest_weight_particles=True):
        def return_None_if_false(b, r):
            if b == True:
                return r
            return None

        self.animators = map(lambda t,r,p,trans,hi: GWhiskerAnimator(
                return_None_if_false(track, t),
                return_None_if_false(resampled_particles, r),
                return_None_if_false(preresampled_particles, p),
                highest_weight_particles=return_None_if_false(highest_weight_particles, hi),
                translate=trans),
                self.tracks, self.resampled_particles, self.preresampled_particles, (d["translate"] for d in self.metadata), self.highest_weight_particles)
        return self.animators

    def preprocess_image(self, image):
        return image.transform(lambda img: filters.gaussian_filter(img,3.0))

    def goodness(self, arg):#particle, image):
        particle, image = arg
        mask = wimage(GWhiskerLayer(particle, self.renderer_dl, self.renderer_length, self.renderer_width, translate=self.current_translation))
        mask_sum = mask.sum()
        if mask_sum == 0:
            return 0

        result =  ((mask*image).sum()/(255*mask_sum))**4
        
        if DEBUG:
            from common import make_run_path
            import os
            wim = wimage((mask*image).data/255)
            
            imsurf=cairo.ImageSurface(cairo.FORMAT_ARGB32, 512*3,512)
            ctx = cairo.Context(imsurf)
            for im in (image, mask, wim):
                ctx.save()
                im.render(ctx)
                ctx.restore()
                ctx.translate(512,0)
            imsurf.write_to_png(make_run_path(os.path.join("debug","%s%i.png"%("frame", self.debug_i))))
            self.debug_i += 1

            print "sum, result:", mask_sum, result
        
        return result

    def weight_function(self, prev_particle, from_states):
        return (1.0/(wmath.spline_lp_distances(prev_particle, from_states, self.renderer_length, self.lp_space)))**self.weight_power
    
    def sample(self, prev_particle):
        return self.db.sample_weighted_average(prev_particle, self.weight_function) + numpy.array(map(numpy.random.normal, numpy.zeros_like(self.STDEVS), self.STDEVS))

