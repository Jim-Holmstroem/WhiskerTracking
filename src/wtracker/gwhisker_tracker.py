DEBUG = False
if DEBUG:
    import cairo
import numpy
import os
import wmath

from common.settings import IMAGE_WIDTH, IMAGE_HEIGHT

from common import make_path
from itertools import izip, repeat
from wmedia import wimage
from wgenerator import GWhiskerGenerator
from wtracker import Tracker
from wview import GWhiskerAnimator, GWhiskerLayer

from scipy.ndimage import filters

class GWhiskerTracker(Tracker):

    debug_i = 0
    STDEVS = numpy.array([max(a)/10.0 for a in (GWhiskerGenerator.A_LIMITS, GWhiskerGenerator.B_LIMITS, GWhiskerGenerator.C_LIMITS)])
    
    def __init__(self, db, video, start_states, *other_args, **kwargs):
        Tracker.__init__(self, db, video, start_states, *other_args, **kwargs)
        self.lp_space = int(kwargs['LP'])
        self.weight_power = int(kwargs['WEIGHT_POWER'])
        self.goodness_power = int(kwargs['GOODNESS_POWER'])
        self.sample_std_modifier = float(kwargs['SAMPLE_STD_MODIFIER'])

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
        mask = wimage(GWhiskerLayer(particle, self.renderer_dl, self.renderer_length, self.renderer_width, translate=self.current_translation), width=IMAGE_WIDTH, height=IMAGE_HEIGHT)
        mask_sum = mask.sum()
        if mask_sum == 0:
            return 0

        result = ((mask*image).sum()/(255.0*mask_sum))**self.goodness_power
        
        if DEBUG:
            from common import make_run_path
            import os
            wim = wimage((mask*image).data/255.0)
            
            imsurf=cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_WIDTH*3,IMAGE_HEIGHT)
            ctx = cairo.Context(imsurf)
            for im in (image, mask, wim):
                ctx.save()
                im.render(ctx)
                ctx.restore()
                ctx.translate(IMAGE_WIDTH,0)
            imsurf.write_to_png(make_run_path(os.path.join("debug","%s%i.png"%("frame", self.debug_i))))
            self.debug_i += 1

            print "sum, result:", mask_sum, result
        
        return result

    def weight_function(self, prev_particle, from_states):
        return (1.0/(wmath.spline_lp_distances(prev_particle, from_states, self.renderer_length, self.lp_space)))**self.weight_power
    
    def sample(self, prev_particle):
        return self.db.sample_weighted_average(prev_particle, self.weight_function) + numpy.array(map(numpy.random.normal, numpy.zeros_like(self.STDEVS), self.STDEVS*self.sample_std_modifier))

    def calculate_error(self, correct_states, error_norms=(2, 4, 8)):
        """Generate error matrices.

        First dimension: Index of the tracked object
        Second dimension: P in the L^P norm: 2, 4, 8
        Third dimension: Time step
        """
        self.absolute_error = []
        self.relative_error = []
        for track, correct in izip(self.tracks, correct_states):
            distances = []
            relative_errors = []
            for P in error_norms:
                distances_P = numpy.array(wmath.spline_lp_distances(track, correct, self.renderer_length, P))
                correct_norms_P = numpy.array(wmath.spline_lp_norms(correct, self.renderer_length, P))
                relative_errors_P = distances_P / correct_norms_P
                distances.append(distances_P)
                relative_errors.append(relative_errors_P)

            self.absolute_error.append(numpy.array(distances))
            self.relative_error.append(numpy.array(relative_errors)) 
       
        self.absolute_error = numpy.array(self.absolute_error)
        self.relative_error = numpy.array(self.relative_error)

    def make_results_name(self):
        return "%s_n=%i_p=%i_a=%i_g=%i_s=%s"%(self.__class__.__name__, self.num_particles, self.lp_space, self.weight_power, self.goodness_power, self.STDEVS*self.sample_std_modifier)

    def make_results_dir(self):
        results_dir = make_path("results", self.make_results_name())
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        return results_dir

    def save_error(self):
        for error_type, error in (("absolute", self.absolute_error,), ("relative", self.relative_error)): 
            save_file = os.path.join(self.make_results_dir(), error_type + "_error.npy")
            numpy.save(save_file, error)

    def export_results(self, pngvin_dir):
        for name, draw_all in zip(("only_track", "all_particles"), (False, True)):
            self.make_animators(track=True, resampled_particles=draw_all, preresampled_particles=draw_all, highest_weight_particles=draw_all)
            pngvin_dir = os.path.join(self.make_results_dir(), name + ".pngvin")
            Tracker.export_results(self, pngvin_dir)
