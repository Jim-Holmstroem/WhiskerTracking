from common import make_video_path
from common.settings import make_run_path
from itertools import repeat
from wdb import StateTransitionDatabase
from wgui.wlayermanager import wlayermanager
from wgui.wwindow import wwindow
from wmedia import wvideo
import gtk
import numpy
import os
import pickle
import wtracker

class TrackerRunner:
    
    def __init__(self, tracker_classes, video_name, database_name, num_particles=100, **cli_kwargs):
        video_path = make_video_path(video_name + ".pngvin")
        
        self.video_name = video_name
        self.database_name = database_name
        
        self.num_objects = 0
        while os.path.exists(os.path.join(video_path, "state_sequence_%i.npy"%(self.num_objects))):
            self.num_objects += 1

        self.correct_states = [numpy.load((os.path.join(video_path, "state_sequence_%i.npy"%i))) for i in xrange(self.num_objects)]

        metadata = [os.path.exists(os.path.join(video_path, "metadata_%i.pickle"%i)) and pickle.load(open(os.path.join(video_path, "metadata_%i.pickle"%i))) or {} for i in xrange(self.num_objects)]

        self.video = wvideo(video_path)
        self.db = StateTransitionDatabase(database_name)

        self.trackers = map(lambda tracker_class:tracker_class(self.db, self.video, [self.correct_states[i][0] for i in xrange(self.num_objects)], num_particles, metadata=metadata, **cli_kwargs), tracker_classes)

    def _run_test(self, tracker):
        print "Tracking with tracker class %s"%(tracker.__class__.__name__)
        tracker.run()
        return (tracker.get_track(i) for i in xrange(self.num_objects))

    def run_benchmark(self):
        print "Running tracking benchmark"
        print
        import cProfile
        cProfile.runctx("self.run()", globals(), locals())
        print "Finished tracking benchmark"
        print
        self.evaluate_results()
    
    def run(self):
        print "Running trackers"
        print
        self.tracks = map(self._run_test, self.trackers)
        print "Finished tracking"
        print

    def evaluate_results(self):
        print "##################################################"
        print "#                  TEST RESULTS                  #"
        print "##################################################"
        print

        # Rows: trackers, Cols: objects
        errors = numpy.array([t.calculate_error(self.correct_states) for t in self.trackers])
        
        for tracker_i, err in enumerate(errors):
            print "Errors for tracker %s:"%(self.trackers[tracker_i].__class__.__name__)
            for obj_i, e in enumerate(err):
                print "Object %i: %f"%(obj_i+1, e)
            print

        wins = numpy.zeros(len(self.trackers))

        for obj_i in xrange(self.num_objects):
            winner = errors[:,obj_i].argmin()
            wins[winner] += 1
            print "Winner for object %i: %s with error %f"%(obj_i+1, self.trackers[winner].__class__.__name__, errors[winner][obj_i])
        print

        winners = numpy.where(wins == wins.max())
        print "The following trackers had the most wins (%i):"%(wins.max())
        for tracker_i in winners:
            print self.trackers[tracker_i].__class__.__name__
        
        print "##################################################"
        print "#               END OF TEST RESULTS              #"
        print "##################################################"
        print
    
    def animate(self, tracker_i):
        print "Animating test results"
        layer_manager = wlayermanager()
        layer_manager.add_layer(self.video)
        map(layer_manager.add_layer, (self.trackers[tracker_i].get_animator(i) for i in xrange(self.num_objects)))
        
        win = wwindow(layer_manager)
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()
        print "Done animating test results"
        print
    
    def export_results(self, name=None):
        if name == None:
            name = self.video_name
        for name_suffix, draw_all in zip(("_only_track", "_all_particles"), (False, True)):
            for tracker in self.trackers:
                tracker.make_animators(track=True, resampled_particles=draw_all, preresampled_particles=draw_all, highest_weight_particles=draw_all)
                pngvin_dir = make_run_path(name + name_suffix + "_" + tracker.__class__.__name__ + ".pngvin")
                print "Saving results of tracker %s to %s"%(tracker.__class__.__name__, pngvin_dir)
                tracker.export_results(pngvin_dir)

def run_cli():
    """Usage: python track.py VIDEO_NAME DB_NAME [-o OUTPUT_NAME] [-n NUM_PARTICLES] [-b (True|False)] [-p LP] [-P ERROR_LP] [-a WEIGHT_POWER] [-g GOODNESS_POWER] [-s SAMPLE_STD_MODIFIER] Classes...
    
    Runs the benchmark for each of the named classes. All named classes must be
    present in the wtracker module. The benchmark is carried out with the
    specified video and database as arguments. The video and database are
    fetched from VIDEO_DIRECTORY and DATABASE_DIRECTORY, as specified in
    common.settings. The result videos are saved with OUTPUT_NAME in the file
    name.

    Optional arguments:
        -n NUM_PARTICLES: Number of particles to use, default 100
        -b BENCHMARK: If "True", the tracking is run as a benchmark. Otherwise
            just runs the trackers.
    Note that these arguments must appear before the Classes list.
    """

    import sys

    if len(sys.argv) <= 1:
        print run_cli.__doc__
        sys.exit()

    num_particles = 100

    from common import cliutils
    args, op_args = cliutils.extract_variables(sys.argv[1:], "VIDEO_NAME DATABASE_NAME [-o OUTPUT_NAME] [-n PARTICLES] [-b BENCHMARK] [-v PRINT_VIDEO] [-p LP] [-P ERROR_LP] [-a WEIGHT_POWER] [-g GOODNESS_POWER] [-s SAMPLE_STD_MODIFIER] TRACKER_CLASSES...")

    video_name, database_name, class_names = args
    if "PARTICLES" in op_args.keys():
        num_particles = int(op_args["PARTICLES"])
    tracker_classes = [getattr(wtracker, c) for c in class_names]

    print "Using video: %s"%(video_name)
    print "Using database: %s"%(database_name)
    print "Using %i particles"%(num_particles)
    
    print
    print "Benchmarking tracker classes:"
    for c in tracker_classes:
        print "\t%s"%(c.__name__)
    print
            
    benchmark = TrackerRunner(tracker_classes, video_name, database_name, num_particles, **op_args)

    if "BENCHMARK" in op_args.keys() and op_args["BENCHMARK"] == "True":
        benchmark.run_benchmark()
    else:
        benchmark.run()

    print_video = True
    if "PRINT_VIDEO" in op_args.keys():
        print_video = op_args["PRINT_VIDEO"] == "True"

    if print_video:
        if "OUTPUT_NAME" in op_args.keys():
            benchmark.export_results(op_args["OUTPUT_NAME"])
        else:
            benchmark.export_results()
#    benchmark.evaluate_results()
#    benchmark.animate(0)

if __name__ == "__main__":
    run_cli()
